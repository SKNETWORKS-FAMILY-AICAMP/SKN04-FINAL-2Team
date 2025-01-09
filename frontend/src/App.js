import React, { useState, useEffect, useRef } from "react";
import { Route, Routes, Link, useLocation, useNavigate } from "react-router-dom";
import Login from "./components/navbar/Login";
import UserManagement from "./components/management/UserManagement";
import AdminPage from "./components/admin/AdminPage";
import Sidebar from "./components/sidebar/Sidebar";
import MainSearch from "./components/search/MainSearch";
import SearchResults from "./components/search/SearchResults";
import BookmarkPage from "./components/navbar/BookmarkPage";
import { useAuth } from './context/AuthContext';
import "./App.css";

const App = () => {
  const { user, logout } = useAuth();
  const [showLogout, setShowLogout] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const [query, setQuery] = useState(""); // 검색어 상태 추가

  /** ✅ 관리자 설정 페이지 접근 처리 */
  const handleSettingsClick = () => {
    if (user && (user.is_superuser || user.is_staff)) {
      navigate("/settings");
    } else {
      alert("해당 기능은 관리자만 접속이 가능합니다.");
    }
  };

  const handleUsernameClick = () => {
    setShowLogout(!showLogout);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowLogout(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div>
      {/* 네비게이션 바 */}
      <nav className="navbar">
        <div className="logo">
          <i className="fa-solid fa-font-awesome"></i>
          <Link to="/">LOGO</Link>
        </div>
        <div className="menu">
          <div className="menu-links">
            <Link to="/bookmarks">Bookmark</Link>
          </div>
          {/* 사용자 인증 상태에 따른 메뉴 표시 */}
          {user ? (
            <div className="dropdown" ref={dropdownRef}>
              <span onClick={handleUsernameClick} className="dropdown-toggle">
                {user.username}
              </span>
              {showLogout && (
                <div className="dropdown-menu">
                  <button onClick={logout} className="logout-button">
                    로그아웃
                  </button>
                </div>
              )}
            </div>
            ) : (
              <Link to="/login">Login</Link>
            )}
          <button onClick={handleSettingsClick} className="settings-button">
            Settings
          </button>
        </div>
        <div className="menu-btn">
          <i className="fa-solid fa-bars"></i>
        </div>
      </nav>
      {/* 메인 컨텐츠 */}
      <MainContent query={query} setQuery={setQuery} />
    </div>
  );
};

/** ✅ 메인 컨텐츠 컴포넌트 */
const MainContent = ({ query, setQuery }) => {
  const location = useLocation();
  const { user } = useAuth();
  const navigate = useNavigate();

  // 사이드바 표시 여부 결정
  const showSidebar =
    location.pathname !== "/" &&
    location.pathname !== "/search-results" &&
    location.pathname !== "/login" &&
    location.pathname !== "/bookmarks";

  return (
    <div>
      {/* 조건부 사이드바 렌더링 */}
      {showSidebar && <Sidebar user={user} />}
      <div style={{ flex: 1, padding: "20px" }}>
        {/* 라우트 설정 */}
        <Routes>
          <Route path="/user-management" element={<UserManagement />} />
          <Route path="/admin-page" element={<AdminPage />} />
          <Route path="/" element={<MainSearch query={query} setQuery={setQuery} />} />
          <Route
            path="/search-results"
            element={<SearchResults query={query} setQuery={setQuery} />}
          />
          <Route
            path="/login"
            element={<Login onClose={() => navigate("/")} />}
          />
          <Route
            path="/bookmarks"
            element={<BookmarkPage user={user} />}
          />
          <Route
            path="/settings"
            element={<Sidebar user={user} />}
          />
        </Routes>
      </div>
    </div>
  );
};

export default App;