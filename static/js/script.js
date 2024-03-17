//#region ============    Menu   ============ 
    /*===== MENU SHOW Y HIDDEN =====*/ 
    const navMenu = document.getElementById('nav-menu'),
    toggleMenu = document.getElementById('nav-toggle'),
    closeMenu = document.getElementById('nav-close')

    
    /*SHOW*/ 
    toggleMenu.addEventListener('click', ()=>{
        console.log(navMenu)
        navMenu.classList.toggle('show')
        console.log(navMenu)
    })

    /*HIDDEN*/
    closeMenu.addEventListener('click', ()=>{
        navMenu.classList.remove('show')
    })

    /*===== ACTIVE AND REMOVE MENU =====*/
    const navLink = document.querySelectorAll('.nav__link');   

    function linkAction(){
        /*Active link*/
        navLink.forEach(n => n.classList.remove('active'));
        this.classList.add('active');
        
        /*Remove menu mobile*/
        navMenu.classList.remove('show')
    }
    navLink.forEach(n => n.addEventListener('click', linkAction));
//#endregion =========    End Menu   ============ 


//#region ============    User Registration   ============ 
const inputs = document.querySelectorAll(".registration-main .input-field");
const toggle_btn = document.querySelectorAll(".registration-main .toggle");
const main = document.querySelector(".registration-main");
const bullets = document.querySelectorAll(".registration-main .bullets span");
const images = document.querySelectorAll(".registration-main .image");

inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});

function moveSlider() {
  let index = this.dataset.value;

  let currentImage = document.querySelector(`.img-${index}`);
  images.forEach((img) => img.classList.remove("show"));
  currentImage.classList.add("show");

  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${(-(index - 1) * 5)-1.2}rem)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  this.classList.add("active");
}

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});

//#endregion =========    End User Registration   ============ 


//#region ============    General Layout   ============ 
//#endregion =========    End General Layout   ============ 