//#region ============    Menu   ============ 
    /*===== MENU SHOW Y HIDDEN =====*/ 
    const navMenu = document.querySelector('.header .nav'),
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
  textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  this.classList.add("active");
}

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});

//#endregion =========    End User Registration   ============ 


//#region ============    Sidebar   ============ 
$(".menu > ul > li").click(function (e) {
  // remove active from already active
  $(this).siblings().removeClass("active");

  // add active to clicked
  $(this).toggleClass("active");

  // if has sub menu open it
  $(this).find("ul").slideToggle();

  // close other sub menu if any open
  $(this).siblings().find("ul").slideUp();

  // remove active class of sub menu items
  $(this).siblings().find("ul").find("li").removeClass("active");
});

$(".menu-btn").click(function () {
  console.log($(".sidebar"))
  $(".sidebar").toggleClass("active");
});
//#endregion =========    End Sidebar   ============ 


//#region ============    Upload Chat    ============ 
let fileInput = document.querySelector('.contact-container .custum-file-upload input');
let fileName = document.querySelector('#file_name');
let submitBtn = document.querySelector('.addfriend-container form .button-container');
let loader = document.querySelector('.addfriend-container form .typewriter');
if(fileInput){
  fileInput.addEventListener('change', function(event){
    const file = event.target.files[0];
    if(file){
      fileName.innerText = file.name;
    }
    else{
      fileName.innerText = 'Click to upload image';
    }
  })
}

if (loader){
  submitBtn.addEventListener('click', () => {
    loader.style.display = 'block';
    setTimeout(() => {
      loader.style.display = 'none';
    }, 5000);
  })
}

//#endregion =========    End Upload Chat    ============ 


//#region ============    General    ============ 
//#endregion =========    End General    ============ 


