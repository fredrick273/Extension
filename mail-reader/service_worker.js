console.log("Background working");

// self.addEventListener('fetch',(event)=>{
//     const url = event.request.url;
//     console.log(url);
// })

async function getTab() {
    let queryOptions = { active: true, currentWindow: true };
    let tabs = await chrome.tabs.query(queryOptions);
    return tabs[0].url;
  }

chrome.tabs.onUpdated.addListener(async function () {
    console.log("TAB UPDATED")
    let url = await getTab()
    console.log(url)
})

