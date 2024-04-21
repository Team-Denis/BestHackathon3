const keyRemap = {
    "a": "q",
    "b": "w",
    "c": "e",
    "d": "r",
    "e": "t",
    "f": "y",
    "g": "u",
    "h": "i",
    "i": "o",
    "j": "p",
    "k": "a",
    "l": "s",
    "m": "d",
    "n": "f",
    "o": "g",
    "p": "h",
    "q": "j",
    "r": "k",
    "s": "l",
    "t": "z",
    "u": "x",
    "v": "c",
    "w": "v",
    "x": "b",
    "y": "n",
    "z": "m",
};

const fragment = 4157;

const inputBox = document.getElementById("input");
const submitButton = document.getElementById("submit");
const correctSentence = "un farfadet malicieux a remap les touches de ton clavier";

function keyTranslate(e) {
    // Checks if the input is a letter
    if (!e.data || !keyRemap[e.data]) {
        return;
    }
    var inputText = inputBox.value;
    var lastChar = inputText.charAt(inputText.length - 1);
    var translatedChar = keyRemap[lastChar];
    var newText = inputText.substring(0, inputText.length - 1) + translatedChar;
    inputBox.value = newText;
}

function checkSentence() {
    if (inputBox.value === correctSentence) {
        alert("Success !\nFragment 4/4: " + fragment);
        window.location.href = "keyRemapSuccess.html";
    } else {
        alert("Incorrect!");
    }
}

inputBox.addEventListener("input", keyTranslate);
submitButton.addEventListener("click", checkSentence);