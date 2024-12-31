import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from "react-router-dom";
import Dropdown from "./components/dropdown/Dropdown";
import Login from "./components/navbar/Login";
import UserManagement from "./components/management/UserManagement";
import AdminPage from "./components/admin/AdminPage";
import Sidebar from "./components/sidebar/Sidebar";
import MainSearch from "./components/search/MainSearch";
import SearchResults from "./components/search/SearchResults";
import BookmarkPage from "./components/navbar/BookmarkPage";
import "./App.css";

const App = () => {
  const [prevScrollPos, setPrevScrollPos] = useState(0);
  const [isNavbarVisible, setIsNavbarVisible] = useState(true);
  const [bookmarks, setBookmarks] = useState([]);
  const [user, setUser] = useState("");

  useEffect(() => {
    const handleScroll = () => {
      const currScrollPos = window.scrollY;

      if (currScrollPos > prevScrollPos) {
        setIsNavbarVisible(false); // 스크롤 다운 시 숨기기
      } else {
        setIsNavbarVisible(true); // 스크롤 업 시 보이기
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
    <Router>
      <div>
        <nav
          className="navbar"
          style={{
            transform: isNavbarVisible ? "translateY(0%)" : "translateY(-105%)",
          }}>
          <div className="logo">
            <i className="fa-solid fa-font-awesome"></i>
            <Link to="/">LOGO</Link>
          </div>
          <div className="menu">
            <div className="menu-links">
              <Link to="/bookmarks">Bookmark</Link>
              <Link to="/login">Login</Link>
            </div>
            <Dropdown hideDropdown={hideDropdown} userRole={user}/>
          </div>
          <div className="menu-btn">
            <i className="fa-solid fa-bars"></i>
          </div>
        </nav>
        <MainContent
        bookmarks={bookmarks}
        removeBookmark={removeBookmark}
        addBookmark={addBookmark}
        user={user}
        />
      </div>
    </Router>
  );
};

const MainContent = ({ bookmarks, removeBookmark, addBookmark, user}) => {
  const location = useLocation();
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
          <Route path="/search-results" element={<SearchResults addBookmark={addBookmark} />} />
          <Route path="/login" element={<Login onClose={() => window.history.back()} />} />
          <Route path="/bookmarks" element={<BookmarkPage bookmarks={bookmarks} removeBookmark={removeBookmark} />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;