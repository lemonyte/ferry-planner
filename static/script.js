// find elements
var input_from = document.querySelector('#from');
var input_to = document.querySelector('#to');
var loading_spinner = document.querySelector('#loading-spinner');
var message_card = document.querySelector('#message-card');
var timeline_card = document.querySelector('#timeline-card')
var schedule_card = document.querySelector('#schedule-card')
var schedule = document.querySelector('#schedule');
var schedule_table = document.querySelector('#schedule-table');
var routes_card = document.querySelector('#routes-card');
var routes_table = document.querySelector('#routes-table');
makeTableSortable(routes_table.parentNode);
var button_submit = document.querySelector('#submit');
var input_date = document.querySelector('#date');
var timeline = document.querySelector('#timeline');
var debug = document.querySelector('#debug');

// add tooltip
d3.select('body')
    .append('div')
    .attr('id', 'tooltip')
    .attr('style', 'position: absolute; opacity: 0;')
    .attr('class', 'd3-tip');
var tooltip = d3.select('#tooltip');

// globals
var plans;
var selectedRow = null;
var colors_map = {
    'FREE': 'lightgreen',
    'WAIT': 'lightgray',
    'CAR': 'yellow',
    'FERRY': 'lightblue',
    'BUS': 'darkblue',
    'AIR': 'aqua'
}


// initialize input controls
input_date.setAttribute("value", new Date().toJSON().slice(0, 10));
input_date.setAttribute("min", new Date().toJSON().slice(0, 10));
initInput(input_from);
initInput(input_to);

function initInput(input) {
    input.addEventListener('input', onInput);
    input.setAttribute('temp', '');
    input.setAttribute('onmouseover', 'this.temp=this.value; this.value="";');
    input.setAttribute('onmouseout', 'this.value=this.temp;');
    input.setAttribute('onfocusin', 'on_input();');
    input.setAttribute('onfocusout', 'autoComplete(this);');
}

function onInput() {
    hideMessage();
};

function autoComplete(input) {
    var value = input.value.trim();
    if (value != " " && !isValidLocation(value)) {
        var r = new RegExp(value, "i");
        for (var name in locations_names) {
            if (name.search(r) >= 0) {
                input.value = name;
                input.temp = name;
                onInput();
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
    url = new URL(window.location);
    for (var [key, value] in url_params) {
        if (url.searchParams.has(key))
            url.searchParams.set(key, value);
        else
            url.searchParams.append(key, value);
    }
    // window.location = url
    plans = await getData("/routeplans", url_params);
    for (var i = 0; i < plans.length; i++) {
        plans[i].id = i + 1;
    }
    return plans
}

// load locations list
var locations = {};
var locations_names = {};
(async () => {
    locations = await getData("/locations");
    var list = document.getElementById('locations');
    for (var id in locations) {
        location_name = locations[id];
        locations_names[location_name] = id;
        var option = document.createElement('option');
        option.value = location_name;
        list.appendChild(option);
    };
    await parseParams();
})();

function isValidLocation(name) {
    name = name.trim();
    return name != " " && name in locations_names;
}


async function parseParams() {
    var params = new URLSearchParams(window.location.search);
    var has_params;
    for (var param of params.entries()) {
        has_params = true;
        var e = document.getElementById(param[0]);
        if (e) e.value = param[1];
    }
    if (has_params) {
        autoComplete(input_from);
        autoComplete(input_to);
        await submit();
    }
}

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
    resetState();
    if (!isValidLocation(input_from.value))
        showError('Please select start location');
    else if (!isValidLocation(input_to.value))
        showError('Please select destination location');
    else if (input_from.value == input_to.value)
        showError('Start and destination location cannot be the same');
    else {
        try {
            loading_spinner.hidden = false;
            button_submit.disabled = true;
            plans = await getRoutePlans();
            if (!plans) {
                showError("Failed to fetch schedule information");
            }
            else if (plans.length == 0) {
                showMessage("", "No itineraries found. Try select another date and/or locations.", "yellow");
            }
            else {
                timeline_card.hidden = false;
                for (var plan of plans) {
                    var via = new Set();
                    for (var s of plan.segments) {
                        var lg = s.connection.location_from.land_group;
                        if (lg) {
                            var pos = lg.indexOf(' (');
                            if (pos > 0)
                                lg = lg.substring(0, pos);
                            via.add(lg);
                        }
                    }
                    plan.via = Array.from(via);
                }
                fillRoutesTable(plans);
                drawChart(plans);
            }
        }
        catch (e) {
            showError(e.message);
        }
        finally {
            loading_spinner.hidden = true;
            button_submit.disabled = false;
        }
    }
}


function resetState() {
    debug.textContent = "";
    timeline_card.hidden = true;
    routes_card.hidden = true;
    schedule_card.hidden = true;
    plans = null;
}

function secondsToString(seconds) {
    dateObj = new Date(seconds * 1000);
    hours = dateObj.getUTCHours();
    minutes = dateObj.getUTCMinutes();
    seconds = dateObj.getSeconds();
    timeString = hours.toString().padStart(2, '0')
        + ':' + minutes.toString().padStart(2, '0')
        + ':' + seconds.toString().padStart(2, '0');
    return timeString;
}

function timeToString(time) {
    dateObj = new Date(time);
    hours = dateObj.getHours();
    minutes = dateObj.getMinutes();
    seconds = dateObj.getSeconds();
    ampm = 'am'
    if (hours >= 12) {
        hours -= 12;
        ampm = 'pm';
    }
    if (hours == 0)
        hours = 12;
    timeString = hours.toString().padStart(2, '0')
        + ':' + minutes.toString().padStart(2, '0')
        + ' ' + ampm;
    return timeString;
}

function durationToString(time) {
    dateObj = new Date(time);
    days = Math.floor(dateObj.getTime() / 60 / 60 / 24 / 1000);
    hours = dateObj.getUTCHours();
    minutes = dateObj.getUTCMinutes();
    seconds = dateObj.getUTCSeconds();
    timeString = '';
    if (days < 1)
        timeString = '';
    else if (days >= 2)
        timeString = `${days} days `;
    else
        timeString = '1 day '
    timeString += hours.toString().padStart(2, '0')
        + ':' + minutes.toString().padStart(2, '0');
    return timeString;
}

function onRowSelected(row, i) {
    console.log("clicked: " + i)
    $(routes_table).children().removeClass('selected-row');
    $(row).addClass('selected-row');
    onPlanSelected(i);
}

function fillRoutesTable(data) {
    // clear table
    while (routes_table.firstChild)
        routes_table.removeChild(routes_table.firstChild);

    for (var i = 0; i < data.length; i++) {
        plan = data[i];
        var tr = $('<tr/>').attr('onclick', `javascript:onRowSelected(this,${i});`);
        $('<td/>').html(`<a href="javascript:onPlanSelected(${i});">Route ${plan.id}</a> ${plan.segments.length}`).appendTo(tr);
        $('<td/>').addClass("w3-center").text(timeToString(plan.depart_time)).appendTo(tr);
        $('<td/>').addClass("w3-center").text(timeToString(plan.arrive_time)).appendTo(tr);
        $('<td/>').addClass("w3-center").text(durationToString(plan.duration * 1000)).appendTo(tr);
        // var drive_time = 0;
        var via = new Set();
        for (var s of plan.segments) {
            var lg = s.connection.location_from.land_group;
            if (lg) {
                var pos = lg.indexOf(' (');
                if (pos > 0)
                    lg = lg.substring(0, pos);
                via.add(lg);
            }
        }

        $('<td/>').addClass("w3-center").text(durationToString(plan.driving_time * 1000)).appendTo(tr);
        $('<td/>').addClass("w3-center").text(`${plan.driving_distance.toFixed(1)} km`).appendTo(tr);
        $('<td/>').addClass("w3-center").text(Array.from(via).splice(1, 1).join(',')).appendTo(tr);
        $(routes_table).append(tr);
    }
    routes_card.hidden = false;
}

function drawChart(data) {
    debug.textContent = JSON.stringify(data, null, 2);
    var chartRows = [];
    for (var i = 0; i < data.length; i++) {
        var plan = data[i];
        chartRow = {
            label: `Itinerary ${plan.id}`,
            times: []
        }
        var text;
        for (var s of plan.segments) {
            for (var t of s.times) {
                s_name = s.connection.location_from.id.length == 3 ? s.connection.location_from.id : s.connection.location_from.name;
                chartRow.times.push({
                    description: t.description,
                    label: s_name != text ? s_name : null,
                    name: s.connection.location_from.land_group,
                    segment_type: t.type == 'TRAVEL' ? s.connection.type : t.type,
                    starting_time: new Date(t.start).getTime(),
                    ending_time: new Date(t.end).getTime()
                });
                text = s_name;
                if (t.end == t.start)
                    chartRow.times[chartRow.times.length - 1].display = 'circle';
                //table.push([rowName, s.connection.location_from.name, style, t.description, new Date(t.start), new Date(t.end)])
            }
        }
        chartRows.push(chartRow);
    }
    var chart = d3.timeline();

    var colorScale = d3.scale.ordinal()
    // .range(Object.values(colors_map))
    // .domain(Object.keys(colors_map));
    var chart = d3.timeline()
        // .colors(colorScale)
        .colorProperty('name')
        .showAxisTop()
        .margin({ left: 90, right: 10, top: 10, bottom: 10 })
        .tickFormat({
            format: d3.time.format("%I %p"),
            tickTime: d3.time.hours,
            tickInterval: 3,
            tickSize: 1
        })
        .stack();

    d3.select("#timeline").select("svg").remove();

    var w = $("#timeline").width();
    var svg = d3.select("#timeline").append("svg").attr('width', w)
        .datum(chartRows)
        .call(chart);

    chart
        .hover((o, i, d) => {
            tooltip
                .style('left', (d3.event.pageX - 30) + 'px')
                .style('top', (d3.event.pageY + 10) + 'px');
        })
        .mouseout((o, i, d) => {
            tooltip
                .transition()
                .duration(100)
                .style('opacity', 0);
        })
        .mouseover((o, i, d) => {
            tooltip
                .html(timeToString(o.starting_time) + " " + o.description)
                .transition()
                .duration(100)
                .style('opacity', 1);
        });

    var c = svg
        .selectAll('.timeline-label')
        .html((d, i) => {
            return `<a href="javascript:onPlanSelected(${i});" class="button2" style="fill:blue;border: 3px solid red;filter: drop-shadow();">Route ${plan.id}</a>`;
        });
    svg.on('mouseleave', () => tooltip.style('opacity', 0));

}

function onPlanSelected(i) {
    schedule_card.hidden = false;
    //schedule_card.height = 1000;
    var plan = plans[i];

    // clear table
    while (schedule_table.firstChild)
        schedule_table.removeChild(schedule_table.firstChild);


    // var node;
    // schedule.appendChild(node = document.createElement('div').className('schedule-header'));
    document.getElementById('schedule-header').textContent = `${plan.segments[0].connection.location_from.name} to ${plan.segments.slice(-1)[0].connection.location_to.name}`
    // schedule.appendChild(node = document.createElement('div').className('schedule-via'));
    document.getElementById('schedule-via').textContent = 'via ' + [...new Set(plan.segments.slice(0, -1).map(s => s.connection.location_to.name))].join(", ");

    document.getElementById('schedule-details').innerHTML =
        `Route ${plan.id}.` +
        ` Total time: <strong>${durationToString(plan.duration * 1000)}</strong>,` +
        ` driving distance ${plan.driving_distance.toFixed(1)} km. <a href="${plan.maps_url}" target="_blank">View on Google Maps</a>`;

    for (var s of plan.segments) {
        for (var t of s.times) {
            var tr = $('<tr/>').appendTo(schedule_table);
            $('<td/>').addClass("w3-center").text(timeToString(t.start)).appendTo(tr);
            $('<td/>').text(t.description).appendTo(tr);
            var duration = new Date(t.end) - new Date(t.start);
            $('<td/>').addClass("w3-center").text(duration > 0 ? durationToString(duration) : "--").appendTo(tr);
        }
    }
}

function sortTable(sortBy) {
    plans.sort((a, b) => {
        if (a[sortBy] > b[sortBy])
            return 1;
        return -1;
    })
    fillRoutesTable(plans);
    drawChart(plans);
}

function makeTableSortable(table) {
    table.querySelectorAll('th') // get all the table header elements
        .forEach((element, columnNo) => { // add a click handler for each 
            element.addEventListener('click', event => {
                var sortBy = element.getAttribute('sort');
                if (!sortBy)
                    showMessage('', 'No sort property on ' + element.innerText, 'yellow')
                else
                    sortTable(sortBy);
            })
        });
}