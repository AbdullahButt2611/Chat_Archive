//#region ============    General Layout   ============ 
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
//#endregion =========    End General Layout   ============ 


//#region ============    General Layout   ============ 
//#endregion =========    End General Layout   ============ 