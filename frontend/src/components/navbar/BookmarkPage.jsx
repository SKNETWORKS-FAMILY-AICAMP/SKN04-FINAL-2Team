import React from "react";
import "./BookmarkPage.css"; // BookmarkPage.css 파일 임포트

const BookmarkPage = ({ bookmarks, removeBookmark }) => {
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