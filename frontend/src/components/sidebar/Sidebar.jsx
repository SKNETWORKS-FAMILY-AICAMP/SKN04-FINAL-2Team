import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css";
import Login from "../management/Login"; // 로그인 폼 컴포넌트
import UserDeletion from "../management/UserDeletion"; // 회원삭제 컴포넌트
import SignUp from "../management/SignUp"; // 회원가입 컴포넌트


const Sidebar = () => {
  const [activeMenu, setActiveMenu] = useState("");
  const [showLogin, setShowLogin] = useState(false); // 로그인 폼 표시 상태
  const [isDeletingUser, setIsDeletingUser] = useState(false); // 회원삭제 모달 상태
  const [showSignUp, setShowSignUp] = useState(false); // 회원가입 폼 표시 상태

  const toggleMenu = (menu) => {
    setActiveMenu(activeMenu === menu ? "" : menu);
  };

  const handleLoginClick = () => {
    setShowLogin(true); // 로그인 폼 표시
  };

  const handleSignUpClick = () => {
    setShowSignUp(true); // 회원가입 폼 표시
  };

  return (
    <>
      <aside className="sidebar">
        <header>
          <p>Settings</p>
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
              id="settings"
              name="sidebar"
              checked={activeMenu === "settings"}
              onChange={() => toggleMenu("settings")}
            />
            <label htmlFor="settings">
              <i className="ai-gear"></i>
              <p>회원관리</p>
              <i className="ai-chevron-down-small"></i>
            </label>
            <div className={`sub-menu ${activeMenu === "settings" ? "open" : ""}`}>
              <ul>
                {/* 회원등록 버튼*/}
                <li><button onClick={handleSignUpClick}>회원등록</button></li>
                {/* 로그인 버튼 */}
                <li><button onClick={handleLoginClick}>Login</button></li>

                {/* 회원삭제 버튼 */}
                <li><button onClick={() => setIsDeletingUser(true)}>회원삭제</button></li>
              </ul>
            </div>
          </li>
        </ul>
      </aside>

      {/* 로그인 폼 표시 */}
      {showLogin && (
        <div className="login-overlay">
          <Login onClose={() => setShowLogin(false)} />
        </div>
      )}

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