const container = document.querySelector('#container');

chrome.storage.sync.get(["key"], async function(result) {
    if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
    } else {
        if ("key" in result) {
            console.log("Key 'key' is present");
            // Do something if the key is present
            console.log(result.key);
            let response = await fetch('http://127.0.0.1:8000/api/usersub/'+result.key+'/');
            let data = await response.json();
            console.log(data);
            if(!data.result){
                let h = document.createElement('h2');
                h.innerText = "You have not subscribed yet would you like to subscribe?";
                container.appendChild(h)
                let b = document.createElement('button')
                b.addEventListener('click', ()=>{
                    window.location.replace("http://127.0.0.1:8000/api/transact/");
                })
                b.innerText = "Yes";
                container.appendChild(b);
                
            }
        } else {
            console.log("Key 'key' is not present");
            try {
                let response = await fetch('http://127.0.0.1:8000/api/gencode/');
                let data = await response.json();
                console.log("Generated code:", data.code);

                // Save the generated code in Chrome Storage
                chrome.storage.sync.set({ "key": data.code }, function() {
                    if (chrome.runtime.lastError) {
                        console.error(chrome.runtime.lastError.message);
                    } else {
                        console.log("Generated code saved in Chrome Storage");

                        // Redirect to the desired URL after saving the code
                        window.location.replace("http://127.0.0.1:8000/api/moralis_auth/");
                    }
                });

                // Do something with the generated code
            } catch (error) {
                console.error('Fetch error:', error);
            }
        }
    }
});
