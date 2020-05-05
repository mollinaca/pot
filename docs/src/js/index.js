// index.js
// called at last of index.html </body>

//------------------------
// Global Variables
//------------------------
const API_ENDPOINT = 'https://mollinaca.github.io/pot/api/'
//latestFilename = undefined;
//let latest_log = undefined;


//------------------------
// Functions
//------------------------

// window.onload initialize
function init() {
    console.log ("init()")

    let metadata = new XMLHttpRequest();
    let metadata_url = API_ENDPOINT + 'metadata.json'
    console.log(`21: ${metadata_url}`)
    metadata.open('GET', metadata_url, true);
    metadata.responseType = 'json';
    metadata.onload = function() {
        let json = this.response;
        let latestFilename = json.metadata.ssh.latest;
        console.log(`25: ${latestFilename}`)
        jsonbox_name.innerHTML = "latest log: " + "<a href=\"" + API_ENDPOINT + latestFilename + "\">" + API_ENDPOINT + latestFilename + "</a>";

        let log = new XMLHttpRequest();
        let log_url = API_ENDPOINT + latestFilename
        console.log (log_url)
        log.open('GET', log_url, true);
        log.responseType = 'json';
        log.onload = function () {
            let jsonbox_body = document.getElementById('jsonbox_body');
            let json = JSON.stringify(this.response, null, '\t');
            jsonbox_body.innerHTML = json;
        };
        log.send();
    }
    metadata.send();
}


///-----------------------

window.onload = init;

