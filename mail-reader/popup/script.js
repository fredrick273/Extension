document.getElementById("mailbutton").addEventListener('click', async function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var activeTab = tabs[0];
        var activeTabId = activeTab.id;

        chrome.scripting.executeScript({
            target: { tabId: activeTabId },
            function: DOMtoString,
        }).then((result) => {
            var user_mail = result[0].result;
            console.log(user_mail);
        });
    });
});

function DOMtoString(selector) {
    var temp_var = document.getElementsByClassName("a3s");
    return temp_var[0].textContent;
}