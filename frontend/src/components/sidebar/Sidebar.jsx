import React, { useState } from "react";
// import { Link } from "react-router-dom";
import "./Sidebar.css";
import UserDeletion from "../management/UserDeletion"; // 회원삭제 컴포넌트
import SignUp from "../management/SignUp"; // 회원가입 컴포넌트

const Sidebar = () => {
  const [activeMenu, setActiveMenu] = useState("");
  const [isDeletingUser, setIsDeletingUser] = useState(false); // 회원삭제 모달 상태
  const [showSignUp, setShowSignUp] = useState(false); // 회원가입 폼 표시 상태
  const [isUserManagementOpen, setIsUserManagementOpen] = useState(false); // 회원관리 드롭다운 상태

  const toggleMenu = (menu) => {
    setActiveMenu(activeMenu === menu ? "" : menu);
  };

  const handleSignUpClick = () => {
    setShowSignUp(true); // 회원가입 폼 표시
  };

  const toggleUserManagement = () => {
    setIsUserManagementOpen(!isUserManagementOpen);
  };

  return (
    <>
      <aside className="sidebar">
        <header>
          <h1>Settings</h1>
        </header>
        <ul>
          <li>
            <input
              type="radio"
              id="dashboard"
              name="sidebar"
              checked={activeMenu === "dashboard"}
              onChange={() => toggleMenu("dashboard")}
            />
            <label htmlFor="dashboard">
              <i className="ai-dashboard"></i>
              <p>관리페이지</p>
            </label>
          </li>
          <li>
            <input
              type="radio"
              id="userManagement"
              name="sidebar"
              checked={activeMenu === "userManagement"}
              onChange={() => toggleMenu("userManagement")}
            />
            <label htmlFor="userManagement" onClick={toggleUserManagement}>
              <i className="ai-user-management"></i>
              <p>회원관리</p>
              <i className={`ai-chevron-${isUserManagementOpen ? "up" : "down"}-small`}></i>
            </label>
            {isUserManagementOpen && (
              <ul className="dropdown">
                <li>
                  <button onClick={handleSignUpClick}>회원등록</button>
                </li>
                <li>
                  <button onClick={() => setIsDeletingUser(true)}>회원삭제</button>
                </li>
              </ul>
            )}
          </li>
        </ul>
      </aside>

      {/* 회원삭제 모달 표시 */}
      {isDeletingUser && (
        <div className="user-deletion-overlay">
          <UserDeletion onClose={() => setIsDeletingUser(false)} />
        </div>
      )}

      {/* 회원가입 폼 표시 */}
      {showSignUp && (
        <div className="login-overlay">
          <SignUp onClose={() => setShowSignUp(false)} />
        </div>
      )}
    </>
  );
};

export default Sidebar;