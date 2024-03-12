// // background.js

console.log("Background script working");

function DOMtoString(selector) {
    var temp_var = document.getElementsByClassName("a3s");
    return temp_var[0].textContent;
}

async function getTab() {
    let queryOptions = { active: true, currentWindow: true };
    let tabs = await chrome.tabs.query(queryOptions);
    return tabs[0].url;
}

chrome.tabs.onUpdated.addListener(async function (tabId, changeInfo, tab) {
    console.log("TAB UPDATED");
    
    let url = await getTab();
    console.log(url);
    if (url.startsWith("https://mail.google.com/")) {   
       console.log("mail url")
       try{
       chrome.tabs.sendMessage(tab.id, { message: "Check scam" });
       } catch(err){
        console.log(err);
       }
    }

});

