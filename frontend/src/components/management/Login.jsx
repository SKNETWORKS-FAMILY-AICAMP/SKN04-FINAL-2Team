import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "./authService";
import "./LoginForm.css";

const Login = ({ onClose }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [id.replace('host-', '')]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const result = await authService.login(formData.username, formData.password);
    
    if (result.success) {
      const userData = result.data;
      
      // 사용자 유형에 따른 리다이렉션
      if (userData.is_host) {
        navigate("/host");
      } else if (userData.is_superuser) {
        navigate("/admin");
      } else {
        navigate("/user");
      }
      
      onClose();
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="login-overlay">
      <div className="login-form-container">
        <h2>로그인</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="host-username">ID</label>
            <input
              type="text"
              id="host-username"
              placeholder="아이디 입력"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="host-password">Password</label>
            <input
              type="password"
              id="host-password"
              placeholder="비밀번호 입력"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit">로그인</button>
        </form>
        <button className="close-button" onClick={onClose}>
          닫기
        </button>
      </div>
    </div>
  );
};

export default Login;