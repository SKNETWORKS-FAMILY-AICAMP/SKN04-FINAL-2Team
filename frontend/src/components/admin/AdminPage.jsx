import React, { useState } from "react";
import axiosInstance from "../../context/axiosInstance";
import "./AdminPage.css";
import logo from "../../images/logo_v2.png";

const AdminPage = ({ onClose }) => {
  const [searchQuery, setSearchQuery] = useState(""); // 검색어 상태
  const [user, setUser] = useState(null); // 검색된 사용자 (단일 사용자)
  const [isSelected, setIsSelected] = useState(false); // 체크박스 선택 여부
  const [error, setError] = useState(""); // 에러 메시지 상태

  // 검색어 변경 처리
  const handleSearch = async () => {
    try {
      const response = await axiosInstance.get(`auth/users/${searchQuery}`);
      if (response.status === 200 && response.data.username) {
        setUser(response.data);
        setError("");
      } else {
        setUser(null);
        setError("사용자를 찾을 수 없습니다");
      }
    } catch (error) {
      setUser(null);
      setError("사용자를 찾을 수 없습니다");
    }
  };

  // 엔터 키로 검색 처리
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };


  // 체크박스 선택 처리
  const handleCheckboxChange = () => {
    setIsSelected(!isSelected);
  };

  // 권한 부여 처리
  const handleGrantRole = async () => {
    if (!user) {
      setError("권한을 부여할 사용자를 선택해주세요.");
      return;
    }

    try {
      const response = await axiosInstance.patch(`/auth/grant-role/${searchQuery}/`, {
        username: searchQuery
      });

      if (response.status === 200) {
        setError("");
        setUser(null);
        setIsSelected(false);
        alert("사용자에게 권한이 성공적으로 부여되었습니다.");
        onClose();
      } else {
        setError(response.data.message || "사용자 권한 부여 중 오류가 발생했습니다.");
      }
    } catch (error) {
      setError(error.response?.data?.message || "사용자 권한 부여 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="admin-page-overlay">
      <div className="admin-page-container">
        <button className="admin-close-button" onClick={onClose}>×</button>
        <div className="admin-top-bar">
          <img src={logo} alt="Logo" className="admin-logo-image" />
        </div>
        <div className="admin-page-form">
          <div className="admin-page-inputs">
            <input
              type="text"
              placeholder="사용자 ID 검색"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress} 
              className="admin-page-input"
            />
          </div>
          <div className="admin-search-button-container">
            <button onClick={handleSearch} className="admin-search-button">검색</button>
          </div>
        </div>
        {error && <p className="admin-page-error-message" style={{ color: "red" }}>{error}</p>}
        {user && (
          <div className="admin-user-checkbox">
            <input
              type="checkbox"
              checked={isSelected}
              onChange={handleCheckboxChange}
            />
            <p>사용자 이름: {user.username}</p>
          </div>
        )}
        <div className="admin-button-container">
          <button onClick={handleGrantRole} className="admin-button">권한 부여</button>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;