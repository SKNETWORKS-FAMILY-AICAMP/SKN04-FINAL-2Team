import React, { useState } from "react";
import { Link, useNavigate} from "react-router-dom";
import "./Dropdown.css";

const Dropdown = ({ hideDropdown, user }) => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleDropdown = () => {
    // is_superuser 혹은 is_staff 만 드롭다운 열기 가능
    if (user === "is_superuser" || user === "is_staff") {
      setIsOpen(!isOpen);
    } else {
      alert("해당 기능은 관리자만 접속이 가능합니다.");
    }
    // setIsOpen(!isOpen);
  };

  const handleLinkClick = (path) => {
    if (path === "/user-management" && user !== "is_superuser") {
      // 관리 페이지 접근 제한
      alert("해당 기능은 관리자만 접속이 가능합니다.");
      return; 
    }
    setIsOpen(false);
    hideDropdown(); // 드롭다운 닫기
    navigate(path);
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