import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MainSearch from "./MainSearch";
import "./SearchResults.css";

const SearchResults = ({ addBookmark }) => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query");
  const [resumes, setResumes] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [viewedResumes, setViewedResumes] = useState([]);
  const [isHiddenBarOpen, setIsHiddenBarOpen] = useState(false);

  useEffect(() => {
    console.log("Fetching resumes for query:", query);

    const fetchResumes = async () => {
      // 실제 API 호출 시 아래 코드를 사용하세요.
      // const response = await fetch(`http://localhost:8000/api/resumes?query=${query}`);
      // const data = await response.json();

      // Mock 데이터
      const data = [
        { name: "John Doe", occupation: 30, career: "Bachelor's Degree" },
        { name: "Jane Smith", occupation: 28, career: "Master's Degree" },
        { name: "Alice Johnson", occupation: 25, career: "PhD" },
      ];

      setResumes(data);
      // Mock 키워드 데이터
      const keywordData = ["React", "Node.js", "Python", "Django", "React", "Node.js", "Python", "Django", "Django", "React", "Node.js"];
      setKeywords(keywordData);
    };

    fetchResumes();
  }, [query]);

  const handleViewDetails = (resume) => {
    setViewedResumes((prevViewedResumes) => {
      if (!prevViewedResumes.some((r) => r.name === resume.name)) {
        return [...prevViewedResumes, resume];
      }
      return prevViewedResumes;
    });
  };

  const toggleHiddenBar = () => {
    setIsHiddenBarOpen(!isHiddenBarOpen);
  };

  return (
    <div className="search-results-container">
      <MainSearch initialQuery={query} />
      <div className="keywords-container">
        {keywords.map((keyword, index) => (
          <span key={index} className="keyword">
            {keyword}
          </span>
        ))}
      </div>
      <div className="search-results-content">
        {resumes.map((resume, index) => (
          <div key={index} className="resume-box-container">
            <div key={index} className="resume-box">
              <div className="resume-details">
                <p><strong>이름: </strong> {resume.name} <strong>직군: </strong> {resume.occupation} <strong>경력: </strong> {resume.career}</p>
                <div className="ai-analysis">
                  <p><strong>AI 분석 결과: </strong></p>
                </div>
              </div>
            </div>
            <div className="resume-buttons">
              <button className="bookmark-button" onClick={() => addBookmark(resume)}>Bookmark</button>
              <button className="details-button" onClick={() => handleViewDetails(resume)}>상세보기</button>
            </div>
          </div>
        ))}
      </div>
      <div className="search-results-container">
        <div className={`hidden-bar ${isHiddenBarOpen ? 'open' : ''}`}>
          <ul>
            {viewedResumes.map((resume, index) => (
              <div key={index} className="hidden-bar-resume-box">
                <p>이름: {resume.name}</p>
                <p>직군: {resume.occupation}</p>
                <p>경력: {resume.career}</p>
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