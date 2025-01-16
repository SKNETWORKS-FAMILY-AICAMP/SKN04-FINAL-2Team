import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { pdfjs } from "react-pdf"; // react-pdf 라이브러리
import axiosInstance from "../../context/axiosInstance";
import { useAuth } from '../../context/AuthContext';
import "./SearchResults.css";

// PDF.js 워커 경로 설정 (정적 경로 사용)
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const SearchResults = ({ query, setQuery }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [resumes, setResumes] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [viewedResumes, setViewedResumes] = useState([]);
  const [isHiddenBarOpen, setIsHiddenBarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState({}); // 북마크 로딩 상태 추가
  const [searchQuery, setSearchQuery] = useState(query);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const encodedQuery = encodeURIComponent(query);
        const response = await axiosInstance.get(`/profile/search/?query=${encodedQuery}`);

        const data = response.data;
        const { results, keywords } = data;

        console.log("Fetched data:", data);

        setKeywords(keywords);

        // 이력서 데이터 업데이트
        setResumes(results.map(profile => ({
          profile_id: profile.profile_id,
          name: profile.name,
          job_category: profile.job_category,
          career_year: profile.career_year,
          ai_analysis: profile.ai_analysis,
          pdf_url: profile.pdf_url // 백엔드에서 제공된 PDF URL 포함
        })));

      } catch (error) {
        console.error("검색 결과 로딩 중 오류 발생:", error);
      }
    };

    if (query) {
      fetchResumes();
    }
  }, [query]);

  const handleAddBookmark = async (profile) => {
    if (!user) {
      alert("북마크를 추가하려면 로그인이 필요합니다.");
      return;
    }

    if (isLoading[profile.profile_id]) return;
    setIsLoading(prev => ({ ...prev, [profile.profile_id]: true }));
    
    try {
      // axiosInstance를 사용하여 북마크 추가 요청
      const response = await axiosInstance.post('/profile/bookmark/add/', {
        profile_id: profile.profile_id,
        user: user,
        ai_analysis: profile.ai_analysis
      });

      if (response.data.success) {
        alert("북마크가 추가되었습니다.");
      }
    } catch (error) {
      if (error.response?.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
      } else if (error.response?.status === 409) {
        alert("이미 북마크된 이력서입니다.");
      } else {
        alert("북마크 추가 중 오류가 발생했습니다.");
      }
      console.error("북마크 추가 중 오류 발생:", error);
    } finally {
      setIsLoading(prev => ({ ...prev, [profile.profile_id]: false }));
    }
  };

  // 새로운 창에서 PDF 열기
  const handleViewDetails = (profile) => {
    if (profile.pdf_url) {
      // 새 창에서 해당 이력서의 PDF 열기
      window.open(profile.pdf_url, "_blank");
    } else {
      console.error("PDF URL이 존재하지 않습니다.");
    }

    // viewedResumes 상태 업데이트
    setViewedResumes((prevViewedResumes) => {
      if (!prevViewedResumes.some((r) => 
        r.name === profile.name && 
        r.job_category === profile.job_category && 
        r.career_year === profile.career_year)) {
        return [...prevViewedResumes, profile];
      }
      return prevViewedResumes;
    });
  };

  const toggleHiddenBar = () => {
    setIsHiddenBarOpen(!isHiddenBarOpen);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setQuery(searchQuery);
    navigate(`/search-results?query=${searchQuery}`);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSearchSubmit(e);
    }
  };

  return (
    <div className="search-results">
      <div className="main-search-container-results">
        <form className="main-search-bar" onSubmit={handleSearchSubmit}>
          <textarea
            placeholder="회사 요구사항 입력"
            value={searchQuery}
            onChange={handleSearchChange}
            onKeyDown={handleKeyDown}
            className="main-search-input"
          />
          <button type="submit" className="main-search-button">검색</button>
        </form>
      </div>
      {/* 키워드 표시 */}
      <div className="keywords-container">
        {keywords.map((keyword, index) => (
          <span key={index} className="keyword">
            {keyword}
          </span>
        ))}
      </div>

      {/* 검색 결과 표시 */}
      <div className="search-results-content">
        {resumes.map((profile, index) => (
          <div key={index} className="resume-box-container">
            <div key={index} className="resume-box">
              <div className="resume-details">
                <p>
                  <strong>이름: </strong> {profile.name} 
                  <strong> 직군: </strong> {profile.job_category} 
                  <strong> 경력: </strong> {profile.career_year}년
                </p>
                {/* <div className="ai-analysis">
                  <p><strong>AI 분석 결과: </strong>{profile.ai_analysis}</p>
                </div> */}
              </div>
            </div>
            <div className="resume-buttons">
              <button className="bookmark-button" onClick={() => handleAddBookmark(profile)}>Bookmark</button>
              <button className="details-button" onClick={() => handleViewDetails(profile)}>상세보기</button>
            </div>
          </div>
        ))}
      </div>
    
      {/* 히든 바 */}
      <div className="search-results-container">
        <div className={`hidden-bar ${isHiddenBarOpen ? 'open' : ''}`}>
          <div className="hidden-bar-content">
            <ul>
              {viewedResumes.map((profile, index) => (
                <div key={index} className="hidden-bar-resume-box" onClick={() => handleViewDetails(profile)}>
                  <p>이름: {profile.name}</p>
                  <p>직군: {profile.job_category}</p>
                  <p>경력: {profile.career_year}</p>
                </div>
              ))}
            </ul>
          </div>
        </div>
        <button 
          className={`toggle-hidden-bar-button ${isHiddenBarOpen ? 'open' : ''}`} 
          onClick={toggleHiddenBar}
        >
          {isHiddenBarOpen ? "▷" : "◁"}
        </button>
      </div>
    </div>
  );
};

export default SearchResults;