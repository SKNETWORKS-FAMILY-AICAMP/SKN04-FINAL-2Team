import React, { useState, useEffect } from "react";
import { Route, Routes, Link, useLocation, useNavigate } from "react-router-dom";
import Login from "./components/navbar/Login";
import UserManagement from "./components/management/UserManagement";
import AdminPage from "./components/admin/AdminPage";
import Sidebar from "./components/sidebar/Sidebar";
import MainSearch from "./components/search/MainSearch";
import SearchResults from "./components/search/SearchResults";
import BookmarkPage from "./components/navbar/BookmarkPage";
import { useAuth } from './context/AuthContext';
import axios from "axios";
import "./App.css";

const App = () => {
  const [bookmarks, setBookmarks] = useState([]);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleSettingsClick = () => {
    if (user && (user.is_superuser || user.is_staff)) {
      navigate("/settings");
    } else {
      alert("해당 기능은 관리자만 접속이 가능합니다.");
    }
  };


  const removeBookmark = async (profile) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/profile/bookmark/remove/${profile.profile_id}/`);
      fetchBookmarks(); // 북마크 삭제 후 목록 새로고침
    } catch (error) {
      console.error("북마크 삭제 실패:", error.response?.data || error.message);
    }
  };
  
  // 북마크 목록을 갱신하기 위한 함수
  const fetchBookmarks = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/profile/bookmark/`);
      setBookmarks(response.data);
    } catch (error) {
      console.error("북마크 목록 가져오기 실패:", error.response?.data || error.message);
    }
  };

  /** 📌 사용자 인증 후 북마크 목록 가져오기 */
  useEffect(() => {
    if (user) {
      fetchBookmarks();
    }
  }, [user]); // user가 변경될 때마다 실행됨

  if (!user) {
    return <Login onClose={() => navigate("/")} />;
  }

  return (
    <div>
      <nav className="navbar">
        <div className="logo">
          <i className="fa-solid fa-font-awesome"></i>
          <Link to="/">LOGO</Link>
        </div>
        <div className="menu">
          <div className="menu-links">
            <Link to="/bookmarks">Bookmark</Link>
          </div>
          {user ? (
              <>
                <span>{user.username}</span>
                <button onClick={logout} className="logout-button">
                  로그아웃
                </button>
              </>
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
      <MainContent
        bookmarks={bookmarks}
        removeBookmark={removeBookmark}
      />
    </div>
  );
};

const MainContent = ({ bookmarks, removeBookmark, addBookmark }) => {
  const location = useLocation();
  const { user } = useAuth();
  const navigate = useNavigate(); // useNavigate 훅을 사용하여 navigate 함수 정의

  const showSidebar =
    location.pathname !== "/" &&
    location.pathname !== "/search-results" &&
    location.pathname !== "/login" &&
    location.pathname !== "/bookmarks";

  return (
    <div>
      {showSidebar && <Sidebar user={user} />}
      <div style={{ flex: 1, padding: "20px" }}>
        <Routes>
          <Route path="/user-management" element={<UserManagement />} />
          <Route path="/admin-page" element={<AdminPage />} />
          <Route path="/" element={<MainSearch />} />
          <Route
            path="/search-results"
            element={<SearchResults addBookmark={addBookmark} />}
          />
          <Route
            path="/login"
            element={<Login onClose={() => navigate("/")} />}
          />
          <Route
            path="/bookmarks"
            element={
              <BookmarkPage
                bookmarks={bookmarks}
                removeBookmark={removeBookmark}
              />
            }
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