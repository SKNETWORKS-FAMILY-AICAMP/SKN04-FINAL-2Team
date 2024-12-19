import React from "react";
import "./LoginForm.css";

const HostLogin = ({ onClose }) => {
  return (
    <div className="login-overlay">
      <div className="login-form-container">
        <h2>로그인</h2>
        <form>
          <div className="form-group">
            <label htmlFor="host-username">ID</label>
            <input type="text" id="host-username" placeholder="Host 아이디 입력" />
          </div>
          <div className="form-group">
            <label htmlFor="host-password">password</label>
            <input type="password" id="host-password" placeholder="Host 비밀번호 입력" />
          </div>
          <button type="submit">Login</button>
        </form>
        <button className="close-button" onClick={onClose}>
          닫기
        </button>
      </div>
    </div>
  );
};

export default HostLogin;