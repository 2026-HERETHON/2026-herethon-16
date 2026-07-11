// 선택 1 - 해온 경험 (가장 익숙한 경험은 무엇인가요?)
const optionCards = document.querySelectorAll(".optionCard");
const backIcon = document.querySelector(".material-symbols-outlined.backIcon");
const nextButton = document.querySelector(".nextButton");

// 사용자가 선택한 옵션 저장
const selectedOptions = [];

// 설문 선택
optionCards.forEach((card) => {
  card.addEventListener("click", () => {
    const index = selectedOptions.indexOf(card);

    // 이미 선택되어 있으면 해제
    if (index > -1) {
      selectedOptions.splice(index, 1);
      card.classList.remove("selected");
      updateNextButton(); // 버튼 스타일 업데이트
      return;
    }

    // 최대 2개
    if (selectedOptions.length >= 2) {
      return;
    }

    selectedOptions.push(card);
    card.classList.add("selected");
    updateNextButton(); // 버튼 스타일 업데이트
  });
});

// 이전 버튼 (이전 페이지로 이동)
backIcon.addEventListener("click", () => {
  window.history.back();
});

// select2.html로 이동하는 CTA 버튼 (선택2 화면으로 이동)
nextButton.addEventListener("click", () => {
  // CTA 비활성 상태일 경우, 클릭 이벤트 무효화
  if (selectedOptions.length === 0) return;

  console.log(selectedOptions.map((card) => card.innerText));

  // 다음 페이지 이동
  window.location.href = nextButton.dataset.nextUrl;
});

// 선택 개수가 바뀔 때마다 버튼 스타일 변경
function updateNextButton() {
  // 1개 이상 선택 시
  if (selectedOptions.length > 0) {
    nextButton.classList.add("active");
  } else {
    // 아무것도 선택 안 한 경우
    nextButton.classList.remove("active");
  }
}
