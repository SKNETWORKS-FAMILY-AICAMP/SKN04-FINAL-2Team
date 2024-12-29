import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"; // axios 라이브러리 사용
import "./MainSearch.css";

const MainSearch = ({ initialQuery = "" }) => {
  const [query, setQuery] = useState(initialQuery);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    try {
      // API 요청 보내기
      const response = await axios.get(`/api/search/?query=${query}`);
      console.log(response.data); // 응답 데이터 처리
      navigate(`/search-results?query=${query}`); // 검색 결과 페이지로 이동
    } catch (error) {
      console.error("검색 중 오류 발생:", error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="main-search-container">
      <form className="main-search-bar" onSubmit={handleSubmit}>
        <textarea
          placeholder="회사 요구사항 입력"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="main-search-input"
        />
        <button type="submit" className="main-search-button">검색</button>
      </form>
    </div>
  );
};

export default MainSearch;