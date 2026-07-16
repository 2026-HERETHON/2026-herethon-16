document.addEventListener('DOMContentLoaded', () => {
    const introSection = document.querySelector('.intro');
    const mainSection = document.getElementById('mainSection');

    setTimeout(() => {
        if (introSection && mainSection) {
            introSection.style.opacity = '0';
            
            mainSection.classList.remove('hide');

            setTimeout(() => {
                introSection.style.display = 'none';
            }, 300);
        }
    }, 1000);
});