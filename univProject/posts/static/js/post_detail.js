document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        this.classList.toggle("active");
    });
});