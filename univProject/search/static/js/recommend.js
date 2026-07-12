/* 추천 전공 - 1, 2 화면 */
const backIcon = document.querySelector(".material-symbols-outlined.backIcon"); // 이전 버튼
const startButton = document.querySelector(".startButton"); // 전공 체험 시작 버튼

// 이전 버튼 (이전 페이지로 이동)
backIcon.addEventListener("click", () => {
  window.history.back();
});

// 전공 체험 시작 버튼 -> experience1.html (체험수업1 화면) 로 이동
startButton.addEventListener("click", () => {
  window.location.href = startButton.dataset.nextUrl;
});
