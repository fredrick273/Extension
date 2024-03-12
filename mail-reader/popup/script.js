document.getElementById("temp-mail").addEventListener('click', function() {
    window.location.href = "tempmail/temp-mail.html"
});


document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var tab = tabs[0];
        var url = tab.url;

        fetch('http://127.0.0.1:8000/api/phishurl/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: JSON.stringify({
                'url': url
            }),
        })
        .then(response => response.text())
        .then(data => {
            console.log('Server response:', data);
            if (data == '1') {
                alert('Suspicious');
                console.log('1');
            } else if (data == '0') {
                console.log('0');
            } else if (data == '-1') {
                chrome.notifications.create({
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "Phishing Alert",
                    message: "This page may be a phishing website.",
                });
                alert('Phishing');
                console.log('-1');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    });
});
