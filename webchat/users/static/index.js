function close_login(){
    var elements = document.getElementsByClassName("wrapper");
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
    }
}
function open_login(){
    var elements = document.getElementsByClassName("wrapper");
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.display = "flex";
    }
}

function open_user(){
    var elements = document.getElementsByClassName("wrapper")[0];
    elements.style.display = "flex";
    var login = document.getElementsByClassName("form-box login")[0];
    var user = document.getElementsByClassName("form-box user")[0];
    login.style.display = "none";
    user.style.display = "block";
    var chat = document.getElementsByClassName("chat")[0];
    chat.style.display = "none";
}
function logout() {
    window.location.href = "logout.php";
}

var lock = true;
function hidden_show() {
    
    var password = document.getElementById("input_password");
    var icon = document.getElementById("locks");
    var icon1 = document.getElementById("show");
    if (password.value === "") {
        lock = false;
    }
    if (lock) {
        icon.style.display = "none";
        icon1.style.display = "inline-block";
        password.setAttribute('type', 'text');
        lock = false;
    }
    else {
        icon.style.display = "inline-block";
        icon1.style.display = "none";
        password.setAttribute('type', 'password');
        lock = true;
    }
}
function dangki(){
    var login = document.getElementsByClassName("form-box login")[0];
    var register = document.getElementsByClassName("form-box register")[0];
    login.style.display = "none";
    register.style.display = "block";
}
function dangnhap(){
    var login = document.getElementsByClassName("form-box login")[0];
    var register = document.getElementsByClassName("form-box register")[0];
    login.style.display = "block";
    register.style.display = "none";
}
function chat(){
    var chat = document.getElementsByClassName("chat")[0];
    var seach = document.getElementsByClassName("seach")[0];
    seach.style.display = "none";
    chat.style.display = "block";
}
function seach(){
    var seach = document.getElementsByClassName("seach")[0];
    var chat = document.getElementsByClassName("chat")[0];
    seach.style.display = "block";
    chat.style.display = "none";
}
function hi(id) {
    var element = document.getElementById("messages_id_"+id);
    var element1 = document.getElementById("messages_id_p_" + id);
    var style = window.getComputedStyle(element1);
    var marginLeft = parseInt(style.marginLeft);
    var marginRight = parseInt(style.marginRight);
    var width = element.offsetWidth + marginLeft + marginRight;
    element.style.marginLeft = "calc(100% - " + width + "px)";
}








