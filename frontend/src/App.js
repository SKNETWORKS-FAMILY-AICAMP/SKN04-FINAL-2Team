import React, { useEffect, useState } from "react";
import "./App.css";
import Dropdown from "./components/dropdown/Dropdown";

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
    <div>
      <nav
        className="navbar"
        style={{
          transform: isNavbarVisible ? "translateY(0%)" : "translateY(-105%)",
        }}>
        <div className="logo">
          <i className="fa-solid fa-font-awesome"></i>
          <a href="#">LOGO</a>
        </div>
        <div className="menu">
          <div className="menu-links">
            <a href="#">Home</a>
            <a href="#">History</a>
          </div>
          <Dropdown />
        </div>
        <div className="menu-btn">
          <i className="fa-solid fa-bars"></i>
        </div>
      </nav>
    </div>
  );
};

export default App;