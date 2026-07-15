const userInputs = document.querySelectorAll(".answerInput, .reviewInput"); // 사용자 입력값
const completeButton = document.querySelector(".completeButton"); // 버튼 (수업 완료하기, N차시로 가기)

// 글자수 세기
function updateCharacterCount(input) {
  const maxLength = Number(input.maxLength);

  // 글자수 제한을 초과한 경우 -> 그 이상 입력한 내용은 버리기
  if (input.value.length > maxLength) {
    input.value = input.value.slice(0, maxLength);
  }

  const count = input.value.length;
  const counter = input.parentElement.querySelector(".currentCount");
  counter.textContent = count;
}

// 모든 항목이 모두 한 글자 이상 입력되었는지 체크
function checkComplete() {
  const isCompleted = [...userInputs].every(
    (input) => input.value.trim().length > 0,
  );

  if (isCompleted) {
    // 조건 충족 시, CTA 버튼 활성화
    completeButton.classList.add("active");
  } else {
    // 조건 불충족 시, CTA 버튼 비활성화
    completeButton.classList.remove("active");
  }
}

// 사용자가 입력을 할 때마다 -> 입력한 글자수 UI에 반영, CTA 버튼 활성화 조건 체크
userInputs.forEach((input) => {
  input.addEventListener("input", () => {
    updateCharacterCount(input);
    checkComplete();
  });
});
