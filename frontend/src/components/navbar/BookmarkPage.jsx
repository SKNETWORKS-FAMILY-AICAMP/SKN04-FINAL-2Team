import React from "react";
import "./BookmarkPage.css"; // BookmarkPage.css 파일 임포트

const BookmarkPage = ({ bookmarks, removeBookmark }) => {
  const viewDetails = (resume) => {
    // 상세보기 기능 구현
    console.log("Viewing details for:", resume);
  };

  return (
    <div className="bookmark-page">
      {bookmarks.length === 0 ? (
        <p>No bookmarks yet.</p>
      ) : (
        bookmarks.map((resume, index) => (
          <div key={index} className="bookmark-resume-box-container">
            <div key={index} className="bookmark-resume-box">
              <div className="bookmark-resume-details">
                <p><strong>이름: </strong> {resume.name} <strong>직군: </strong> {resume.occupation} <strong>경력: </strong> {resume.career}</p>
                <div className="ai-analysis">
                  <p><strong>AI 분석 결과: </strong></p>
                </div>
              </div>
            </div>
            <div className="bookmark-resume-buttons">
              <button className="bookmark-button" onClick={() => removeBookmark(resume)}>삭제</button>
              <button className="details-button" onClick={() => viewDetails(resume)}>상세보기</button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default BookmarkPage;