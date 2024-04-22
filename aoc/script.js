let loginForm = document.getElementById("submit-form");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let answer = document.getElementById("answer");

  if (md5(answer.value) === "3ba9af181751761d3b387f74ded2d783") {
    document.getElementById("next").innerHTML = `Fragment de 🔥 [1/3] = ${answer.value}, <a href="../chess">passer à la suite</a>`;
  }
});
