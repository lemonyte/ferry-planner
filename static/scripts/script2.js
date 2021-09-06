async function getData(request) {
    try {
        var response = await fetch(request);
        return await response.json();
    }
    catch (error) {
        console.warn("Fetch error: " + error);
    }
}

function getTerminals() {
    //var terminals;
    //getData("terminals").then((data) => {terminals = data});
    var fromTerminal = document.getElementById("fromTerminal");
    var toTerminal = document.getElementById("toTerminal");
    for (var terminal in terminals) {
        var option = document.createElement("option");
        option.value = terminals[terminal];
        option.innerHTML = terminals[terminal].name;
        fromTerminal.appendChild(option);
        var option = document.createElement("option");
        option.value = terminals[terminal];
        option.innerHTML = terminals[terminal].name;
        toTerminal.appendChild(option);
    }
    return terminals;
}

function getSchedule(fromTerminal, toTerminal) {
    console.log(terminals)
    route = fromTerminal + "-" + toTerminal
    var schedule;
    getData("schedule/route=" + route + "&date=" + "07/07/2021").then((data) => {schedule = data})
    return schedule;
}

var terminals;
(async() => {
    terminals = await getData("terminals");
    console.log("inside async call")
    console.log(terminals)
})();
console.log("outside aysync call");
console.log(terminals);