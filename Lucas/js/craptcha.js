var canvas = document.getElementById("captcha");
console.log(canvas);
var ctx = canvas.getContext("2d");

const width = canvas.width
const height = canvas.height

ctx.font = "normal 36px Verdana";
ctx.fillStyle = "#000000"
ctx.textAlign = "left"

var character_list = ["🈵", "👹", "👽", "😁", "😘", "😨"]
const CAPTCHA_LENGTH = 4;
var captcha_txt;
var validation_counter = 3;

// const txt = character_list.join("");
// ctx.fillText(txt, width/2 - ctx.measureText(txt).width/2, height/2)

function gen_captcha(char_list) {
    let out = '';
    let temp_list = [...char_list]; // Create a copy of the original list
    for(let i = 0; i < CAPTCHA_LENGTH; i++) {
        let randomIndex = Math.floor(Math.random() * temp_list.length);
        out += temp_list[randomIndex];
        temp_list.splice(randomIndex, 1); // Remove the selected character from the list
    }
    console.log(out);
    return out;
}

function display_captcha(context, captcha_txt) {
    context.fillText(captcha_txt, (width - ctx.measureText(captcha_txt).width)/2, height/2);
}

function verify_captcha() {
    const user_input = document.getElementById("captcha-input").value;
    document.getElementById("captcha-input").value = "";
    if (user_input.localeCompare(captcha_txt) === 0) {
        validation_counter -= 1;
    }
    else {
        alert("Invalid");
    }

    if (validation_counter === 0) {
        window.location.href = "../pages/craptchaSuccess.html";
    }
 
    captcha_txt = gen_captcha(character_list);
    display_captcha(ctx, captcha_txt);
}

document.getElementById("captcha-button").addEventListener("click", verify_captcha)
captcha_txt = gen_captcha(character_list);
display_captcha(ctx, captcha_txt);
