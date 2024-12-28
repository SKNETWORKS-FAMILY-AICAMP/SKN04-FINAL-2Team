import React, { useState } from "react";
import "./AdminPage.css";

const AdminPage = ({ onClose }) => {
  const [searchQuery, setSearchQuery] = useState(""); // 검색어 상태
  const [user, setUser] = useState(null); // 검색된 사용자 (단일 사용자)
  const [isSelected, setIsSelected] = useState(false); // 체크박스 선택 여부
  const [adminId, setAdminId] = useState(""); // 관리자 ID
  const [adminPassword, setAdminPassword] = useState(""); // 관리자 비밀번호
  const [error, setError] = useState(""); // 에러 메시지 상태

  // Mock 데이터 (실제 구현 시 API 호출로 대체)
  const mockUsers = [
    { id: "user1", name: "John Doe" },
    { id: "user2", name: "Jane Smith" },
    { id: "user3", name: "Alice Johnson" },
  ];

  // 검색어 변경 처리
  const handleSearch = () => {
    const foundUser = mockUsers.find(user => user.id === searchQuery);
    if (foundUser) {
      setUser(foundUser);
      setError("");
    } else {
      setUser(null);
      setError("사용자를 찾을 수 없습니다");
    }
  };

  // 체크박스 선택 처리
  const handleCheckboxChange = () => {
    setIsSelected(!isSelected);
  };

  // 권한 부여 처리
  const handleGrantRole = () => {
    if (!adminId || !adminPassword) {
      setError("관리자 ID와 비밀번호를 입력해주세요.");
      return;
    }

    if (user && isSelected) {
      // 실제 권한 부여 로직 구현
      console.log(`Granting role to user: ${user.name}`);
      setError("");
    } else {
      setError("사용자를 선택하고 확인란을 체크해주세요.");
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
        <h2 className="admin-page-header">사용자 권한 부여</h2>
        <input
          type="text"
          placeholder="사용자 ID 검색"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress} // 엔터 키로 검색 처리
          className="admin-page-input"
        />
        <button onClick={handleSearch} className="admin-page-button">검색</button>
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
          className="admin-page-input"
        />
        <input
          type="password"
          placeholder="관리자 비밀번호"
          value={adminPassword}
          onChange={(e) => setAdminPassword(e.target.value)}
          className="admin-page-input"
        />
        <button onClick={handleGrantRole} className="admin-page-button">권한 부여</button>
        {error && <div className="admin-page-error">{error}</div>}
      </div>
    </div>
  );
};

export default AdminPage;