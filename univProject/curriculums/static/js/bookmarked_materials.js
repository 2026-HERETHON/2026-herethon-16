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
        location.href = "/materials/";
    });
}