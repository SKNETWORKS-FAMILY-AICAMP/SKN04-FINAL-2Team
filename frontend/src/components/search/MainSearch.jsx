import React, { useState } from "react";
import "./MainSearch.css";

const MainSearch = () => {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 검색 로직 추가
    console.log("검색어:", query);
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
          placeholder="검색어 입력"
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