let websocket = null;
let reconnectInterval = null;
let isConnecting = false;
let user_id = null;

let lastActivity = Date.now();
let connectionCheckInterval = null;
let isPageVisible = true;

const WEBSOCKET_URL = "ws://103.200.23.126:9000";
const RECONNECT_DELAY = 3000;




function handleMessage(event) {
    try {
        const data = JSON.parse(event.data);
     
        
        
        // Xử lý các loại message khác nhau
        switch(data.type) {
            case 'friend_status':
                console.log("Friend status update:", data.friend, data.status);
                break;
            case 'error':
                console.error("Server error:", data);
                break;
            case 'welcome':
                console.log("Welcome message:", data);
                break;
            case 'connected':
                console.log("Connected message:", data);
                break;
            
        }
        
        // Reset reconnect attempts khi nhận được message thành công
        reconnectAttempts = 0;
        
    } catch (error) {
        console.error("Error parsing WebSocket message:", error);
        console.log("Raw message:", event.data);
    }
}


function sendMessage(data) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        // Nếu là ping message, ghi lại thời gian
        if (data.type === 'ping') {
            pingStartTime = Date.now();
        }
        
        websocket.send(JSON.stringify(data));
        return true;
    } else {
        console.warn("WebSocket is not connected. Message not sent:", data);
        return false;
    }
}

function connectWebSocket(user_id) {
    if (isConnecting || (websocket && websocket.readyState === WebSocket.CONNECTING)) {
        return;
    }

    if (websocket && websocket.readyState === WebSocket.OPEN) {
        return;
    }

    isConnecting = true;
    

    try {
        console.log(`Attempting to connect to WebSocket... `);
        websocket = new WebSocket(WEBSOCKET_URL);

        // Thiết lập timeout cho kết nối
        const connectionTimeout = setTimeout(() => {
            if (websocket.readyState === WebSocket.CONNECTING) {
                websocket.close();
            }
        }, 10000); // 10 giây timeout

        websocket.onopen = () => {
            clearTimeout(connectionTimeout);
            isConnecting = false;
            reconnectAttempts = 0;
            
        
            
            // Gửi thông tin user_id
            const data = {
                type: "user",
                user_id: user_id,
                timestamp: new Date().toISOString()
            };
            
            websocket.send(JSON.stringify(data));
           
            
            // Clear any existing reconnect interval
            if (reconnectInterval) {
                
                clearInterval(reconnectInterval);
                

                reconnectInterval = null;
            }
        };

        websocket.onmessage = function(event) {
    received_message(event);  
    handleMessage(event);    
};

        websocket.onerror = (event) => {
            clearTimeout(connectionTimeout);
            console.log("WebSocket error:", event);
            isConnecting = false;
        };

        websocket.onclose = (event) => {
            clearTimeout(connectionTimeout);
            isConnecting = false;
            
       
            
            // Chỉ reconnect nếu không phải do user chủ động đóng
            if (event.code !== 1000 ) {
                scheduleReconnect();
            }
        };

    } catch (error) {
        console.error("Exception in connectWebSocket:", error);
        isConnecting = false;
        scheduleReconnect();
    }
}
// hàm tự động kết nối lại nếu mất kết nối
function scheduleReconnect() {
    if (reconnectInterval) {
        // Nếu đã có interval đang chạy, không cần tạo mới
        return;
    }
    reconnectInterval = setTimeout(() => {
        reconnectInterval = null;
        if (user_id) {
            connectWebSocket(user_id);
        }
    }, RECONNECT_DELAY);
}

// hàm đóng kêt nối WebSocket
function disconnectWebSocket() {
    if (reconnectInterval) {
        clearInterval(reconnectInterval);
        reconnectInterval = null;
    }
    
    if (websocket) {
        websocket.close(1000, "User initiated disconnect");
        websocket = null;
    }
    
    
    isConnecting = false;
    console.log("WebSocket disconnected by user");
}

// Kiểm tra trạng thái kết nối
function getConnectionStatus() {
    if (!websocket) return "disconnected";
    
    switch(websocket.readyState) {
        case WebSocket.CONNECTING: return "connecting";
        case WebSocket.OPEN: return "connected";
        case WebSocket.CLOSING: return "closing";
        case WebSocket.CLOSED: return "closed";
        default: return "unknown";
    }
}

// Heartbeat để duy trì kết nối
// function startHeartbeat() {
//     // Clear existing intervals
//     if (connectionCheckInterval) {
//         clearInterval(connectionCheckInterval);
//     }
    
//     connectionCheckInterval = setInterval(() => {
//         detectWakeup();
        
//         if (websocket && websocket.readyState === WebSocket.OPEN) {
//             // Gửi ping để đo độ trễ
//             sendMessage({
//                 type: "ping",
//                 timestamp: new Date().toISOString()
//             });
//         } else if (isPageVisible) {
//             // Nếu page visible nhưng websocket không connected
//             checkAndReconnectIfNeeded();
//         }
//     }, 15000); // Ping mỗi 15 giây
// }

// Thêm event listeners để detect page visibility


// Detect khi máy wake up từ sleep
let lastHeartbeat = Date.now();
function detectWakeup() {
    const now = Date.now();
    if (now - lastHeartbeat > 35000) { // Nếu > 35s không có heartbeat
        console.log('System wakeup detected, reconnecting...');
        forceReconnect();
    }
    lastHeartbeat = now;
}

// Kiểm tra kết nối thực sự
// async function checkRealConnection() {
//     if (!websocket || websocket.readyState !== WebSocket.OPEN) {
//         return false;
//     }
    
//     return new Promise((resolve) => {
//         const startTime = Date.now();
//         const timeout = setTimeout(() => {
//             lastPingTime = null; // Ping timeout
//             resolve(false);
//         }, 10000); // 10s timeout
        
//         const originalOnMessage = websocket.onmessage;
        
//         websocket.onmessage = (event) => {
//             const data = JSON.parse(event.data);
//             if (data.type === 'pong') {
//                 clearTimeout(timeout);
//                 websocket.onmessage = originalOnMessage;
                
//                 // Tính ping time
//                 const pingTime = Date.now() - startTime;
//                 lastPingTime = pingTime;
                
//                 // Cập nhật lịch sử
//                 pingHistory.push(pingTime);
//                 if (pingHistory.length > 10) {
//                     pingHistory.shift();
//                 }
//                 averagePing = Math.round(pingHistory.reduce((a, b) => a + b, 0) / pingHistory.length);
                
//                 resolve(true);
//             } else {
//                 originalOnMessage(event);
//             }
//         };
        
//         // Gửi ping test
//         pingStartTime = Date.now();
//         sendMessage({
//             type: "ping",
//             timestamp: new Date().toISOString()
//         });
//     });
// }
// Force reconnect
function forceReconnect() {

    
    // Reset ping data
    lastPingTime = null;
    pingHistory = [];
    averagePing = 0;
    pingStartTime = 0;
    
    if (websocket) {
        websocket.close();
        websocket = null;
    }
    
    isConnecting = false;
    
    const user = getCookie('user');
    if (user && user.user_id) {
        setTimeout(() => {
            connectWebSocket(parseInt(user.user_id));
        }, 1000);
    }
}
// Kiểm tra và reconnect nếu cần
async function checkAndReconnectIfNeeded() {
    if (!isPageVisible) return;
    
    
    
    if (!isReallyConnected) {
        forceReconnect();
    }
}

setInterval(() => {
    sendMessage({
                type: "ping",
                timestamp: new Date().toISOString()
            });
}, 1000);
