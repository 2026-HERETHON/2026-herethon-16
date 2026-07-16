// ==============================
// Filter Component
// ==============================

const filters = document.querySelectorAll(".filterComponent > div");

filters.forEach(filter => {
    filter.addEventListener("click", () => {

        const page = filter.dataset.page;

        // data-page가 없으면 종료
        if (!page) {
            return;
        }

        // 현재 페이지면 다시 이동하지 않음
        if (window.location.pathname.endsWith(page)) {
            return;
        }

        location.href = page;
    });
});

// ==============================
// Footer Navigation
// (추후 구현 예정)
// ==============================

// const footerTabs = document.querySelectorAll(".footerTap, .footerTapActive");

// footerTabs.forEach(tab => {
//     tab.addEventListener("click", () => {
//
//     });
// });