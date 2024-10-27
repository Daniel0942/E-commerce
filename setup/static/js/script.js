//Deixar as mensagens flash temporarias
let msgFlash = document.getElementsByClassName("msg-flash")

setTimeout(() => {
    Array.from(msgFlash).forEach(element => {
        element.style.display = 'none';
    });
}, 3000);

// funcionalidade menu 
let menu = document.getElementById("menu")

menu.addEventListener("click", ()=> {
    menu.classList.add("abrirMenu")
})