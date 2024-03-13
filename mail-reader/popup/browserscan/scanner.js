const container = document.querySelector('#container');
const buttonScan = document.querySelector('#scanbutton');

async function checkid(id) {
    try {
        let response = await fetch("http://127.0.0.1:8000/api/extension/", {
            method: "POST",
            body: JSON.stringify({
                'id': id
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const msg = await response.json();
        console.log(msg.result);
        if (msg.result == -1){
            return true;
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return false;
    }
    return false;
}

buttonScan.addEventListener('click', async () => {
    chrome.management.getAll(async function(extensions) {
        for (const extension of extensions) {
            let d = document.createElement('div');
            let a = document.createElement('p');
            a.innerText = extension.name;
            d.appendChild(a);
    
            // Wait for the asynchronous checkid function to complete
            const isPhishing = await checkid(extension.id);
            
            if(isPhishing) {
                d.style.backgroundColor = 'red';
            }
    
            let b = document.createElement('button');
            b.innerText = 'Uninstall';
            d.append(b);
            container.appendChild(d);
            console.log(extension);
            // Corrected event handling for the onclick event
            b.onclick = async () => {
                try {
                    await chrome.management.uninstall(extension.id, { showConfirmDialog: true });
                    console.log('Extension uninstalled successfully');
                    // Remove the div element from the container after uninstalling
                    container.removeChild(d);
                } catch (error) {
                    console.error('Error uninstalling extension:', error);
                }
            };
        }
    });
});
