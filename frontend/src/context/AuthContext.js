import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axiosInstance from './axiosInstance';
import { getCookie, setCookie, removeCookie } from './cookieUtils';

/** ✅ AuthContext 생성 */
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    /** ✅ 상태 관리 */
    const [user, setUser] = useState(() => {
        // 초기 상태를 localStorage에서 가져옴
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : null;
    });
    const [isRefreshing, setIsRefreshing] = useState(false);

    /** ✅ 쿠키 기본 옵션 */
    const cookieOptions = {
        path: '/',
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'Lax'
    };

    /** ✅ 토큰 저장 함수 */
    const saveTokens = useCallback((access, refresh) => {
        // Access Token 저장 (1시간)
        setCookie('accessToken', access, {
            ...cookieOptions,
            maxAge: 3600
        });
        
        // Refresh Token 저장 (24시간)
        setCookie('refreshToken', refresh, {
            ...cookieOptions,
            maxAge: 24 * 3600
        });

        // axios 기본 헤더에 토큰 설정
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    }, [cookieOptions]);

    /** ✅ 로그아웃 함수 */
    const logout = useCallback(() => {
        // 쿠키에서 토큰 제거
        removeCookie('accessToken');
        removeCookie('refreshToken');
        
        // localStorage에서 사용자 정보 제거
        localStorage.removeItem('user');
        
        // axios 헤더에서 토큰 제거
        delete axiosInstance.defaults.headers.common['Authorization'];
        
        // 상태 초기화
        setUser(null);
        console.log('✅ 로그아웃 완료');
    }, []);

    /** ✅ Access Token 갱신 함수 */
    const refreshAccessToken = useCallback(async () => {
        if (isRefreshing) return null;
        
        try {
            setIsRefreshing(true);
            const refreshToken = getCookie('refreshToken');
            
            if (!refreshToken) {
                console.warn('❌ Refresh Token 없음');
                logout();
                return null;
            }

            const response = await axiosInstance.post('/auth/refresh/', {
                refresh: refreshToken
            });

            const { access } = response.data;
            setCookie('accessToken', access, {
                ...cookieOptions,
                maxAge: 3600
            });

            // axios 기본 헤더 업데이트
            axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access}`;

            console.log('✅ Access Token 갱신 성공');
            return access;
        } catch (error) {
            console.error('🚨 Refresh Token 오류:', error);
            logout();
            return null;
        } finally {
            setIsRefreshing(false);
        }
    }, [isRefreshing, cookieOptions, logout]);

    /** ✅ 로그인 함수 */
    const login = useCallback(async (username, password) => {
        try {
            const response = await axiosInstance.post('/auth/login/', { 
                username, 
                password 
            });
        
            if (response.data.success && response.data.token) {
                const { access, refresh } = response.data.token;
                saveTokens(access, refresh);
                
                // 사용자 정보 저장
                setUser(response.data.user);
                localStorage.setItem('user', JSON.stringify(response.data.user));
                
                console.log('✅ 로그인 성공, 토큰 저장됨');
                return true;
            }
            return false;
        } catch (error) {
            console.error('🚨 로그인 실패:', error);
            return false;
        }
    }, [saveTokens]);

    /** ✅ axios 인터셉터 설정 */
    useEffect(() => {
        // 요청 인터셉터
        const requestInterceptor = axiosInstance.interceptors.request.use(
            (config) => {
                const accessToken = getCookie('accessToken');
                if (accessToken) {
                    config.headers.Authorization = `Bearer ${accessToken}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        // 응답 인터셉터
        const responseInterceptor = axiosInstance.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;

                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    const newAccessToken = await refreshAccessToken();
                    
                    if (newAccessToken) {
                        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                        return axiosInstance(originalRequest);
                    }
                }
                return Promise.reject(error);
            }
        );

        // 클린업 함수
        return () => {
            axiosInstance.interceptors.request.eject(requestInterceptor);
            axiosInstance.interceptors.response.eject(responseInterceptor);
        };
    }, [refreshAccessToken]);

    /** ✅ 초기 인증 상태 확인 */
    useEffect(() => {
        const initAuth = async () => {
            const accessToken = getCookie('accessToken');
            if (accessToken) {
                // 저장된 토큰이 있으면 axios 헤더에 설정
                axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
                
                // 저장된 사용자 정보 복원
                const savedUser = localStorage.getItem('user');
                if (savedUser) {
                    setUser(JSON.parse(savedUser));
                }
            } else {
                logout();
            }
        };

        initAuth();
    }, [logout]);

    /** ✅ Context Provider 값 설정 */
    const value = {
        user,
        login,
        logout,
        refreshAccessToken
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

/** ✅ Custom Hook */
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export default AuthContext;