let websocket = null;
let reconnectInterval = null;
let isConnecting = false;
let user_id = null;

const WEBSOCKET_URL = "ws://103.200.23.126:8000";
const RECONNECT_DELAY = 3000;


function handleMessage(event) {
    try {
        const data = JSON.parse(event.data);
        console.log("WebSocket message received:", data);
        
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
            case 'message':             
                break;
            case 'pong':
                console.log("Pong received:", data);
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
        websocket.send(JSON.stringify(data));
        return true;
    } else {
        console.warn("WebSocket is not connected. Message not sent:", data);
        return false;
    }
}

function connectWebSocket(user_id) {
    if (isConnecting || (websocket && websocket.readyState === WebSocket.CONNECTING)) {
        console.log("WebSocket is already connecting...");
        return;
    }

    if (websocket && websocket.readyState === WebSocket.OPEN) {
        console.log("WebSocket is already connected");
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
                console.error("WebSocket connection timeout");
            }
        }, 10000); // 10 giây timeout

        websocket.onopen = () => {
            clearTimeout(connectionTimeout);
            isConnecting = false;
            reconnectAttempts = 0;
            
            console.log("WebSocket connected successfully");
            
            // Gửi thông tin user_id
            const data = {
                type: "user",
                user_id: user_id,
                timestamp: new Date().toISOString()
            };
            
            websocket.send(JSON.stringify(data));
            console.log("User ID sent:", user_id);
            
            // Clear any existing reconnect interval
            if (reconnectInterval) {
                
                clearInterval(reconnectInterval);
                

                reconnectInterval = null;
            }
        };

        websocket.onmessage = handleMessage;

        websocket.onerror = (event) => {
            clearTimeout(connectionTimeout);
            console.log("WebSocket error:", event);
            isConnecting = false;
        };

        websocket.onclose = (event) => {
            clearTimeout(connectionTimeout);
            isConnecting = false;
            
            console.log(`WebSocket closed. Code: ${event.code}, Reason: ${event.reason}`);
            
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
function startHeartbeat() {
    setInterval(() => {
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            sendMessage({
                type: "ping",
                timestamp: new Date().toISOString()
            });
        }
    }, 30000);
}
