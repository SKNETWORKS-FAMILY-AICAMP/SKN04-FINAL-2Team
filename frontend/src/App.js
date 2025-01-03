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
import axiosInstance from './context/axiosInstance';
import "./App.css";

const App = () => {
  // 상태 관리
  const [bookmarks, setBookmarks] = useState([]);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  /** ✅ 관리자 설정 페이지 접근 처리 */
  const handleSettingsClick = () => {
    if (user && (user.is_superuser || user.is_staff)) {
      navigate("/settings");
    } else {
      alert("해당 기능은 관리자만 접속이 가능합니다.");
    }
  };

  /** ✅ 북마크 추가 함수 */
  const addBookmark = async (profile) => {
    try {
      // GET 메서드로 변경
      const response = await axiosInstance.post(`/profile/bookmark/add/`, {
        profile_id: profile.profile_id,
        ai_analysis: profile.ai_analysis,
        user: user.username
      });
      
      if (response.status === 200 || response.status === 201) {
        await fetchBookmarks(); // 북마크 추가 후 목록 새로고침
        alert("북마크가 추가되었습니다.");
      }
    } catch (error) {
      if (error.response?.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
      } else if (error.response?.status === 409) {
        alert("이미 북마크된 이력서입니다.");
      } else {
        console.error("북마크 추가 실패:", error.response?.data || error.message);
      }
    }
  };

  /** ✅ 북마크 제거 함수 */
  const removeBookmark = async (profile) => {
    try {
      // GET 메서드로 변경
      await axiosInstance.get(`/profile/bookmark/remove/`, {
        params: {
          profile_id: profile.profile_id
        }
      });
      await fetchBookmarks(); // 북마크 삭제 후 목록 새로고침
      alert("북마크가 삭제되었습니다.");
    } catch (error) {
      if (error.response?.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
      } else {
        console.error("북마크 삭제 실패:", error.response?.data || error.message);
      }
    }
  };
  
  /** ✅ 북마크 목록 조회 함수 */
  const fetchBookmarks = async () => {
    try {
      // GET 메서드로 변경
      const response = await axiosInstance.get('/profile/bookmark/');
      if (response.data.success) {
        setBookmarks(response.data.bookmarks);
      }
    } catch (error) {
      if (error.response?.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
      } else {
        console.error("북마크 목록 가져오기 실패:", error.response?.data || error.message);
      }
    }
  };

  /** ✅ 사용자 인증 후 북마크 목록 가져오기 */
  useEffect(() => {
    if (user) {
      fetchBookmarks();
    }
  }, [user]); // user가 변경될 때마다 실행됨

  // 로그인하지 않은 경우 로그인 페이지 표시
  if (!user) {
    return <Login onClose={() => navigate("/")} />;
  }

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
      {/* 메인 컨텐츠 */}
      <MainContent
        bookmarks={bookmarks}
        removeBookmark={removeBookmark}
        addBookmark={addBookmark}
      />
    </div>
  );
};

/** ✅ 메인 컨텐츠 컴포넌트 */
const MainContent = ({ bookmarks, removeBookmark, addBookmark }) => {
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