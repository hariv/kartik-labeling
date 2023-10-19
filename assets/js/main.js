var cookieName = "kartikCookie";
var imageOneId = "imageOne";
var imageTwoId = "imageTwo";
var formDivId = "formDiv";

function sendData(d, endpoint) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", endpoint);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(data));
}

function getCookie(name) {
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
    return match ? match[1] : null;
}

if (!getCookie(cookieName)) {
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 3000000*3600;
    now.setTime(expireTime);
    document.cookie = cookieName + "=" + Math.floor(Math.random() * 1000000000) + ";expires=" + now.toUTCString() + ";path=/";
}

window.onload = function() {
    console.log("lsdf");
    var hiddenInputOne = document.createElement("input");
    hiddenInputOne.setAttribute("type", "hidden");
    hiddenInputOne.setAttribute("name", "imgOneName");
    hiddenInputOne.setAttribute("value", document.getElementById(imageOneId).src);
    
    var hiddenInputTwo = document.createElement("input");
    hiddenInputTwo.setAttribute("type", "hidden");
    hiddenInputTwo.setAttribute("name", "imgTwoName");
    hiddenInputTwo.setAttribute("value", document.getElementById(imageTwoId).src);
    
    document.getElementById(formDivId).appendChild(hiddenInputOne);
    document.getElementById(formDivId).appendChild(hiddenInputTwo);
}

/*function submitLabel() {
    var imgOneName = document.getElementById(imageOneId).src;
    var imgTwoName = document.getElementById(imageTwoId).src;
    var label = document.getElementById("labelOption").value;

    var labelObject = {};
    labelObject.imgOneName = imgOneName;
    labelObject.imgTwoName = imgTwoName;
    labelObject.label = label;

    sendData(labelObject);    
}*/
