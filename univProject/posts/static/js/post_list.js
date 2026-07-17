document.querySelectorAll('.box_btn').forEach(function(button) {
  button.addEventListener('click', function(event) {
    // 1. 카드 클릭(상세페이지 이동) 이벤트로 번지는 것 차단
    event.stopPropagation();
    event.preventDefault(); 
    
    // 2. 클릭할 때마다 active 클래스를 넣었다 뺐다 토글
    this.classList.toggle('active');
   
  });
});



const modal = document.getElementById('write-modal');
const openBtn = document.getElementById('open-modal-btn');
const closeBtn = document.getElementById('close-modal-btn');

//플러스(+) 버튼 클릭 시 모달 열기 
if (openBtn && modal) {
  openBtn.addEventListener('click', function(event) {
    event.preventDefault(); 
    modal.classList.add('show'); 
  });
}



// 어두운 바깥 배경 클릭 시 모달 닫기
if (modal) {
  modal.addEventListener('click', function(event) {
    // 내가 클릭한 곳이 흰색 모달 박스가 아니라 바깥 어두운 배경일 때만 닫기
    if (event.target === modal) {
      modal.classList.remove('show');
    }
  });
}


const categoryButtons = document.querySelectorAll('.cate-btn');

if (categoryButtons.length > 0) {
  categoryButtons.forEach(button => {
    button.addEventListener('click', function(event) {
      event.preventDefault(); 
      
      categoryButtons.forEach(btn => btn.classList.remove('active'));
      
      this.classList.add('active');
      
    });
  });
}