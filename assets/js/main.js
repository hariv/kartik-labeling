const imageOneId = "imageOne";
const imageTwoId = "imageTwo";
const formDivId = "formDiv";
const imageOneName = "imageOneName";
const imageTwoName = "imageTwoName";
const pairIdDiv = "pairIdDiv";
const counterDiv = "counterDiv";
const labelField = "labelField";
const hiddenPairId = "hiddenPairId";
const baseUrl = "https://kartik-labeling-cvpr-0ed3099180c2.herokuapp.com";
const counterDiv = "counterDiv";
const urlExtension = "";

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

function sendData(data, endpoint) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	    var response = xmlhttp.responseText;
	    var responseObject = JSON.parse(response);
	    
	    var versionUserStr = window.location.href.replace(baseUrl, "");
	    var versionStr = versionUserStr.split("/")[2];
	    var totalCount = "500";

	    if (versionStr in versionCountMap) {
		// If this exists, then the cookie map should also exit
		totalCount = versionCountMap[versionStr];
		
		if (!getCookie(versionCookieMap[versionStr])) {
		    setCookie(versionCookieMap[versionStr], 1);
		}
	    }
	    
	    document.getElementById(imageOneId).src = responseObject.img_1_b64;
	    document.getElementById(imageTwoId).src = responseObject.img_2_b64;
	    document.getElementById(pairIdDiv).innerHTML = "Pair ID: " + responseObject.pair_id;
	    document.getElementById(hiddenPairId).value = responseObject.pair_id;
	    
	    if (getCookie(versionCookieMap[versionStr])) {
		document.getElementById(counterDiv).innerHTML = getCookie(versionCookieMap[versionStr]) + "/" + totalCount + " done";
	    }
	    else {
		document.getElementById(counterDiv).innerHTML = "1/" + totalCount + " done";
	    }
	    resizeImage(document.getElementById(imageOneId));
	    resizeImage(document.getElementById(imageTwoId));
	}
    }
    xmlhttp.open("POST", endpoint);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(data));
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
    //urlExtension = versionUserStr;

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

function submitLabel() {
    var label = document.getElementById(labelField).value;
    if (label > 10 || label < 0) {
	alert("Label has to be within 1 and 10");
	return;
    }

    if (label == "") {
	alert("You have to enter a label");
	return;
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
    var labelData = {};
    labelData.label = label;
    labelData.pairId = document.getElementById(hiddenPairId).value;
    sendData(labelData, versionUserStr);
}
/*function preSubmit(e) {    
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
}*/
