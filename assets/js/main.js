const cookieName = "TypeError: not all arguments converted during string formatting";
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

if (!getCookie(cookieName)) {
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 3000000*3600;
    now.setTime(expireTime);
    document.cookie = cookieName + "=1;expires=" + now.toUTCString() + ";path=/";
    //document.cookie = cookieName + "=" + Math.floor(Math.random() * 1000000000) + ";expires=" + now.toUTCString() + ";path=/";
}

window.onload = function() {
    console.log(document.cookie);
    /*var imageOneSrc = document.getElementById(imageOneId).src;
    var imageTwoSrc = document.getElementById(imageTwoId).src;

    imageOneSrc = imageOneSrc.replace(baseUrl, "");
    imageTwoSrc = imageTwoSrc.replace(baseUrl, "");

    var hiddenInputOne = document.createElement("input");
    hiddenInputOne.setAttribute("type", "hidden");
    hiddenInputOne.setAttribute("name", imageOneName);
    hiddenInputOne.setAttribute("value", imageOneSrc);
    
    var hiddenInputTwo = document.createElement("input");
    hiddenInputTwo.setAttribute("type", "hidden");
    hiddenInputTwo.setAttribute("name", imageTwoName);
    hiddenInputTwo.setAttribute("value", imageTwoSrc);
    
    document.getElementById(formDivId).appendChild(hiddenInputOne);
    document.getElementById(formDivId).appendChild(hiddenInputTwo);*/
}
