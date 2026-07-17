document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // 상단 탭
    // ==========================

    const tabs = document.querySelectorAll(".tabSelection a");
    const myStepTab = document.querySelector(".myStepTab");
    const allMajorTab = document.querySelector(".allMajorTab");

    tabs[0].addEventListener("click", () => {
        tabs[0].classList.add("tabSelected");
        tabs[0].classList.remove("tab");

        tabs[1].classList.add("tab");
        tabs[1].classList.remove("tabSelected");

        myStepTab.style.display = "block";
        allMajorTab.style.display = "none";
    });

    tabs[1].addEventListener("click", () => {
        tabs[1].classList.add("tabSelected");
        tabs[1].classList.remove("tab");

        tabs[0].classList.add("tab");
        tabs[0].classList.remove("tabSelected");

        myStepTab.style.display = "none";
        allMajorTab.style.display = "block";
    });


    // ==========================
    // 카테고리
    // ==========================

    const categoryBtns = document.querySelectorAll(".categoryOption");

    const allCategory = document.querySelector(".allCategory");
    const programCategory = document.querySelector(".programCategory");
    const lectureCategory = document.querySelector(".lectureCategory");
    const bookCategory = document.querySelector(".bookCategory");

    const categoryLists = [
        allCategory,
        programCategory,
        lectureCategory,
        bookCategory
    ];

    categoryBtns.forEach((button, index) => {

        button.addEventListener("click", () => {

            // 버튼 스타일 변경
            categoryBtns.forEach(btn => {
                btn.classList.remove("categoryActivated");
            });

            button.classList.add("categoryActivated");

            // 내용 변경
            categoryLists.forEach(list => {
                list.style.display = "none";
            });

            categoryLists[index].style.display = "grid";

        });

    });


    // ==========================
    // 북마크
    // ==========================

    const bookmarkBtns = document.querySelectorAll(".bookmarkBtn");

    bookmarkBtns.forEach(button => {

        const off = button.querySelector(".bookmark");
        const on = button.querySelector(".bookmarkActivated");

        let bookmarked = false;

        button.addEventListener("click", () => {

            bookmarked = !bookmarked;

            if (bookmarked) {
                off.style.display = "none";
                on.style.display = "block";
            } else {
                off.style.display = "block";
                on.style.display = "none";
            }

            // --------------------------
            // 백엔드 연결 필요: 자료실에서 북마크 > 담은 자료에서 확인
            // --------------------------
        });
    });
});