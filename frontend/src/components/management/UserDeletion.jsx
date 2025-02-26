import React, { useState } from "react";
import axiosInstance from "../../context/axiosInstance";
import "./UserDeletion.css";
import logo from "../../images/logo_v2.png";

const UserDeletion = ({ onClose }) => {
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

  // 체크박스 선택 처리
  const handleCheckboxChange = () => {
    setIsSelected(!isSelected);
  };

  // 사용자 삭제 처리
  const handleDelete = async () => {
    if (!user) {
      setError("삭제할 사용자를 선택해주세요.");
      return;
    }

    try {
      const response = await axiosInstance.delete('auth/delete/', {
        data: { username: searchQuery }
      });

      if (response.status === 204) {
        setError("");
        setUser(null);
        setIsSelected(false);
        alert("사용자가 성공적으로 삭제되었습니다.");
        onClose();
      } else {
        setError("사용자 삭제 중 오류가 발생했습니다.");
      }
    } catch (error) {
      setError("사용자 삭제 중 오류가 발생했습니다.");
    }
  };

  // 엔터 키로 검색 처리
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="user-deletion-overlay">
      <div className="user-deletion-container">
        <button className="user-deletion-close-button" onClick={onClose}>×</button>
        <div className="user-deletion-top-bar">
          <img src={logo} alt="Logo" className="user-deletion-logo-image" />
        </div>
        <div className="user-deletion-form">
          <div className="user-deletion-inputs">
            <input
              type="text"
              placeholder="사용자 ID 검색"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress} 
              className="user-deletion-input"
            />
          </div>
          <div className="user-deletion-search-button-container">
            <button onClick={handleSearch} className="user-deletion-search-button">검색</button>
          </div>
        </div>
        {error && <p className="user-deletion-error-message" style={{ color: "red" }}>{error}</p>}
        {user && (
          <div className="user-deletion-checkbox">
            <input
              type="checkbox"
              checked={isSelected}
              onChange={handleCheckboxChange}
            />
            <p>사용자 이름: {user.username}</p>
          </div>
        )}
        <div className="user-deletion-button-container">
          <button onClick={handleDelete} className="user-deletion-button">삭제</button>
        </div>
      </div>
    </div>
  );
};

export default UserDeletion;