/* 선택 1~3 화면 JS 파일 */

// 선택 최대 개수 (HTML에서 설정)
const maxSelectCount = Number(
  document.querySelector(".optionList").dataset.max,
);

const optionCards = document.querySelectorAll(".optionCard");
const backIcon = document.querySelector(".material-symbols-outlined.backIcon");
const nextButton = document.querySelector(".nextButton");

// 초기 상태 (CTA 비활성화)
nextButton.disabled = true;

// 설문 선택
optionCards.forEach((card) => {
  const checkbox = card.querySelector('input[type="checkbox"]');

  // 체크박스 상태가 바뀔 때마다
  checkbox.addEventListener("change", () => {
    const checkedCards = document.querySelectorAll(".optionCard input:checked");

    // N개 초과 선택 방지
    if (checkedCards.length > maxSelectCount) {
      checkbox.checked = false;
      return;
    }

    // 체크박스에 체크된 옵션 카드의 스타일 변경
    optionCards.forEach((c) => {
      const input = c.querySelector("input");
      c.classList.toggle("selected", input.checked);
    });

    // CTA 버튼 비활성화 or 활성화 체크
    updateNextButton();
  });
});

// 이전 버튼 (이전 페이지로 이동)
backIcon.addEventListener("click", () => {
  window.history.back();
});

// 선택 개수가 바뀔 때마다 CTA 버튼 스타일 변경
function updateNextButton() {
  // 1개 이상 선택 시
  const checkedCount = document.querySelectorAll(
    ".optionCard input:checked",
  ).length;

  // 0개 클릭된 경우엔 CTA 버튼 비활성화
  // 1개 이상 클릭된 경우엔 CTA 버튼 활성화
  nextButton.disabled = checkedCount === 0;
}
