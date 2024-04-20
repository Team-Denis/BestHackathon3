let loginForm = document.getElementById("submit-form");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let answer = document.getElementById("answer");

  if (md5(answer.value) === "3ba9af181751761d3b387f74ded2d783") {
    alert(`Fragment 1/5 = ${answer.value}`);
  }
});
