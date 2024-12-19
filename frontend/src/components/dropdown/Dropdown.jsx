import React, { useState } from "react";
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
          <a href="/user-management">회원관리</a>
          <a href="/admin-page">관리 페이지</a>
        </div>
      )}
    </div>
  );
};

export default Dropdown;