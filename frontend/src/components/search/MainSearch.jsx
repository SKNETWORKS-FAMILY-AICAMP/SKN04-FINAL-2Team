import React from "react";
import { useNavigate } from "react-router-dom";
import "./MainSearch.css";

const MainSearch = ({ query, setQuery }) => {
  const navigate = useNavigate();

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate(`/search-results?query=${query}`);
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