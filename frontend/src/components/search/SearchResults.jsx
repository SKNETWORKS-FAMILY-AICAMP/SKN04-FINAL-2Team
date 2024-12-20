import React from "react";
import { useLocation } from "react-router-dom";
import "./SearchResults.css";

const SearchResults = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query");

  return (
    <div className="search-results-container">
      <div className="search-results-content">
        <p>{query}</p>
        {/* 검색 결과를 표시하는 로직 추가 */}
      </div>
    </div>
  );
};

export default SearchResults;