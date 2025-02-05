import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { pdfjs } from "react-pdf"; 
import axiosInstance from "../../context/axiosInstance";
import { useAuth } from '../../context/AuthContext';
import "./SearchResults.css";
import search from "../../images/search_icon.png";
import logo from "../../images/logo_v2.png";
import PDF from "../../images/PDF_icon.png";
import bookmark from "../../images/bookmark_icon.png";

pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const SearchResults = ({ query, setQuery }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [resumes, setResumes] = useState([]);
  const [viewedResumes, setViewedResumes] = useState([]);
  const [isHiddenBarOpen, setIsHiddenBarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(query);
  const [aiAnalysisSkipped, setAiAnalysisSkipped] = useState(false);

  useEffect(() => {
    const fetchResumes = async () => {
      setIsLoading(true);
      try {
        const encodedQuery = encodeURIComponent(query);
        const response = await axiosInstance.get(`/profile/search/?query=${encodedQuery}`);

        const data = response.data;
        console.log("Fetched data:", data);

        setResumes(data.results.map(profile => ({
          profile_id: profile.profile_id,
          name: profile.name,
          job_category: profile.job_category,
          career_year: profile.career_year,
          ai_analysis: profile.ai_analysis,
          pdf_url: profile.pdf_url 
        })));

        setAiAnalysisSkipped(data.ai_analysis_skipped || false);
      } catch (error) {
        console.error("검색 결과 로딩 중 오류 발생:", error);
      } finally {
        setIsLoading(false); // 🔹 검색 완료 즉시 로딩 해제
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
      const response = await axiosInstance.post('/profile/bookmark/add/', {
        profile_id: profile.profile_id,
        user: user,
        ai_analysis: profile.ai_analysis
      });

      if (response.status === 201) {
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

  const handleViewDetails = (profile) => {
    if (profile.pdf_url) {
      window.open(profile.pdf_url, "_blank");
    } else {
      console.error("PDF URL이 존재하지 않습니다.");
    }

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
        <form className="main-search-bar-results" onSubmit={handleSearchSubmit}>
          <textarea
            placeholder="찾으시는 인재상을 입력해 주세요."
            value={searchQuery}
            onChange={handleSearchChange}
            onKeyDown={handleKeyDown}
            className="main-search-input-results"
            rows="2"
          />
          <button type="submit">
            <img src={search} alt="Logo" className="main-search-button-results"/>
          </button>
        </form>
      </div>
      <div className="search-results-content">
        {isLoading ? (
          <div className="search-results-count loading">
            <p> 🔍 검색 진행 중...</p>
          </div>
        ) : (
          <div className="search-results-count">
            <p> 총 {resumes.length}건의 검색 결과 </p>
          </div>
        )}
        {aiAnalysisSkipped && !isLoading && (
          <div className="analysis-warning">
            ⚠️ 총 결과가 15개 이상이 되어 분석 결과가 생략됩니다.
          </div>
        )}

        {!isLoading && resumes.length === 0 && (
          <div className="no-results">
            😔 검색 결과가 없습니다.
          </div>
        )}
        {resumes.map((profile, index) => (
          <div key={index} className="resume-box">
            <div className="resume-header">
              <img src={logo} alt="Logo" className="profile-logo-image" />
              <div className="profile-details">
                {profile.name} | {profile.job_category} | {profile.career_year}년차
              </div>
              <div className="resume-buttons">
                <button onClick={() => handleAddBookmark(profile)}>
                  <img src={bookmark} alt="bookmark" className="bookmark-button"/>
                </button>
                <button onClick={() => handleViewDetails(profile)}>
                  <img src={PDF} alt="PDF" className="details-button" />
                </button>
              </div>
            </div>
            <div className="ai-analysis">
              {profile.ai_analysis ? <p>{profile.ai_analysis}</p> : null}
            </div>
          </div>
        ))}
      </div>
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