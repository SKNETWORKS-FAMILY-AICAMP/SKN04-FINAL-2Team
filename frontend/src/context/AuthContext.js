import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { useCookies } from 'react-cookie';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [cookies, setCookie, removeCookie] = useCookies(['accessToken', 'refreshToken']);

    const login = (userData, tokens) => {
        setUser(userData);
        setCookie('accessToken', tokens.access, { path: '/' });
        setCookie('refreshToken', tokens.refresh, { path: '/' });
    };

    const logout = useCallback(() => {
        setUser(null);
        removeCookie('accessToken');
        removeCookie('refreshToken');
    }, [removeCookie]);

    useEffect(() => {
        const validateToken = async () => {
            const token = cookies.accessToken;
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
                    logout();
                }
            } catch (error) {
                console.error('Token validation error:', error);
                logout();
            }
        };

        validateToken();
    }, [cookies.accessToken, logout]);

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