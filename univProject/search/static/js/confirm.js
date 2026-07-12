const backIcon = document.querySelector(".material-symbols-outlined.backIcon"); // 이전 버튼
const startButton = document.querySelector(".startButton"); // "이 전공으로 시작하기" CTA 버튼
const majorCards = document.querySelectorAll(".majorCard"); // 전공 카드

startButton.classList.add("disabled"); // 초기 상태 (CTA 비활성화)
let selectedMajorId = null; // 사용자가 선택한 전공 ID를 저장할 변수

// 이전 버튼 (이전 페이지로 이동)
backIcon.addEventListener("click", () => {
  window.history.back();
});

// 전공 카드 선택
majorCards.forEach((card) => {
  card.addEventListener("click", () => {
    majorCards.forEach((item) => {
      item.classList.remove("selected");
    });
    card.classList.add("selected");

    // 사용자가 선택한 전공 ID 저장
    selectedMajorId = Number(card.dataset.majorId);

    // CTA 활성화
    startButton.classList.remove("disabled");
    startButton.classList.add("active");
  });
});

// "이 전공으로 시작하기" CTA 버튼
startButton.addEventListener("click", () => {
  console.log("선택한 전공 ID:", selectedMajorId); // 사용자가 선택한 전공 ID 출력
});
