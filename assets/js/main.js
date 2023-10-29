const cookieName = "kartikCounterCookie";
const imageOneId = "imageOne";
const imageTwoId = "imageTwo";
const formDivId = "formDiv";
const imageOneName = "imageOneName";
const imageTwoName = "imageTwoName";
const labelFormId = "labelForm";
const labelField = "labelField";
const baseUrl = "https://kartik-labeling-cvpr-0ed3099180c2.herokuapp.com";
const counterDiv = "counterDiv";
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
    document.cookie = cookieName + "=" + val + ";expires=" + now.toUTCString() + ";path=/";
}

if (!getCookie(cookieName)) {
    setCookie(1);
}

const versionCountMap = {
    "/hzVGodRyhB": "3000",
    "/cpmKQMWnB0": "2500"
}

function resizeImage(img) {
    if (img.width > 500) {
	var aspectRatio = img.width / img.height;
	img.width = 500;
	img.height = 500 / aspectRatio;
    }

    if (img.height > 500) {
	var aspectRatio = img.width / img.height;
	img.height = 500;
	img.width = 500 * aspectRatio
    }
}
window.onload = function() {
    var versionUserStr = window.location.href.replace(baseUrl, "");
    var totalCount = "500";
    document.getElementById(labelFormId).action = versionUserStr;

    
    if (versionUserStr in versionCountMap) {
	totalCount = versionCountMap[versionUserStr];
    }
    document.getElementById(counterDiv).innerHTML = getCookie(cookieName) + "/" + totalCount + " done";

    resizeImage(document.getElementById(imageOneId));
    resizeImage(document.getElementById(imageTwoId));
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
    return true;
}
