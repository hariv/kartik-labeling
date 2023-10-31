//const cookieName = "kartikCounterCookie";
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

const versionCountMap = {
    "hzVGodRyhB": "3000",
    "cpmKQMWnB0": "2500",
    "hzoK4PdUsc": "2",
    "gPuFU6tgsI": "6"
}

const versionCookieMap = {
    "hzVGodRyhB": "kartikCounterCookieV3",
    "cpmKQMWnB0": "kartikCounterCookieV4",
    "hzoK4PdUsc": "katikCounterCookieV1",
    "gPuFU6tgsI": "kartikCounterCookieV2"
}

function getCookie(name) {
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
    return match ? match[1] : null;
}

function setCookie(cookieName, val) {
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 3000000*3600;
    now.setTime(expireTime);
    document.cookie = cookieName + "=" + val + ";expires=" + now.toUTCString() + ";path=/";
}

//if (!getCookie(cookieName)) {
//    setCookie(1);
//}

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

//window.addEventListener('popstate', function(event) {
//    alert("You've accidentally pressed the back button. Don't do that.");
//});

//window.onpopstate=function() {
//    alert("Back/Forward clicked!");
//}

//window.addEventListener('popstate', function (event) {
//    alert("fuck otu");
//});

window.onpopstate = (e) => {
    alert("sdfsf");
};

window.onload = function() {
    var label = document.getElementById(labelField).value;
    
    //if (label != "") {
    //alert("You have accidentally pressed the back button. Please hit the refresh button again to proceed.");
    //window.location.reload();
    //}
    
    var versionUserStr = window.location.href.replace(baseUrl, "");
    var totalCount = "500";
    document.getElementById(labelFormId).action = versionUserStr;

    var versionStr = versionUserStr.split("/")[2];

    if (versionStr in versionCountMap) {
	// If this exists, then the cookie map should also exit
	totalCount = versionCountMap[versionStr];
	if (!getCookie(versionCookieMap[versionStr])) {
	    setCookie(versionCookieMap[versionStr], 1);
	}
    }

    if (getCookie(versionCookieMap[versionStr])) {
	document.getElementById(counterDiv).innerHTML = getCookie(versionCookieMap[versionStr]) + "/" + totalCount + " done";
    }
    else {
	document.getElementById(counterDiv).innerHTML = "1/" + totalCount + " done";
    }

    
    resizeImage(document.getElementById(imageOneId));
    resizeImage(document.getElementById(imageTwoId));
}

function preSubmit(e) {    
    var label = document.getElementById(labelField).value;
    if (label > 10 || label < 0) {
	e.preventDefault();
	return false;
    }

    if (label == "") {
	alert("Please enter a label");
	e.preventDefault();
	return false;
    }
    var versionUserStr = window.location.href.replace(baseUrl, "");
    var versionStr = versionUserStr.split("/")[2];
    
    var currentCount = getCookie(versionCookieMap[versionStr]);
    
    if (!currentCount) {
	setCookie(versionCookieMap[versionStr], 1);
    }
    else {
	setCookie(versionCookieMap[versionStr], parseInt(currentCount) + 1);
    }
    return true;
}
