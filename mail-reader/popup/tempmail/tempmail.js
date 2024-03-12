// tempmail.js

const mailcontainer = document.querySelector('#mail');
const inboxContainer = document.querySelector("#inbox-container");

let inbox = [];

async function showmail() {
    const response = await fetch("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1");
    const mail = await response.json();
    console.log(mail);
    mailcontainer.innerText = mail[0];
    setInterval(() => getmails(mail[0]), 5000);
}

async function getmails(mailid) {
    const maildetails = mailid.split("@");
    let url = "https://www.1secmail.com/api/v1/?action=getMessages&login=" + maildetails[0] + "&domain=" + maildetails[1];
    const response = await fetch(url);
    const data = await response.json();
    console.log(inbox);
    if (data.length > 0){
    getmailfromid(maildetails[0], maildetails[1], data[0].id);
    }
}

async function getmailfromid(user, domain, id) {
    let url = "https://www.1secmail.com/api/v1/?action=readMessage&login=" + user + "&domain=" + domain + "&id=" + id;
    const response = await fetch(url);
    const data = await response.json();
    if (!inbox.some(email => email.id === data.id)) {
        inbox.push(data);
        createMailBar(data);
    }
}

function createMailBar(email) {
    const mailBar = document.createElement('div'); // Changed from anchor to div element
    mailBar.classList.add('mail-bar');
    mailBar.onclick = function() {
        window.location.href = `mail_detail.html?subject=${encodeURIComponent(email.subject)}&sender=${encodeURIComponent(email.from)}&message=${encodeURIComponent(email.body)}`;
    }; // Redirect to mail_detail.html with email details
    
    mailBar.style.cursor = "pointer"; // Change cursor to indicate clickability
    
    const subject = document.createElement('p');
    subject.textContent = email.subject;
    mailBar.appendChild(subject);
    
    const sender = document.createElement('p');
    sender.textContent = 'From: ' + email.from;
    mailBar.appendChild(sender);
    
    inboxContainer.appendChild(mailBar);
}


document.addEventListener("DOMContentLoaded", showmail);
