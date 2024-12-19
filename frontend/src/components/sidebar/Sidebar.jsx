import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css";
import Login from "../management/Login"; // Host 로그인 폼 컴포넌트

const Sidebar = () => {
  const [activeMenu, setActiveMenu] = useState("");
  const [loginType, setLoginType] = useState(""); // 현재 표시할 로그인 창 타입 ("Host", "Superuser", "User")

  const toggleMenu = (menu) => {
    setActiveMenu(activeMenu === menu ? "" : menu);
  };

  const handleLoginClick = (type) => {
    setLoginType(type); // 클릭한 타입("Host", "Superuser", "User") 설정
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
                {/* 각각의 버튼 클릭 시 handleLoginClick 호출 */}
                <li><button onClick={() => handleLoginClick("Host")}>Login</button></li>
              </ul>
            </div>
          </li>
        </ul>
      </aside>

      {/* 로그인 폼 표시 */}
      {loginType === "Host" && (
        <div className="login-overlay">
          <Login onClose={() => setLoginType("")} />
        </div>
      )}
    </>
  );
};

export default Sidebar;
