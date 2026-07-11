// 전공 체험 시작 버튼
const startButton = document.querySelector(".startButton");

// 전공 체험 시작 버튼 -> experience1.html (체험수업1 화면) 로 이동
startButton.addEventListener("click", () => {
  window.location.href = startButton.dataset.nextUrl;
});
