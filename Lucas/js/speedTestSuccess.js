const fragment = 4269;

document.getElementById("fragment").innerText = "Fragment for this challenge : " + fragment;

document.getElementById("next-button").addEventListener("click", 
    () => {
        window.location.href = "passwordGame.html";
    }
);