const body = document.querySelector('body');
body.style.transition = "opacity 300ms ease-in";
body.style.opacity = "1";

setTimeout(function() {
   
    body.style.opacity = "0";
    
    setTimeout(function() {
         window.location.href = "/accounts/landing/";
    }, 300);

}, 200);
