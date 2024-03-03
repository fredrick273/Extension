const textinput = document.querySelector("#nameInput");
const displayText = document.querySelector("#name");

textinput.addEventListener('keyup',()=>{
displayText.innerText = textinput.value;
})