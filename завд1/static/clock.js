function updateClock(element) {
  const now = new Date();

  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");

  element.textContent = `${hours} : ${minutes}`;
}

// приклад використання
const clockElement = document.querySelector("#clock");

updateClock(clockElement);
setInterval(() => updateClock(clockElement), 60000);
