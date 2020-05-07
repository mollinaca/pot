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
//    console.log ("init()")

    let metadata = new XMLHttpRequest();
    let metadata_url = API_ENDPOINT + 'metadata.json'
//    console.log(`21: ${metadata_url}`)
    metadata.open('GET', metadata_url, true);
    metadata.responseType = 'json';
    metadata.onload = function() {
        let json = this.response;
        let latestFilename = json.metadata.ssh.latest;
//        console.log(`25: ${latestFilename}`)
        jsonbox_name.innerHTML = "latest log: " + "<a href=\"" + API_ENDPOINT + latestFilename + "\">" + API_ENDPOINT + latestFilename + "</a>";

        let log = new XMLHttpRequest();
        let log_url = API_ENDPOINT + latestFilename
//        console.log (log_url)
        log.open('GET', log_url, true);
        log.responseType = 'json';
        log.onload = function () {
            let jsonbox_body = document.getElementById('jsonbox_body');
            let res = this.response;
//            console.log(typeof res)
            jsonbox_body.innerHTML = JSON.stringify(res);

            let logs = res.logs;
//            console.log(json)
//            console.log(typeof logs)
//            console.log(logs)
//            console.log(typeof logsp)
//            console.log(logs[0])

            // summary
            let count_cc = 0;
            let count_iu = 0;
            let count_user = {};
            let count_ip = {};
            let ip_cc = {};

            Object.keys(logs).forEach(function(key) {
                ip = logs[key].ip;
                if (count_ip[ip]) {
                    count_ip[ip] += 1
                } else {
                    count_ip[ip] = 1
                };

                cc = logs[key].country;
//                console.log(cc)
                if (!ip_cc[ip]) {
                    ip_cc[ip] = cc
                }

                if (logs[key].log_type_sub == "Connection closed") {
                    count_cc += 1
                } else if (logs[key].log_type_sub == "Invalid user") {
                    count_iu += 1
                    user = logs[key].user
//                    console.log(user)
                    if (count_user[user]) {
                        count_user[user] += 1
                    } else {
                        count_user[user] = 1
                    };

                } else {
//                    console.log(logs[key].log_type_sub)
                };

            });

            // user を回数で sort
            let user_keys=[];
            for(var key in count_user)user_keys.push(key);
            function Compare(a,b){
                return count_user[b]-count_user[a];
            }
            user_keys.sort(Compare)

            // ip を回数で sort
//            console.log(count_ip)
            let ip_keys=[];
            for(var key in count_ip)ip_keys.push(key);
            function Compare(a,b){
                return count_ip[b]-count_ip[a];
            }
            ip_keys.sort(Compare)

            // table1
            let tablebox1 = document.getElementById('tablebox1');
            let table1_summary_html = "<table>";
            table1_summary_html += "<tr><th> サマリ <th></tr>";
            table1_summary_html += "<tr><td> ログ取得数 </td><td> " + logs.length + "</td></tr>";
            table1_summary_html += "<tr><td> Connection closed </td><td> " + count_cc + "</td></tr>";
            table1_summary_html += "<tr><td> Invalid user </td><td> " + count_iu + "</td></tr>";
            table1_summary_html += "</table>";
            tablebox1.innerHTML = table1_summary_html;

            // table2 ユーザ別
            let tablebox2 = document.getElementById('tablebox2');
            let table2_summary_html = "<table><tr><th> ユーザ名 </th><th> 試行回数 </th></tr>";
//            console.log("table2");
//            console.log(count_user);
            if (Object.keys(count_user).length > 3) {
                max = 3
            } else {
                max = Object.keys(count_user).length
            };
            for (let i = 0; i < max; i++) {
                table2_summary_html += "<tr><td> " + user_keys[i] + " </td><td> " + count_user[user_keys[i]] + " </td></tr>";
            }
            table2_summary_html += "</table>";
            tablebox2.innerHTML = table2_summary_html;

            // table3 IPアドレス別
            let tablebox3 = document.getElementById('tablebox3');
            let table3_summary_html = "<table><tr><th> IPアドレス </th><th> 試行回数 </th><th> 国コード </th></tr>";
//            console.log("table3");
//            console.log(count_ip);
            if (Object.keys(count_ip).length > 3) {
                max = 3
            } else {
                max = Object.keys(count_ip).length
            };
            for (let i = 0; i < max; i++) {
//                console.log (ip_keys[i])
                table3_summary_html += "<tr><td> " + ip_keys[i] + " </td><td> " + count_ip[ip_keys[i]] + " </td><td> " + ip_cc[ip_keys[i]] +"</td></tr>";
            }
            table3_summary_html += "</table>";
            tablebox3.innerHTML = table3_summary_html;

        };
        log.send();
    }
    metadata.send();
}

///-----------------------

window.onload = init;

