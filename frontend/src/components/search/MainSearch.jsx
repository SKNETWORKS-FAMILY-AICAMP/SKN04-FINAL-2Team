import React from "react";
import { useNavigate } from "react-router-dom";
import "./MainSearch.css";
import search from "../../images/search_icon.png";

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
          placeholder="찾으시는 인재상을 입력해 주세요."
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="main-search-input"
          rows="4"
        />
        
        <button type="submit" >
          <img src={search} alt="Logo" className="main-search-button"/>
        </button>
      </form>
    </div>
  );
};

export default MainSearch;