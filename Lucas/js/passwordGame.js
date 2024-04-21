const list = document.getElementById('list');
const fragment = 2907;

function romanToNumber(roman) {
    const romanNumerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    };

    let result = 0;

    for (let i = 0; i < roman.length; i++) {
        if (i > 0 && romanNumerals[roman[i]] > romanNumerals[roman[i - 1]]) {
            result += romanNumerals[roman[i]] - 2 * romanNumerals[roman[i - 1]];
        } else {
            result += romanNumerals[roman[i]];
        }
    }

    return result;
}

var rulesIndication = [
    "At least 5 characters",
    "At least 1 number",
    "An uppercase letter",
    "A special character",
    "Digits summing to 25",
    "A month",
    "One brand among 'pepsi', 'starbucks' and 'shell'",
    "Roman numerals need to multiply to 35",
    "Solve the chess problem in the image and add the first best move in the password",
    "Today's Wordle solution",
]

var rules = [
    (password) => password.length >= 5,
    (password) => /\d/.test(password),
    (password) => /[A-Z]/.test(password),
    (password) => /[^a-zA-Z0-9]/.test(password),
    (password) => {
        let sum = 0;
        for(let i = 0; i < password.length; i++) {
            let char = password[i];
            if(!isNaN(char)) {
                sum += parseInt(char);
            }
        }
        return sum === 25;
    },
    (password) => /january|february|march|april|may|june|july|august|september|october|november|december/.test(password.toLowerCase()),
    (password) => /pepsi|starbucks|shell/.test(password.toLowerCase()),
    (password) => {
        const romanRegex = /[IVXLCDM]+/g;
        const matches = password.match(romanRegex);

        if (!matches) {
            return 0; // If no Roman numerals found, return 0
        }

        let product = 1;

        for (let i = 0; i < matches.length; i++) {
            product *= romanToNumber(matches[i]);
        }

        return (product===35);
    },
    (password) => /rh4\+/.test(password.toLowerCase()),
    (password) => password.toLowerCase() === "jolly",
]

function checkPassword() {
    var password = document.getElementById('password-input').value;

    var countValid = 0;

    for (let i = 0; i < rules.length; i++) {
        if (!rules[i](password)) {
            list.children[i].style.backgroundColor = 'red';
        }
        else {
            list.children[i].style.backgroundColor = 'green';
            countValid++;
        }
    }

    if (countValid === rules.length) {
        alert("Success !\nFragment 3/4: " + fragment);
        window.location.href = "passwordGameSuccess.html";
    }
    
}   

for (let i = 0; i < rules.length; i++) {
    var li = document.createElement('li');
    li.textContent = rulesIndication[i];
    list.appendChild(li);
}

document.getElementById('try-button').addEventListener('click', checkPassword);



