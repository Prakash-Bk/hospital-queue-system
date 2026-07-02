console.log("Hospital Queue Management Loaded");

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

card.addEventListener("mouseenter", () => {

card.style.background = "#e8f4ff";

});

card.addEventListener("mouseleave", () => {

card.style.background = "white";

});

});
const addDoctor=document.getElementById("addDoctor");

if(addDoctor){

addDoctor.onclick=function(){

alert("Doctor Added Successfully");

}

}

const resetQueue=document.getElementById("resetQueue");

if(resetQueue){

resetQueue.onclick=function(){

alert("Queue Reset Successfully");

}

}

const deleteButtons=document.querySelectorAll(".delete-btn");

deleteButtons.forEach(button=>{

button.addEventListener("click",function(){

alert("Patient Deleted");

});

});

const loginForm=document.getElementById("loginForm");

if(loginForm){

loginForm.addEventListener("submit",function(e){

e.preventDefault();

let username=document.getElementById("username").value;

let password=document.getElementById("password").value;

if(username=="" || password==""){

alert("Please fill all fields");

return;

}

alert("Login Successful");

});

}