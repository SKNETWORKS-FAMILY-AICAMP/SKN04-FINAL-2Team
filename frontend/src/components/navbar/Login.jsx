import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../context/AuthContext';
import "./LoginForm.css";

const Login = ({ onClose }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

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
  
    try {
      // AuthContext의 login 함수 사용
      const success = await login(formData.username, formData.password);
      
      if (success) {
        navigate("/");
        onClose();
      } else {
        setError("로그인에 실패했습니다.");
      }
    } catch (error) {
      console.error('Login error:', error);
      setError("로그인 처리 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="login-overlay">
      <div className="login-form-container">
        <button className="login-close-button" onClick={onClose}>×</button>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="login-form-group">
            <label htmlFor="host-username">ID</label>
            <input
              type="text"
              id="host-username"
              placeholder="아이디 입력"
              value={formData.username}
              onChange={handleChange}
              required
              className={error ? "error" : ""}
            />
          </div>
          <div className="login-form-group">
            <label htmlFor="host-password">Password</label>
            <input
              type="password"
              id="host-password"
              placeholder="비밀번호 입력"
              value={formData.password}
              onChange={handleChange}
              required
              className={error ? "error" : ""}
            />
          </div>
          {error && <div className="login-error-message">{error}</div>}
          <button type="submit" className="login-button">로그인</button>
        </form>
      </div>
    </div>
  );
};

export default Login;