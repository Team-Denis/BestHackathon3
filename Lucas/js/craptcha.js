var canvas = document.getElementById("captcha");
console.log(canvas);
var ctx = canvas.getContext("2d");

ctx.font = "normal 36px Verdana";
ctx.fillStyle = "#000000"
ctx.textAlign = "left"
ctx.fillText("😁", 50, 50)

