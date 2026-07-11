const nextButton = document.querySelector(".nextButton");

nextButton.addEventListener("click", () => {
  window.location.href = nextButton.dataset.nextUrl;
});
