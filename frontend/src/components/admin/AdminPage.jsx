import React, { useState } from "react";
import axiosInstance from "../../context/axiosInstance";
import "./AdminPage.css";

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


  // 체크박스 선택 처리
  const handleCheckboxChange = () => {
    setIsSelected(!isSelected);
  };

  // 권한 부여 처리
  const handleGrantRole = async () => {
    if (!user) {
      setError("삭제할 사용자를 선택해주세요.");
      return;
    }

    try {
      const response = await axiosInstance.authorize(`/auth/update`, {
        data: { username: searchQuery }
      });

      if (response.status === 200) {
        setError("");
        setUser(null);
        setIsSelected(false);
        alert("사용자가 성공적으로 삭제되었습니다.");
      } else {
        setError(response.data.message || "사용자 삭제 중 오류가 발생했습니다.");
      }
    } catch (error) {
      setError(error.response?.data?.message || "사용자 삭제 중 오류가 발생했습니다.");
    }
  };

  // 엔터 키로 검색 처리
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="admin-page-overlay">
      <div className="admin-page-container">
        <button className="admin-page-close-button" onClick={onClose}>×</button> {/* 엑스 버튼 */}
        <h2 className="admin-page-header">권리자 권한 부여</h2>
        <input
          type="text"
          placeholder="사용자 ID 검색"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress} // 엔터 키로 검색 처리
          className="admin-page-input"
        />
        <button onClick={handleSearch} className="admin-page-button">검색</button>
        {error && <div className="admin-page-error">{error}</div>}
        {user && (
          <div className="user-box">
            <div>
              <p>사용자 이름: {user.username}</p>
            <input
              type="checkbox"
              checked={isSelected}
              onChange={handleCheckboxChange}
              className="user-checkbox"
            />
            <label>사용자 선택</label>
            </div>
          </div>
        )}
        <p>
          <button onClick={handleGrantRole} className="admin-page-button">권한 부여</button>
        </p>
      </div>
    </div>
  );
};

export default AdminPage;