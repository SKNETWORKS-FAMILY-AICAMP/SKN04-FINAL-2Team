import React, { useEffect, useState } from "react";
import axios from "axios";
import "./BookmarkPage.css"; // BookmarkPage.css 파일 임포트

const BookmarkPage = ({ user }) => {
  const [bookmarks, setBookmarks] = useState([]);

  // 북마크 목록 가져오기
  const fetchBookmarks = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/profile/bookmark/`);
      setBookmarks(response.data);
    } catch (error) {
      console.error('북마크 목록 가져오기 실패:', error);
    }
  };

  // 컴포넌트 마운트 시 북마크 목록 가져오기
  useEffect(() => {
    if (user) {  // 로그인된 경우에만 북마크 가져오기
      fetchBookmarks();
    }
  }, [user, bookmarks]);

  const removeBookmark = async (profile) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/profile/bookmark/remove/${profile.profile_id}/`
      );
      fetchBookmarks();  // 북마크 삭제 후 목록 새로고침
    } catch (error) {
      console.error('북마크 삭제 실패:', error.response?.data || error.message);
    }
  };

  const viewDetails = (profile) => {
    // 상세보기 기능 구현
    console.log("Viewing details for:", profile);
  };

  return (
    <div className="bookmark-page">
      {bookmarks.length === 0 ? (
        <p>No bookmarks yet.</p>
      ) : (
        bookmarks.map((profile, index) => (
          <div key={index} className="bookmark-resume-box-container">
            <div key={index} className="bookmark-resume-box">
              <div className="bookmark-resume-details">
                <p>
                  <strong>이름: </strong> {profile.name}
                  <strong>직군: </strong> {profile.job_category}
                  <strong>경력: </strong> {profile.career_year}
                </p>
                <div className="ai-analysis">
                  <p><strong>AI 분석 결과: </strong>{profile.ai_analysis}</p>
                </div>
              </div>
            </div>
            <div className="bookmark-resume-buttons">
              <button className="bookmark-button" onClick={() => removeBookmark(profile)}>삭제</button>
              <button className="details-button" onClick={() => viewDetails(profile)}>상세보기</button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default BookmarkPage;