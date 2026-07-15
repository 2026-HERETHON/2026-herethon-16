// ==============================
// Downloads Page
// ==============================

// TODO: Django 연동 후 사용자의 북마크 데이터를 받아올 예정
const materials = [];


// ==============================
// Empty / Full Page
// ==============================

const emptyPage = document.getElementById("emptypage");
const fullPage = document.getElementById("fullpage");

if (materials.length === 0) {

    emptyPage.style.display = "flex";
    fullPage.style.display = "none";

} else {

    emptyPage.style.display = "none";
    fullPage.style.display = "block";

}


// ==============================
// Move To Article
// ==============================

const moveToDownloads = document.querySelector(".moveToDownloads");

if (moveToDownloads) {

    moveToDownloads.addEventListener("click", () => {

        // TODO: 자료실 페이지 경로로 변경
        // location.href = "../article/article.html";

    });

}