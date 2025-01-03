/** ✅ 쿠키 유틸리티 함수 */
/** 모든 쿠키 가져오기 */
export const getAllCookies = () => {
    return document.cookie
        .split('; ')
        .reduce((cookies, cookie) => {
            const [name, value] = cookie.split('=');
            cookies[name] = decodeURIComponent(value);
            return cookies;
        }, {});
};

/** 특정 쿠키 가져오기 */
export const getCookie = (name) => {
    return document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`))
        ?.split('=')[1];
};

/** 쿠키 설정 */
export const setCookie = (name, value, options = {}) => {
    const defaultOptions = {
        path: '/',
        sameSite: 'Lax',
        secure: window.location.protocol === 'https:',
        maxAge: 3600, // 1시간
    };

    const finalOptions = { ...defaultOptions, ...options };

    let cookieString = `${name}=${encodeURIComponent(value)}`;
    if (finalOptions.maxAge) {
        cookieString += `; max-age=${finalOptions.maxAge}`;
    }
    if (finalOptions.expires) {
        cookieString += `; expires=${finalOptions.expires.toUTCString()}`;
    }
    cookieString += `; path=${finalOptions.path}`;
    cookieString += `; sameSite=${finalOptions.sameSite}`;
    if (finalOptions.secure) {
        cookieString += '; secure';
    }
    document.cookie = cookieString;
};

/** 쿠키 삭제 */
export const removeCookie = (name) => {
    document.cookie = `${name}=; path=/; max-age=0;`;
};
