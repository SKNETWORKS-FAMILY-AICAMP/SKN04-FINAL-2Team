import React, { useEffect, useState } from "react";
import { Route, Routes, Link, useLocation } from "react-router-dom";
import Dropdown from "./components/dropdown/Dropdown";
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
  const [prevScrollPos, setPrevScrollPos] = useState(0);
  const [isNavbarVisible, setIsNavbarVisible] = useState(true);
  const [bookmarks, setBookmarks] = useState([]);
  const { user, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      const currScrollPos = window.scrollY;

      if (currScrollPos > prevScrollPos) {
        setIsNavbarVisible(false);
      } else {
        setIsNavbarVisible(true);
      }

      setPrevScrollPos(currScrollPos);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [prevScrollPos]);

  const hideDropdown = () => {
    // setIsDropdownVisible(false);
  };

  const addBookmark = (profile) => {
    setBookmarks((prevBookmarks) => [...prevBookmarks, profile]);
  };

  const removeBookmark = (profile) => {
    setBookmarks((prevBookmarks) => prevBookmarks.filter((b) => b !== profile));
  };

  return (
    <div>
      <nav
        className="navbar"
        style={{
          transform: isNavbarVisible ? "translateY(0%)" : "translateY(-105%)",
        }}
      >
        <div className="logo">
          <i className="fa-solid fa-font-awesome"></i>
          <Link to="/">LOGO</Link>
        </div>
        <div className="menu">
          <div className="menu-links">
            <Link to="/bookmarks">Bookmark</Link>
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
          </div>
          <Dropdown hideDropdown={hideDropdown} user={user} />
        </div>
        <div className="menu-btn">
          <i className="fa-solid fa-bars"></i>
        </div>
      </nav>
      <MainContent
        bookmarks={bookmarks}
        removeBookmark={removeBookmark}
        addBookmark={addBookmark}
      />
    </div>
  );
};

const MainContent = ({ bookmarks, removeBookmark, addBookmark }) => {
  const location = useLocation();
  const { user } = useAuth();

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
            element={<Login onClose={() => window.history.back()} />}
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
        </Routes>
      </div>
    </div>
  );
};

export default App;