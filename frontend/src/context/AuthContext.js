import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        // localStorage에서 사용자 정보와 토큰을 가져옴
        const savedUser = localStorage.getItem('user');
        const token = localStorage.getItem('accessToken');
        return savedUser && token ? JSON.parse(savedUser) : null;
    });

    const login = (userData, tokens) => {
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('accessToken', tokens.access);
        localStorage.setItem('refreshToken', tokens.refresh);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    };

    // 토큰 유효성 검사
    useEffect(() => {
        const validateToken = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) return;

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
            });

            if (!response.ok) {
            // 토큰이 유효하지 않으면 로그아웃
            logout();
            }
        } catch (error) {
            console.error('Token validation error:', error);
        }
        };

        validateToken();
    }, []);

    const value = {
        user,
        login,
        logout
    };

    return (
        <AuthContext.Provider value={value}>
        {children}
        </AuthContext.Provider>
    );
    };

    export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth는 AuthProvider 내부에서만 사용할 수 있습니다');
    }
    return context;
};