import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MainSearch from "./MainSearch";
import { pdfjs } from "react-pdf"; // react-pdf 라이브러리
import axios from "axios";
import "./SearchResults.css";


// PDF.js 워커 경로 설정 (정적 경로 사용)
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const SearchResults = ({ addBookmark }) => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query");
  const [resumes, setResumes] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [viewedResumes, setViewedResumes] = useState([]);
  const [isHiddenBarOpen, setIsHiddenBarOpen] = useState(false);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/profile/search/?query=${query}`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const data = response.data;
        const { results } = data;

        console.log("Fetched data:", data);

        // 키워드 데이터 업데이트
        // 테스트용 더미데이터 
        const keywords = ["React", "Node.js", "Python", "Django"];
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
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/profile/bookmark/add/`, 
      {
        profile_id: profile.profile_id
      }, 
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

      if (response.status === 200 || response.status === 201) {
        console.log("북마크 추가 성공:", profile);
        addBookmark(profile);
      } else {
        console.error("북마크 추가 중 오류 발생:", response.statusText);
      }
    } catch (error) {
      console.error("북마크 추가 중 오류 발생:", error);
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
      if (!prevViewedResumes.some((r) => r.name === profile.name)) {
        return [...prevViewedResumes, profile];
      }
      return prevViewedResumes;
    });
  };

  const toggleHiddenBar = () => {
    setIsHiddenBarOpen(!isHiddenBarOpen);
  };

  return (
    <div className="search-results">
      <div className="main-search-container">
        <MainSearch initialQuery={query} />
      </div>
      <div className="search-results-container">
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
                    <strong> 경력: </strong> {profile.career_year}
                  </p>
                  <div className="ai-analysis">
                    <p><strong>AI 분석 결과: </strong>{profile.ai_analysis}</p>
                  </div>
                </div>
              </div>
              <div className="resume-buttons">
                <button className="bookmark-button" onClick={() => handleAddBookmark(profile)}>Bookmark</button>
                <button className="details-button" onClick={() => handleViewDetails(profile)}>상세보기</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    
      {/* 히든 바 */}
      <div className="search-results-container">
        <div className={`hidden-bar ${isHiddenBarOpen ? 'open' : ''}`}>
          <ul>
            {viewedResumes.map((profile, index) => (
              <div key={index} className="hidden-bar-resume-box">
                <p>이름: {profile.name}</p>
                <p>직군: {profile.job_category}</p>
                <p>경력: {profile.career_year}</p>
              </div>
            ))}
          </ul>
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