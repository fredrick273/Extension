// Function to check if the URL is a phishing site
async function checkPhishUrl(url) {
    try {
        let response = await fetch("http://127.0.0.1:8000/api/phishurl/", {
            method: "POST",
            body: JSON.stringify({
                'url': url
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const msg = await response.json();
        console.log(msg.result)
        if (msg.result == '-1'){
            
           alert("Warning Phishing page")
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// Get the current URL
const currentUrl = window.location.href;

// Call the function to check the current URL for phishing
checkPhishUrl(currentUrl);
