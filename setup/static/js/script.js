//Deixar as mensagens flash temporarias
let msgFlash = document.getElementsByClassName("msg-flash")

setTimeout(() => {
    Array.from(msgFlash).forEach(element => {
        element.style.display = 'none';
    });
}, 3000);

// funcionalidade menu 
let abrirMenu = document.getElementById("abrir-menu")
let menu = document.getElementById("menu")
let fecharMenu = document.getElementById("fechar-menu")
let telaFundo = document.getElementsByClassName("tela-fundo")[0]

abrirMenu.addEventListener("click", ()=> {
    menu.classList.add("menu-JS")
})
fecharMenu.addEventListener("click", ()=> {
    menu.classList.remove("menu-JS")
})
telaFundo.addEventListener("click", ()=> {
    menu.classList.remove("menu-JS")
})
