// 탐색 학기 Flow 첫 번째 화면
const nextButton = document.querySelector(".nextButton");

// select1.html로 이동하는 버튼 (선택1 화면으로 이동)
nextButton.addEventListener("click", () => {
  window.location.href = nextButton.dataset.nextUrl;
});
