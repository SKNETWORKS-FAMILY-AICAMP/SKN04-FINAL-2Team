import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000/auth/';

const authService = {
    // ... existing code ...

    // 로그인
    login: async (username, password) => {
        try {
            const response = await axios.post(API_URL + 'login/', {
                username,
                password
            });
            
            if (response.data.access) {
                localStorage.setItem('user', JSON.stringify(response.data));
                return {
                    success: true,
                    data: response.data
                };
            }
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || '로그인에 실패했습니다.'
            };
        }
    },

    // 로그아웃
    logout: () => {
        localStorage.removeItem('user');
    },

    // 현재 사용자 정보 가져오기
    getCurrentUser: () => {
        return JSON.parse(localStorage.getItem('user'));
    },

    // ... existing code ...
};

export default authService;