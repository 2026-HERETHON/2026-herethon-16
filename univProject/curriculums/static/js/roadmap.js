// ==============================
// Roadmap Progress
// ==============================

// TODO: Django 연동 후 사용자의 현재 진행 단계를 받아올 예정
const currentStep = 1;

const roadmapSteps = document.querySelectorAll(".roadmapStep");

roadmapSteps.forEach(step => {

    const stepNumber = Number(step.dataset.step);
    const status = step.querySelector(".roadmapStatus");

    if (stepNumber < currentStep) {
        status.textContent = "완료";
    } else if (stepNumber === currentStep) {
        status.textContent = "진행 중";
    } else {
        status.textContent = "예정";
    }

});