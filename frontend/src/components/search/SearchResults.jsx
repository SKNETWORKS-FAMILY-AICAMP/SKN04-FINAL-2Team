import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MainSearch from "./MainSearch";
import "./SearchResults.css";

const SearchResults = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query");
  const [resumes, setResumes] = useState([]);
  const [keywords, setKeywords] = useState([]);

  useEffect(() => {
    console.log("Fetching resumes for query:", query); // 로그 추가

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
      const keywordData = ["React", "Node.js", "Python", "Django"];
      setKeywords(keywordData);
    };

    fetchResumes();
  }, [query]);

  return (
    <div className="search-results-container">
      <MainSearch initialQuery={query} />
      <div className="keywords-container">
        {keywords.map((keyword, index) => (
          <div key={index} className="keyword-box">
            {keyword}
          </div>
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
              <button className="bookmark-button">Bookmark</button>
              <button className="details-button">상세보기</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;