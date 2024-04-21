const timeLimit = 1000;
var counter = timeLimit;
const fragment = 3617;

function checkValidEmail(email) {
    return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}


function keyPressHandler(event) {
    if (event.key === 'Enter') {
        const user_input = document.getElementById('email-input').value;
        
        if (checkValidEmail(user_input)) {
            alert("Success !\nFragment de 💨 2/4: " + fragment);
            window.location.href = 'speedTestSuccess.html';
        } else {
            alert('Invalid email');
            window.location.href = 'speedTest.html';
        }
    }
}

function afterTimeOut() {
    counter = timeLimit;
    document.getElementById('email-input').value = '';
    document.getElementById('time-remaining').innerText = "Time limit reached, try again...";
}

function timerStart() {
    // Reinitialize user input
    document.getElementById('email-input').value = '';

    const endTime = Date.now() + timeLimit;
    let intervalId = setInterval(() => {
        if (counter > 0) {
            counter = endTime - Date.now();
            document.getElementById('time-remaining').innerText = `${counter} [ms]`;
        }
        else {
            clearInterval(intervalId);
            afterTimeOut();
        }
    }, 1);
}

document.addEventListener('keypress', keyPressHandler);
document.getElementById('start-timer').addEventListener('click', timerStart);