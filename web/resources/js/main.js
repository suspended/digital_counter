$(document).ready(function(){
    setNumber();
    setInterval(setNumber, 1500);
});

function setNumber(){
    let num = Math.floor(Math.random() * 100);
    let counterDiv = document.getElementById("counter");

    counterDiv.innerHTML = num;
    if(num > 80){
        counterDiv.style.color = "red";
    }else if(num > 50){
        counterDiv.style.color = "orange";
    }else {
        counterDiv.style.color = "green";
    }

}
