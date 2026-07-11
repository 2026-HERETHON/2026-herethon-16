const startButton = document.querySelector(".startButton");
const majorCards = document.querySelectorAll(".majorCard");

// 초기 상태 (CTA 비활성화)
startButton.classList.add("disabled");

// 전공 카드 선택
majorCards.forEach((card) => {
  card.addEventListener("click", () => {
    majorCards.forEach((item) => {
      item.classList.remove("selected");
    });
    card.classList.add("selected");

    // CTA 활성화
    startButton.classList.remove("disabled");
    startButton.classList.add("active");
  });
});

// "이 전공으로 시작하기" CTA 버튼
startButton.addEventListener("click", () => {
  console.log("이 전공으로 시작하기");
});
