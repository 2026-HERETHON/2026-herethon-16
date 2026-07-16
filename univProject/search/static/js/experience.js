const backIcon = document.querySelector(".material-symbols-outlined.backIcon"); // 이전 버튼
const answerInputs = document.querySelectorAll(".answerInput"); // 사용자 입력값
const completeButton = document.querySelector(".completeButton"); // "첫 전공 체험 시작하기" 버튼

// 초기 상태 (CTA 비활성화)
completeButton.disabled = true;

// 이전 버튼 (이전 페이지로 이동)
backIcon.addEventListener("click", () => {
  window.history.back();
});

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

// 3개의 항목이 모두 한 글자 이상 입력되었는지 체크
function checkComplete() {
  const isCompleted = [...answerInputs].every(
    (input) => input.value.trim().length > 0,
  );

  if (isCompleted) {
    // 조건 충족 시, CTA 버튼 활성화
    completeButton.disabled = false;
  } else {
    // 조건 불충족 시, CTQ 버튼 비활성화
    completeButton.disabled = true;
  }
}

// 사용자가 입력을 할 때마다 -> 입력한 글자수 UI에 반영, CTA 버튼 활성화 조건 체크
answerInputs.forEach((input) => {
  input.addEventListener("input", () => {
    updateCharacterCount(input);
    checkComplete();
  });
});

// 전공 체험 완료 버튼 -> 다음 페이지로 이동
completeButton.addEventListener("click", () => {
  // 사용자의 답변을 저장할 배열
  const answers = [];

  // answerInputs 배열에 사용자 답변 추가
  answerInputs.forEach((input) => {
    answers.push({
      questionId: Number(input.dataset.questionId),
      answer: input.value.trim(),
    });
  });

  // 사용자 답변을 log로 출력 (추후 API 연동 시 수정할 예정)
  console.log("사용자 답변:", answers);

  // 다음 페이지로 이동
  window.location.href = completeButton.dataset.nextUrl;
});
