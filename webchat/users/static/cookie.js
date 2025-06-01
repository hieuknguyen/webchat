function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return JSON.parse(JSON.parse(decodeURIComponent(cookieValue).replace(/\\054/g, ',')).replace(/'/g, '"'));
        }
    }
    return null;
}