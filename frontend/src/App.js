import React, { useState, useEffect, useRef } from "react";
import { Route, Routes, Link, useLocation, useNavigate, Navigate } from "react-router-dom";
import Login from "./components/navbar/Login";
import UserManagement from "./components/management/UserManagement";
import AdminPage from "./components/admin/AdminPage";
import Sidebar from "./components/sidebar/Sidebar";
import MainSearch from "./components/search/MainSearch";
import SearchResults from "./components/search/SearchResults";
import BookmarkPage from "./components/navbar/BookmarkPage";
import { useAuth } from './context/AuthContext';
import "./App.css";
import logo from "./images/logo_v2.png";

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

  // user 상태가 변경될 때 showLogout 상태를 false로 설정
  useEffect(() => {
    setShowLogout(false);
  }, [user]);

  // 로그아웃 후 MainSearch 화면으로 이동하고 검색어 초기화
  const handleLogout = () => {
    logout();
    setQuery(""); // 검색어 초기화
    navigate("/");
  };

  return (
    <div>
      <nav className="navbar">
        <div className="logo">
          <Link to="/">
            <img src={logo} alt="Logo" className="logo-image" />
          </Link>
        </div>
        <div className="menu">
          <div className="menu-links">
            <Link to="/">
              {/* <img src> </img> */}
            </Link>
          </div>
          <Link to="/bookmarks" className="bookmark-link">Bookmark</Link>
          {user ? (
            <div className="dropdown" ref={dropdownRef}>
              <span onClick={handleUsernameClick} className="dropdown-toggle">
                {user.username}
              </span>
              {showLogout && (
                <div className="dropdown-menu">
                  <button onClick={handleLogout} className="logout-button">
                    로그아웃
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link to="/login" className="login-button">Login</Link>
          )}
          <button onClick={handleSettingsClick} className="settings-button">
            Settings
          </button>
        </div>
        <div className="menu-btn">
          <i className="fa-solid fa-bars"></i>
        </div>
      </nav>
      <MainContent query={query} setQuery={setQuery} />
    </div>
  );
};

const MainContent = ({ query, setQuery }) => {
  const location = useLocation();
  const { user } = useAuth();
  const navigate = useNavigate();

  const showSidebar =
    location.pathname !== "/" &&
    location.pathname !== "/search-results" &&
    location.pathname !== "/login" &&
    location.pathname !== "/bookmarks";

  return (
    <div>
      {showSidebar && <Sidebar user={user} />}
      <div style={{ flex: 1, padding: "20px" }}>
        {/* 라우트 설정 */}
        <Routes>
          <Route path="/user-management" element={<UserManagement />} />
          <Route path="/admin-page" element={<AdminPage />} />
          <Route path="/" element={user ? <MainSearch query={query} setQuery={setQuery} /> : <Navigate to="/login" />} />
          <Route
            path="/search-results"
            element={user ? <SearchResults query={query} setQuery={setQuery} /> : <Navigate to="/login" />}
          />
          <Route
            path="/login"
            element={<Login onClose={() => navigate("/")} />}
          />
          <Route
            path="/bookmarks"
            element={user ? <BookmarkPage user={user} /> : <Navigate to="/login" />}
          />
          <Route
            path="/settings"
            element={user ? <Sidebar user={user} /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </div>
  );
};

export default App;