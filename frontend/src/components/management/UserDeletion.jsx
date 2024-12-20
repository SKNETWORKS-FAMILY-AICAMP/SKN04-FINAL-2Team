import React, { useState } from "react";
import "./UserDeletion.css";

const UserDeletion = ({ onClose }) => {
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

  // 사용자 삭제 처리
  const handleDelete = () => {
    if (!adminId || !adminPassword) {
      setError("관리자 ID와 비밀번호를 입력해주세요.");
      return;
    }

    if (user && isSelected) {
      // 실제 삭제 로직 구현
      console.log(`Deleting user: ${user.name}`);
      onClose();
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
    <div className="user-deletion-overlay">
      <div className="user-deletion-container">
        <button className="user-deletion-close-button" onClick={onClose}>×</button> {/* 엑스 버튼 */}
        <h2>회원 삭제</h2>
        <div className="user-deletion-form-group">
          <label htmlFor="search">사용자 검색</label>
          <input
            type="text"
            id="search"
            placeholder="사용자 ID 입력"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress} // 엔터 키로 검색 처리
            className={error && !user ? "error" : ""}
          />
          <button onClick={handleSearch} className="user-deletion-button">검색</button>
          {error && !user && <div className="user-deletion-error-message">{error}</div>}
        </div>
        {user && (
          <div className="user-info">
            <p>사용자: {user.name}</p>
            <label>
              <input
                type="checkbox"
                checked={isSelected}
                onChange={handleCheckboxChange}
              />
              삭제 확인
            </label>
          </div>
        )}
        <div className="user-deletion-form-group">
          <label htmlFor="admin-id">관리자 ID</label>
          <input
            type="text"
            id="admin-id"
            placeholder="관리자 ID 입력"
            value={adminId}
            onChange={(e) => setAdminId(e.target.value)}
            className={error && !adminId ? "error" : ""}
          />
          {error && !adminId && <div className="user-deletion-error-message">{error}</div>}
        </div>
        <div className="user-deletion-form-group">
          <label htmlFor="admin-password">관리자 비밀번호</label>
          <input
            type="password"
            id="admin-password"
            placeholder="관리자 비밀번호 입력"
            value={adminPassword}
            onChange={(e) => setAdminPassword(e.target.value)}
            className={error && !adminPassword ? "error" : ""}
          />
          {error && !adminPassword && <div className="user-deletion-error-message">{error}</div>}
        </div>
        <button onClick={handleDelete} className="user-deletion-button">삭제</button>
      </div>
    </div>
  );
};

export default UserDeletion;