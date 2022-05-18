// find elements
var input_from = document.querySelector('#from');
var input_to = document.querySelector('#to');
var message_card = document.querySelector('#message-card');
var timeline_panel = document.querySelector('#timeline-panel')
var button_submit = document.querySelector('#submit');
var input_date = document.querySelector('#date');
input_date.setAttribute("value", new Date().toJSON().slice(0, 10));
input_date.setAttribute("min", new Date().toJSON().slice(0, 10));

var is_hidden;

function optionsClick() {
    var x = document.querySelector('#options');
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

function autoComplete(o) {
    var value = o.value.trim();
    if (value != " " && !is_valid_location(value)) {
        var r = new RegExp(value, "i");
        for (var name in locations_names) {
            if (name.search(r) >= 0) {
                o.value = name;
                o.temp = name;
                on_input(null);
                break;
            }
        }
    }
}

async function getData(request, url_params) {
    try {
        if (url_params)
            request += '?' + new URLSearchParams(url_params)
        var response = await fetch('/api' + request);
        return await response.json();
    } catch (error) {
        console.warn("Fetch error: " + error);
    }
}

async function getRoutePlans() {
    url_params = {}
    for (var input of document.getElementsByTagName('input')) {
        var value = input.value;
        switch (input.type) {
            case "text":
                value = locations_names[value];
                break;
            case "checkbox":
                value = input.checked;
                break;
        }
        url_params[input.id] = value;
        //console.log(input.id + ": " + value);
    }
    return await getData("/routeplans", url_params);
}

// load locations list
var locations = {};
var locations_names = {};
(async () => {
    locations = await getData("/locations");
    var list = document.getElementById('locations');
    for (var id in locations) {
        name = locations[id];
        locations_names[name] = id;
        var option = document.createElement('option');
        option.value = name;
        list.appendChild(option);
    };
})();

var message_hidden = true;

function showMessage(heading, text, color) {
    message_card.hidden = false;
    message_hidden = false;
    if (!heading)
        heading = '';
    if (heading.length > 0)
        heading += ' : ';
    message_card.querySelector("#message-heading").textContent = heading;
    message_card.querySelector("#message-content").textContent = text;
    message_card.setAttribute("class", `w3-panel w3-card-4 w3-${color}`);
    // message_card.querySelector("#message-heading").setAttribute("class", `w3-container w3-${color}`);
}

function hideMessage() {
    if (message_hidden == true)
        return;
    message_hidden = true;
    message_card.hidden = true;
}

function showError(message) {
    showMessage('Error', message, 'red');
}

async function submit() {
    timeline_panel.hidden = true;
    if (!is_valid_location(input_from.value))
        showError('Please select start location');
    else if (!is_valid_location(input_to.value))
        showError('Please select destination location');
    else if (input_from.value == input_to.value)
        showError('Start and destination location cannot be the same');
    else {
        loading = document.getElementById('loading');
        try {
            showMessage("Loading...", "Please wait", "blue");
            loading.hidden = false;
            button_submit.disabld = true;
            plans = await getRoutePlans();
            if (!plans) {
                showError("Failed to fetch schedule information");
            }
            else if (plans.length == 0) {
                showMessage("", "No itineraries found. Try select another date and/or locations.", "yellow ");
            }
            else {
                timeline_panel.hidden = false;
                drawChart(plans);
            }
        }
        catch (e) {
            showError(e.message);
        }
        finally {
            hideMessage();
            loading.hidden = true;
            button_submit.disabled = false;
        }
    }
}

function is_valid_location(name) {
    name = name.trim();
    return name != " " && name in locations_names;
}

function on_input() {
    hideMessage();
    //var valid = is_valid_location(input_from.value) && is_valid_location(input_to.value) && input_from.value != input_to.value;
    //button_submit.disabled = !valid;
};

function init_input(input) {
    input.addEventListener('input', on_input);
    input.setAttribute('temp', '');
    input.setAttribute('onmouseover', 'this.temp=this.value; this.value="";');
    input.setAttribute('onmouseout', 'this.value=this.temp;');
    input.setAttribute('onfocusin', 'on_input();');
    input.setAttribute('onfocusout', 'autoComplete(this);');
}

init_input(input_from);
init_input(input_to);

google.charts.load("current", {
    packages: ["timeline"]
});

function drawChart(data) {
    document.querySelector('#schedule').textContent = JSON.stringify(data, null, 2);
    var table = [];
    for (var i = 0; i < data.length; i++) {
        var rowName = "Itinerary " + (i + 1);
        var plan = data[i];
        for (var s of plan.segments) {
            for (var t of s.times) {
                style = "#000000";
                switch (t.type) {
                    case "FREE":
                        style = "color:green;";
                        break;
                    case "WAIT":
                        style = "#808080";
                        break;
                    case "TRAVEL":
                        switch (s.connection.type) {
                            case "CAR":
                                style = "color:orange;";
                                break;
                            case "FERRY":
                                style = "color:blue;";
                                break;
                            case "BUS":
                                style = "color:darkblue;";
                                break;
                            case "AIR":
                                style = "color:yellow;";
                                break;
                        }
                }
                table.push([rowName, s.connection.location_from.name, style, t.description, new Date(t.start), new Date(t.end)])
            }
        }
    }

    var container = document.getElementById("timeline");
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({
        type: "string",
        id: "Title"
    });
    dataTable.addColumn({
        type: "string",
        id: "Label"
    });
    dataTable.addColumn({
        type: "string",
        role: "style"
    });
    dataTable.addColumn({
        type: "string",
        role: "tooltip"
    });
    dataTable.addColumn({
        type: "date",
        id: "Start"
    });
    dataTable.addColumn({
        type: "date",
        id: "End"
    });
    dataTable.addRows(table);

    var options = {
        timeline: {
            tooltip: { isHtml: true },
            groupByRowLabel: true,
        }
    };

    var view = new google.visualization.DataView(dataTable);
    chart.draw(view, options);

    google.visualization.events.addListener(chart, 'select', () => {
        var sel = chart.getSelection();
        if (is_hidden == false)
            view.setRows([sel[0].row]);
        else
            view.setRows(0, dataTable.getNumberOfRows() - 1);
        is_hidden = !is_hidden;
        chart.draw(view, options);
    });
}