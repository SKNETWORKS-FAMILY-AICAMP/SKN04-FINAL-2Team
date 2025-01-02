import React, { useState } from "react";
import "./SignUpForm.css";

const SignUp = ({ onClose }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
  });
  const [error, setError] = useState("");

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

    if (!formData.username || !formData.password || !formData.email) {
      setError("모든 필드를 입력해주세요.");
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "회원가입 중 오류가 발생했습니다.");
        return;
      }

      console.log("회원가입 완료:", data);
      onClose();
    } catch (error) {
      setError("서버 연결 중 오류가 발생했습니다.");
      console.error("회원가입 오류:", error);
    }
  };

  return (
    <div className="signup-overlay">
      <div className="signup-form-container">
        <button className="signup-close-button" onClick={onClose}>×</button> {/* 엑스 버튼 */}
        <h2>Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="signup-form-group">
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
          <div className="signup-form-group">
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
          <div className="signup-form-group">
            <label htmlFor="host-email">Email</label>
            <input
              type="email"
              id="host-email"
              placeholder="이메일 입력"
              value={formData.email}
              onChange={handleChange}
              required
              className={error ? "error" : ""}
            />
          </div>
          {error && <div className="signup-error-message">{error}</div>}
          <button type="submit" className="signup-button">회원등록</button>
        </form>
      </div>
    </div>
  );
};

export default SignUp;