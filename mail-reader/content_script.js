console.log('mail active');

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    console.log(
      sender.tab
        ? "from a content script:" + sender.tab.url
        : "from the extension"
    );
    var temp_var = document.getElementsByClassName("a3s");
    if (temp_var){
   
    checkmail(temp_var[0].textContent);
    var ele = document.getElementsByClassName("hj");
if (ele.length > 0) {
    var p = document.createElement('p');
    p.textContent = "Scam";
    // Assuming you want to append to the first element in the collection:
    ele[0].appendChild(p);
    console.log(ele);
}

    }

  });



// if (temp_var){
//     console.log(temp_var)
// }


async function checkmail(content="") {
  console.log(content)
  try {
    let response = await fetch("http://127.0.0.1:8000/api/emailscan/",{
      method: "POST",
      body: JSON.stringify({
        'mail': content
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const msg = await response.json();
    console.log(msg);
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
}
