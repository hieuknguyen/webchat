function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();

        if (cookie.startsWith(name + '=')) {
            let cookieValue = cookie.substring(name.length + 1); 
            
            let decodedCookieValue; 

            try {
                decodedCookieValue = decodeURIComponent(cookieValue);
                console.log('1. Decoded cookieValue (with potential outer quotes):', decodedCookieValue);

                // Thêm bước này: Loại bỏ dấu nháy kép bao quanh bên ngoài nếu có
                if (decodedCookieValue.startsWith('"') && decodedCookieValue.endsWith('"')) {
                    decodedCookieValue = decodedCookieValue.slice(1, -1);
                    console.log('2. Decoded cookieValue (after outer quotes removed):', decodedCookieValue);
                } else {
                    console.log('2. No outer quotes found, decodedCookieValue remains:', decodedCookieValue);
                }

                // Bây giờ chuỗi đã sẵn sàng để JSON.parse
                const userObject = JSON.parse(decodedCookieValue);
                console.log('3. Successfully parsed user object:', userObject);

                return userObject;

            } catch (e) {
                console.error('Lỗi parse cookie:', e);
                console.error('Chuỗi gây lỗi (sau decodeURIComponent và loại bỏ quotes):', decodedCookieValue);
                return null;
            }
        }
    }
    return null;
}
function updateCookieField(cookieName, key, newValue, days = 7) {
    // Lấy dữ liệu hiện tại từ cookie, giả định getCookie đã được sửa để trả về đối tượng
    const currentData = getCookie(cookieName) || {};

    // Cập nhật trường dữ liệu mong muốn
    currentData[key] = newValue;

    // Chuyển đối tượng JavaScript thành chuỗi JSON
    // Không thêm dấu cách thừa bằng separators=(',', ':') nếu muốn chuỗi gọn nhất
    let jsonString = JSON.stringify(currentData);

    // **Bước quan trọng:** Mã hóa URL toàn bộ chuỗi JSON.
    // Điều này đảm bảo tất cả các ký tự đặc biệt (bao gồm cả dấu nháy kép, dấu phẩy, dấu hai chấm)
    // được mã hóa an toàn để lưu vào cookie.
    let encodedCookieValue = encodeURIComponent(jsonString);

    // Tạo ngày hết hạn cho cookie
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }

    // Ghi cookie. Giá trị đã được mã hóa URL.
    document.cookie = `${cookieName}=${encodedCookieValue}${expires}; path=/`;

    // Trả về chuỗi JSON gốc (chưa mã hóa URL) cho mục đích sử dụng ngay nếu cần
    // Nếu bạn muốn trả về chuỗi đã mã hóa URL, hãy trả về `encodedCookieValue`
    return jsonString; 
}


function parseCookieToJson(cookieString) {
    console.log("Chuỗi cookie ban đầu:", cookieString);
    if (typeof cookieString !== 'string' || cookieString.length === 0) {
        console.error("Đầu vào không hợp lệ: phải là một chuỗi không rỗng.");
        return null;
    }
    let processedString = cookieString;
    if (processedString.startsWith('"') && processedString.endsWith('"')) {
        processedString = processedString.slice(1, -1);
    }

    processedString = processedString.replace(/\\054/g, ',');
    try {
        const jsonObject = JSON.parse(processedString);
        return jsonObject;
    } catch (e) {
        console.error("Lỗi khi chuyển đổi chuỗi cookie sang JSON:", e);
        console.error("Chuỗi cookie sau khi xử lý gây lỗi:", processedString);
        return null;
    }
}