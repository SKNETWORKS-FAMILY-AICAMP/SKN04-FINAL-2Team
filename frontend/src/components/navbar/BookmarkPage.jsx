import React, { useEffect, useState } from "react";
import axiosInstance from '../../context/axiosInstance';
import "./BookmarkPage.css"; // BookmarkPage.css 파일 임포트

const BookmarkPage = ({ user }) => {
  const [bookmarks, setBookmarks] = useState([]);

  // 북마크 목록 가져오기
  const fetchBookmarks = async () => {
    try {
      const response = await axiosInstance.get(`/profile/bookmark/`);
      setBookmarks(response.data.bookmarks || []);
    } catch (error) {
      console.error('북마크 목록 가져오기 실패:', error);
      setBookmarks([]);
    }
  };

  // 컴포넌트 마운트 시 북마크 목록 가져오기
  useEffect(() => {
    if (user) {  // 로그인된 경우에만 북마크 가져오기
      fetchBookmarks();
    }
  }, [user]);

  const removeBookmark = async (profile) => {
    try {
      await axiosInstance.delete(
        `/profile/bookmark/remove/${profile.profile_id}/`
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
        <p className="no-bookmarks">저장된 북마크가 없습니다.</p>
      ) : (
        <div className="bookmark-list-content">
          {bookmarks.map((profile) => (
            <div key={profile.profile_id} className="bookmark-resume-box-container">
              <div className="bookmark-resume-box">
                <div className="bookmark-resume-details">
                  <p>
                    <strong>이름: </strong> {profile.name}
                    <strong>직군: </strong> {profile.job_category}
                    <strong>경력: </strong> {profile.career_year}년
                  </p>
                  <div className="ai-analysis">
                    <p><strong>AI 분석 결과: </strong>{profile.ai_analysis}</p>
                  </div>
                </div>
              </div>
                <div className="bookmark-resume-buttons">
                  <button 
                    className="bookmark-bookmark-button" 
                    onClick={() => removeBookmark(profile)}
                  >
                    북마크 삭제
                  </button>
                  <button 
                    className="bookmark-details-button" 
                    onClick={() => {
                      viewDetails(profile);
                      if (profile.pdf_url) {
                        window.open(profile.pdf_url, '_blank', 'noopener noreferrer');
                      }
                    }}
                  >
                    상세보기
                  </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BookmarkPage;