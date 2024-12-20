import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from "react-router-dom";
import "./App.css";
import Dropdown from "./components/dropdown/Dropdown";
import UserManagement from "./components/management/UserManagement";
import AdminPage from "./components/admin/AdminPage";
import Sidebar from "./components/sidebar/Sidebar";
import MainSearch from "./components/search/MainSearch"; // MainSearch 컴포넌트 임포트
import SearchResults from "./components/search/SearchResults"; // SearchResults 컴포넌트 임포트

const App = () => {
  const [prevScrollPos, setPrevScrollPos] = useState(0);
  const [isNavbarVisible, setIsNavbarVisible] = useState(true);

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

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [prevScrollPos]);

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
              <a href="#">History</a>
            </div>
            <Dropdown />
          </div>
          <div className="menu-btn">
            <i className="fa-solid fa-bars"></i>
          </div>
        </nav>
        <MainContent />
      </div>
    </Router>
  );
};

const MainContent = () => {
  const location = useLocation();
  const showSidebar = location.pathname !== "/" && location.pathname !== "/search-results";

  return (
    <div style={{ display: "flex" }}>
      {showSidebar && <Sidebar />}
      <div style={{ flex: 1, padding: "20px" }}>
        <Routes>
          <Route path="/user-management" element={<UserManagement />} />
          <Route path="/admin-page" element={<AdminPage />} />
          <Route path="/" element={<MainSearch />} /> {/* MainSearch 컴포넌트 사용 */}
          <Route path="/search-results" element={<SearchResults />} /> {/* SearchResults 컴포넌트 추가 */}
        </Routes>
      </div>
    </div>
  );
};

export default App;