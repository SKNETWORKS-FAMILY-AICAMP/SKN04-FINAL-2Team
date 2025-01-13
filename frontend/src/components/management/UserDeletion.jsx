import React, { useState } from "react";
import axiosInstance from "../../context/axiosInstance";
import "./UserDeletion.css";

const UserDeletion = ({ onClose }) => {
  const [searchQuery, setSearchQuery] = useState(""); // 검색어 상태
  const [user, setUser] = useState(null); // 검색된 사용자 (단일 사용자)
  const [isSelected, setIsSelected] = useState(false); // 체크박스 선택 여부
  const [adminId, setAdminId] = useState(""); // 관리자 ID
  const [adminPassword, setAdminPassword] = useState(""); // 관리자 비밀번호
  const [error, setError] = useState(""); // 에러 메시지 상태

  // 검색어 변경 처리
  const handleSearch = async () => {
    try {
      const response = await axiosInstance.get(`/users/${searchQuery}`);
      if (response.status === 200) {
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
    if (!adminId || !adminPassword) {
      setError("관리자 ID와 비밀번호를 입력해주세요.");
      return;
    }

    if (!user) {
      setError("삭제할 사용자를 선택해주세요.");
      return;
    }

    try {
      const response = await axiosInstance.delete(`/users/${user.id}`, {
        data: { adminId, adminPassword }
      });

      if (response.status === 200) {
        setError("");
        setUser(null);
        setIsSelected(false);
        alert("사용자가 성공적으로 삭제되었습니다.");
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
        <button className="user-deletion-close-button" onClick={onClose}>×</button> {/* 엑스 버튼 */}
        <h2>사용자 삭제</h2>
        <input
          type="text"
          placeholder="사용자 ID 검색"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress} // 엔터 키로 검색 처리
          className="user-deletion-input"
        />
        <button onClick={handleSearch} className="user-deletion-button">검색</button>
        {user && (
          <div className="user-box">
            <input
              type="checkbox"
              checked={isSelected}
              onChange={handleCheckboxChange}
              className="user-checkbox"
            />
            <div className="user-info">
              <p>{user.name}</p>
            </div>
          </div>
        )}
        <input
          type="text"
          placeholder="관리자 ID"
          value={adminId}
          onChange={(e) => setAdminId(e.target.value)}
          className="user-deletion-input"
        />
        <input
          type="password"
          placeholder="관리자 비밀번호"
          value={adminPassword}
          onChange={(e) => setAdminPassword(e.target.value)}
          className="user-deletion-input"
        />
        <button onClick={handleDelete} className="user-deletion-button">삭제</button>
        {error && <div className="user-deletion-error-message">{error}</div>}
      </div>
    </div>
  );
};

export default UserDeletion;