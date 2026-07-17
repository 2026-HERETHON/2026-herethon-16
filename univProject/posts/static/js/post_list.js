document.querySelectorAll('.box_btn').forEach(function(button) {
  button.addEventListener('click', function(event) {
    event.stopPropagation();
    event.preventDefault(); 
    this.classList.toggle('active');
  });
});

const modal = document.getElementById('write-modal');
const openBtn = document.getElementById('open-modal-btn');
const closeBtn = document.getElementById('close-modal-btn');

if (openBtn && modal) {
  openBtn.addEventListener('click', function(event) {
    event.preventDefault(); 
    modal.classList.add('show'); 
  });
}

if (modal) {
  modal.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.classList.remove('show');
    }
  });
}

const categoryButtons = document.querySelectorAll('.cate-btn');
const categoryInput = document.getElementById('category-input'); // 추가

if (categoryButtons.length > 0) {
  categoryButtons.forEach(button => {
    button.addEventListener('click', function(event) {
      event.preventDefault(); 
      
      categoryButtons.forEach(btn => btn.classList.remove('active'));
      
      this.classList.add('active');

      if (categoryInput) {
        categoryInput.value = this.dataset.value || ''; // 추가
      }
    });
  });
}

document.querySelectorAll(".heartButton").forEach((heartButton) => {
  const heartFull = heartButton.querySelector(".heartFull");
  const heartEmpty = heartButton.querySelector(".heartEmpty");

  let liked = false;

  heartButton.addEventListener("click", () => {
    liked = !liked;

    if (liked) {
      heartFull.style.display = "block";
      heartEmpty.style.display = "none";
    } else {
      heartFull.style.display = "none";
      heartEmpty.style.display = "block";
    }
  });
});