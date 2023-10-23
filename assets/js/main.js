const cookieName = "kartikCounterCookie";
const imageOneId = "imageOne";
const imageTwoId = "imageTwo";
const formDivId = "formDiv";
const imageOneName = "imageOneName";
const imageTwoName = "imageTwoName";
const baseUrl = "https://kartik-labeling-cvpr-0ed3099180c2.herokuapp.com/";
//const baseUrl = "http://localhost:8080/";

function getCookie(name) {
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
    return match ? match[1] : null;
}

function setCookie(val) {
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 3000000*3600;
    now.setTime(expireTime);
    document.cookie = cookieName + "=" + 1 + ";expires=" + now.toUTCString() + ";path=/";
}

if (!getCookie(cookieName)) {
    setCookie(1);
}

function preSubmit() {
    var label = document.getElementById(labelField).value;
    if (label > 10 || label < 0)
	return false;
    var currentCount = getCookie(cookieName);
    if (!currentCount) {
	setCookie(1);
    }
    else {
	setCookie(parseInt(currentCount) + 1);
    }
    return True;
}
