import React, { useState } from "react";
import "./Sidebar.css";
import UserDeletion from "../management/UserDeletion"; // 회원삭제 컴포넌트
import SignUp from "../management/SignUp"; // 회원가입 컴포넌트
import AdminPage from "../admin/AdminPage"; // AdminPage 임포트
import { useAuth } from '../../context/AuthContext'; // useAuth 임포트
import adminIcon from "../../images/manage_icon.png"; // 관리자 아이콘 이미지
import manageIcon from "../../images/member_icon.png"; // 회원관리 아이콘 이미지

const Sidebar = () => {
  const [isDeletingUser, setIsDeletingUser] = useState(false); // 회원삭제 모달 상태
  const [showSignUp, setShowSignUp] = useState(false); // 회원가입 폼 표시 상태
  const [isUserManagementOpen, setIsUserManagementOpen] = useState(false); // 회원관리 드롭다운 상태
  const [showAdminPage, setShowAdminPage] = useState(false); // 관리 페이지 상태 추가
  const { user } = useAuth(); // useAuth 훅 사용

  const handleSignUpClick = () => {
    setShowSignUp(true); // 회원가입 폼 표시
  };

  const handleAdminPageClick = () => {
    if (user && (user.is_superuser || user.is_staff)) {
      setShowAdminPage(true); // 관리 페이지 표시
    } else {
      alert("해당 기능은 관리자만 접속이 가능합니다.");
    }
  };

  const toggleUserManagement = () => {
    setIsUserManagementOpen(!isUserManagementOpen);
  };

  return (
    <>
      <aside className="sidebar">
        <header>
          <h1>Settings</h1>
        </header>
          <div className="admin-container">
            <img src={adminIcon} alt="Icon" className="admin-icon" />
            <h3> <button className="admin-form" onClick={handleAdminPageClick}>관리페이지</button> </h3>
          </div>
          <div className="user-management-container" onClick={toggleUserManagement}>
            <img src={manageIcon} alt="Icon" className="member-icon" />
            <h3>회원관리</h3>
            <p> <li onClick={handleSignUpClick}>회원등록</li> </p>
            <p> <li onClick={() => setIsDeletingUser(true)}>회원삭제</li> </p>
          </div>
      </aside>

      {/* 관리 페이지 모달 표시 */}
      {showAdminPage && (
        <div className="admin-page-overlay">
          <AdminPage onClose={() => setShowAdminPage(false)} />
        </div>
      )}

      {/* 회원삭제 모달 표시 */}
      {isDeletingUser && (
        <div className="user-deletion-overlay">
          <UserDeletion onClose={() => setIsDeletingUser(false)} />
        </div>
      )}

      {/* 회원가입 모달 표시 */}
      {showSignUp && (
        <div className="login-overlay">
          <SignUp onClose={() => setShowSignUp(false)} />
        </div>
      )}
    </>
  );
};

export default Sidebar;