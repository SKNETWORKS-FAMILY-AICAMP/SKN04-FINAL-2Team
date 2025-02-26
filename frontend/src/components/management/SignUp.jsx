import React, { useState } from "react";
import axiosInstance from "../../context/axiosInstance";
import "./SignUpForm.css";
import logo from "../../images/logo_v2.png";

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
      const response = await axiosInstance.post('/auth/register/', formData);

      console.log("회원가입 완료:", response.data);
      onClose();
    } catch (error) {
      if (error.response) {
        // 백엔드에서 반환한 에러 메시지 처리
        const serverErrors = error.response.data;
        let errorMessage = "회원가입 중 오류가 발생했습니다.";

        if (serverErrors.username) {
          errorMessage = `ID 오류: ${serverErrors.username.join(", ")}`;
        } else if (serverErrors.email) {
          errorMessage = `이메일 오류: ${serverErrors.email.join(", ")}`;
        }
        setError(errorMessage);
      } else {
        setError("서버 연결 중 오류가 발생했습니다.");
      }
      console.error("회원가입 오류:", error);
    }
};


  return (
    <div className="signup-overlay">
      <div className="signup-form-container">
        <button className="signup-close-button" onClick={onClose}>×</button> {/* 엑스 버튼 */}
        <div className="signup-top-bar">
          <img src={logo} alt="Logo" className="signup-logo-image" />
        </div>
        <form onSubmit={handleSubmit}>
          <div className="signup-form-inputs">
            {/* <label htmlFor="host-username">ID</label> */}
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
          <div className="signup-form-inputs">
            {/* <label htmlFor="host-password">Password</label> */}
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
          <div className="signup-form-inputs">
            {/* <label htmlFor="host-email">Email</label> */}
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
          <div className="signup-button-container">
            <button type="submit" className="signup-button">회원등록</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUp;