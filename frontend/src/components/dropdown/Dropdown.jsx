import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Dropdown.css";

const Dropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={`dropdown ${isOpen ? "open" : ""}`}>
      <button onClick={() => setIsOpen(!isOpen)} className="dropdown-button">
        Settings
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <Link to="/user-management">관리 페이지</Link>
          <Link to="/admin-page">회원관리</Link>
        </div>
      )}
    </div>
  );
};

export default Dropdown;