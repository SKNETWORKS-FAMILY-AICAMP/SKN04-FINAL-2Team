import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Dropdown.css";

const Dropdown = ({ hideDropdown }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleLinkClick = () => {
    setIsOpen(false);
    hideDropdown(); // 드롭다운 메뉴 숨기기
  };

  return (
    <div className={`dropdown ${isOpen ? "open" : ""}`}>
      <button onClick={toggleDropdown} className="dropdown-button">
        Settings
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <Link to="/user-management" onClick={handleLinkClick}>관리 페이지</Link>
          <Link to="/admin-page" onClick={handleLinkClick}>회원관리</Link>
        </div>
      )}
    </div>
  );
};

export default Dropdown;