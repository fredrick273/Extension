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
                window.location.replace("http://127.0.0.1:8000/api/transact/");
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
