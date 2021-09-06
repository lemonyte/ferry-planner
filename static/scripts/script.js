async function getData(request) {
    try {
        var response = await fetch(request);
        return await response.json();
    }
    catch (error) {
        console.error("Fetch error: " + error);
    }
}

async function populateTerminalList(terminals, fromTerminalList, toTerminalList) {
    for (var terminal in terminals) {
        var option = document.createElement("option");
        option.value = terminal;
        option.innerHTML = terminals[terminal].name;
        fromTerminalList.appendChild(option);
        var option = document.createElement("option");
        option.value = terminal;
        option.innerHTML = terminals[terminal].name;
        toTerminalList.appendChild(option);
    }
    return terminals;
}

async function getSchedule(terminals, fromTerminal, toTerminal) {
    route = terminals[fromTerminal].id + "-" + terminals[toTerminal].id;
    return await getData("schedule/route=" + route + "&date=" + "07/07/2021");
}

async function main() {
    var fromTerminalList = document.getElementById("fromTerminalList");
    var toTerminalList = document.getElementById("toTerminalList");
    var terminals = await getData("terminals");


    var testArea = document.createElement("pre");
    testArea.appendChild(document.createTextNode(JSON.stringify(terminals, null, 4)));
    document.body.appendChild(testArea);


    populateTerminalList(terminals, fromTerminalList, toTerminalList);
    toTerminalList.value = "Westview";
    var schedule = await getSchedule(terminals, fromTerminalList.value, toTerminalList.value);
    
    
    var testArea = document.createElement("pre");
    testArea.appendChild(document.createTextNode(JSON.stringify(schedule, null, 4)));
    document.body.appendChild(testArea);
}

main();