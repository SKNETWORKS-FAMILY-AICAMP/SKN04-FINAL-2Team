import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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
    setFormData((prev) => ({
      ...prev,
      [id.replace("host-", "")]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // 입력값 검증
    if (!formData.username || !formData.password) {
      setError("아이디와 비밀번호를 모두 입력해주세요.");
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "로그인에 실패했습니다.");
        return;
      }

      // 로그인 성공 처리
      if (data.token) {
        // JWT 토큰 저장
        localStorage.setItem('accessToken', data.token.access);
        localStorage.setItem('refreshToken', data.token.refresh);
        
        // 사용자 정보 저장
        if (data.user) {
          localStorage.setItem('user', JSON.stringify(data.user));
        }

        // 메인 검색 페이지로 이동
        navigate("/");
        onClose();
      } else {
        setError("로그인 처리 중 오류가 발생했습니다.");
      }
    } catch (error) {
      console.error('Login error:', error);
      setError("서버 연결 중 오류가 발생했습니다.");
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