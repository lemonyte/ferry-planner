// find elements
const input_origin = document.querySelector('#origin');
const input_destination = document.querySelector('#destination');
const loading_spinner = document.querySelector('#loading-spinner');
const message_card = document.querySelector('#message-card');
const tab_routes_timelines = document.querySelector('#tab-routes-timeline')
const schedule_card = document.querySelector('#schedule-card')
const schedule = document.querySelector('#schedule');
const schedule_table = document.querySelector('#schedule-table');
const tab_routes_table = document.querySelector('#tab-routes-table');
const routes_table = document.querySelector('#routes-table');
const routes_card = document.querySelector('#routes-card')
const button_submit = document.querySelector('#submit');
const input_date = document.querySelector('#date');
const timeline = document.querySelector('#timeline');
const debug = document.querySelector('#debug');
const sort_option = document.getElementById('sort-option');

sort_option.setAttribute("onchange", "sortPlans(this.value);");
// init sort options
routes_table.parentNode.querySelectorAll('th') // get all the table header elements
    .forEach((element, columnNo) => { // add a click handler for each 
        const sortBy = element.getAttribute('sort');
        if (sortBy) {
            element.addEventListener('click', event => sortPlans(sortBy));
            var opt = document.createElement("option");
            opt.text = element.textContent;
            opt.value = sortBy;
            sort_option.add(opt, null);
        }
    });

// add tooltip
d3.select('body')
    .append('div')
    .attr('id', 'tooltip')
    .attr('style', 'position: absolute; opacity: 0;')
    .attr('class', 'timeline-tooltip');
const tooltip = d3.select('#tooltip');

// globals
var plans;
var timelinesFilled;
var routesTableFilled;
var selectedRow = null;
var current_tab;
var current_sort = 'duration';
var tabs_state = {};
var locations = {};
var locations_to_id = {};
var location_names = [];
var message_hidden = true;

const activity_colors_map = {
    FREE: 'lightgreen',
    WAIT: 'lightgray',
    CAR: 'orange',
    FERRY: 'aqua  ',
    BUS: 'darkblue',
    AIR: 'aqua'
};

const activities_info = {
    FREE: {
        color: 'lightgreen',
        icon: '\uf118', // far fa-smile
        icon_class: 'fa',
    },
    WAIT: {
        color: 'lightgray',
        icon: '\uf017', // fa fa-clock-o, far fa-clock, fas fa-clock
        icon_class: 'fa',
    },
    CAR: {
        color: 'orange',
        icon: '\uf1b9', // fa/fas fa-car, fas fa-car-alt:f5de, fas fa-car-side:f5e4 directions_car:e531
        icon_class: 'fa',
    },
    FERRY: {
        color: 'aqua',
        icon: '\uf21a', // fa/fas fa-ship
        icon_class: 'fa',
    },
    BUS: {
        color: 'darkblue',
        icon: '\uf207', // fa/fas fa-bus
        icon_class: 'fa',
    },
    AIR: {
        color: 'lightblue',
        icon: '\uf072', // fa/fas fa-plane
        icon_class: 'fa',
    },
};

resetState();
loadLocations();

// initialize input controls
input_date.setAttribute('value', new Date().toJSON().slice(0, 10));
input_date.setAttribute('min', new Date().toJSON().slice(0, 10));
initInput(input_origin);
initInput(input_destination);

async function fetchApiData(request, body, method = 'GET') {
    try {
        // if (url_params)
        // request += '?' + new URLSearchParams(url_params)
        const fetchOptions = {
            method: method,
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' }
        }
        const response = await fetch('/api' + request, fetchOptions);
        return await response.json();
    } catch (error) {
        console.warn("Fetch error: " + error);
    }
}

// load locations list
async function loadLocations() {
    locations = await fetchApiData('/locations');
    for (const id in locations) {
        locations_to_id[locations[id]] = id;
    }

    location_names = Object.values(locations);
    location_names.sort((a, b) => a.localeCompare(b));

    var locations_list = document.getElementById('locations');
    for (const name of location_names) {
        var option = document.createElement('option');
        option.value = name;
        locations_list.appendChild(option);
    }
    await parseParams();
}

function initInput(input) {
    input.addEventListener('input', onInput);
    // input.setAttribute('temp', '');
    // input.setAttribute('onmouseover', 'this.temp=this.value; this.value="";');
    // input.setAttribute('onmouseout', 'this.value=this.temp;');
    input.addEventListener('input', onInput);
    input.addEventListener('focusout', autoComplete);
}

function onInput() {
    hideMessage();
}

function autoComplete(event) {
    var input = event.target;
    var value = input.value.trim();
    if (value != '' && !isValidLocation(value)) {
        var r = new RegExp(value, 'i');
        for (var name of location_names) {
            if (name.search(r) >= 0) {
                input.value = name;
                input.temp = name;
                onInput();
                break;
            }
        }
    }
}

async function getRoutePlans() {
    var options = {}
    for (var input of document.getElementsByTagName('input')) {
        var value = input.value;
        switch (input.type) {
            case 'text':
                value = locations_to_id[value];
                break;
            case 'number':
                value = parseInt(value);
                break;
            case 'checkbox':
                value = input.checked;
                break;
            case 'radio':
                value = input.checked;
                break;
        }
        options[input.id] = value;
    }
    // url = new URL(window.location);
    // for (var [key, value] in options) {
    //     if (url.searchParams.has(key))
    //         url.searchParams.set(key, value);
    //     else
    //         url.searchParams.append(key, value);
    // }
    // window.location = url
    plans = await fetchApiData('/routeplans', options, 'POST');
    for (var i = 0; i < plans.length; i++) {
        plans[i].id = i + 1;
    }
    return plans
}

function isValidLocation(name) {
    name = name.trim();
    return name != ' ' && name in locations_to_id;
}

async function parseParams() {
    var params = new URLSearchParams(window.location.search);
    var has_params;
    for (var param of params.entries()) {
        has_params = true;
        var e = document.getElementById(param[0]);
        if (e)
            e.value = param[1];
    }
    if (has_params) {
        autoComplete(input_origin);
        autoComplete(input_destination);
        await submit();
    }
}

function showMessage(heading, text, color) {
    message_card.hidden = false;
    message_hidden = false;
    if (!heading)
        heading = '';
    if (heading.length > 0)
        heading += ' : ';
    message_card.querySelector('#message-heading').textContent = heading;
    message_card.querySelector('#message-content').textContent = text;
    message_card.setAttribute('class', `w3-panel w3-card-4 w3-${color}`);
    // message_card.querySelector('#message-heading').setAttribute('class', `w3-container w3-${color}`);
}

function hideMessage() {
    if (message_hidden == true)
        return;
    message_hidden = true;
    message_card.hidden = true;
}

function showError(message) {
    showMessage("Error", message, 'red');
}

async function submit() {
    hideMessage();
    resetState();
    if (!isValidLocation(input_origin.value))
        showError("Please select start location");
    else if (!isValidLocation(input_destination.value))
        showError("Please select destination location");
    else if (input_origin.value == input_destination.value)
        showError("Start and destination location cannot be the same");
    else {
        try {
            loading_spinner.hidden = false;
            button_submit.disabled = true;
            plans = await getRoutePlans();
            if (!plans)
                showError("Failed to fetch schedule information");
            else if (plans.length == 0)
                showMessage("", "No itineraries found. Try select another date and/or locations.", "yellow");
            else {
                for (var plan of plans) {
                    var via = new Set();
                    for (var s of plan.segments) {
                        var lg = s.connection.origin.land_group;
                        if (lg) {
                            var pos = lg.indexOf(' (');
                            if (pos > 0)
                                lg = lg.substring(0, pos).trim();
                            via.add(lg);
                        }
                    }
                    plan.via = Array.from(via).splice(1, 1);
                }
                // force sort
                var sort = current_sort;
                current_sort = null;
                sortPlans(sort);
                // show routes
                routes_card.hidden = false;
                showTab('tab-routes-table');
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
    debug.textContent = '';
    routes_card.hidden = true;
    tab_routes_table.hidden = true;
    tab_routes_timelines.hidden = true;
    current_tab = null;
    tabs_state = {};
    schedule_card.hidden = true;
    plans = null;
    routesTableFilled = false;
    timelinesFilled = false;
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
    ampm = 'am';
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
        timeString = '1 day ';
    timeString += hours.toString().padStart(2, '0')
        + ':' + minutes.toString().padStart(2, '0');
    return timeString;
}

function onRowSelected(row, id) {
    for (var child of routes_table.children) {
        child.classList.remove('selected-row');
    }
    row.classList.add('selected-row')
    onPlanSelected(id);
}

function updateRoutesTable() {
    if (tab_routes_table.hidden)
        return;
    if (tabs_state.routes_table_sort == current_sort)
        return;
    tabs_state.routes_table_sort = current_sort;

    // clear table
    while (routes_table.firstChild)
        routes_table.removeChild(routes_table.firstChild);

    for (var i = 0; i < plans.length; i++) {
        plan = plans[i];

        var tr = document.createElement('tr');
        tr.setAttribute('onclick', `javascript:onRowSelected(this,${plan.id});`);
        tr.classList.add('routes-table-row');

        var td = document.createElement('td');
        td.textContent = `Route ${plan.id}`
        tr.appendChild(td);

        var td = document.createElement('td');
        td.classList.add('w3-center');
        td.textContent = timeToString(plan.depart_time);
        tr.appendChild(td);

        var td = document.createElement('td');
        td.classList.add('w3-center')
        td.textContent = timeToString(plan.arrive_time)
        tr.appendChild(td)

        var td = document.createElement('td');
        td.classList.add('w3-center');
        td.textContent = durationToString(plan.duration * 1000);
        tr.appendChild(td)

        var td = document.createElement('td');
        td.classList.add('w3-center');
        td.textContent = durationToString(plan.driving_duration * 1000);
        tr.appendChild(td)


        var td = document.createElement('td');
        td.classList.add('w3-center');
        td.textContent = `${plan.driving_distance.toFixed(1)} km`;
        tr.appendChild(td)


        var td = document.createElement('td');
        td.classList.add('w3-center');
        td.textContent = plan.via.join(',');
        tr.appendChild(td)

        routes_table.appendChild(tr);
    }
}

function updateTimelines() {
    if (tab_routes_timelines.hidden)
        return;
    var current_coloring = document.getElementById('color-option').value;
    if (tabs_state.timelines_sort == current_sort && tabs_state.timelines_coloring == current_coloring)
        return;
    tabs_state.timelines_sort = current_sort;
    tabs_state.timelines_coloring = current_coloring;
    d3.select('#timeline').select('svg').remove();
    //debug.textContent = JSON.stringify(plans, null, 2);
    var chartRows = [];
    var coloring_keys = new Set();
    for (var plan of plans) {
        chartRow = {
            label: `Route ${plan.id}`,
            times: []
        }
        var location;
        var land_group;
        for (var s of plan.segments) {
            for (var t of s.times) {
                var label = '';
                var segment_type = t.type == 'TRAVEL' ? s.connection.type : t.type;
                var activity_info = activities_info[segment_type];
                if (location == null || t.type == 'TRAVEL') {
                    if (location != s.connection.destination) {
                        location = s.connection.destination;
                        land_group = location.land_group;
                        if (land_group == undefined) {
                            land_group = null;
                            if (location.address.indexOf('Island') > 0 || location.name.indexOf('Island') > 0)
                                land_group = 'Islands';
                        }
                        if (land_group && land_group.indexOf('(') > 0)
                            land_group = land_group.substring(0, land_group.indexOf('(')).trim();

                        //label = location.id.length == 3 ? location.id : location.name;
                    }
                }
                if (activity_info.icon)
                    label = `<tspan class="${activity_info.icon_class}">${activity_info.icon}<tspan>` + label;

                var t2 = {
                    description: t.description,
                    segment_type: segment_type,
                    starting_time: new Date(t.start).getTime(),
                    ending_time: new Date(t.end).getTime()
                };
                if (label.length > 0) {
                    t2.label = ''; // just a placeholder now, will be replaced with _label later
                    t2._label = label;
                }
                var color_key = current_coloring == 'activity' ? segment_type : land_group;
                if (color_key != null) {
                    coloring_keys.add(color_key);
                    t2._color = color_key;
                }
                if (t.end == t.start) {
                    t2.display = 'circle';
                    t2._label = ''; // don't show labels for start/finish 
                    chartRow.times.splice(0, 0, t2);
                }
                else {
                    chartRow.times.push(t2);
                }
            }
        }
        chartRows.push(chartRow);
    }


    var chart = d3.timeline();

    var colorScale;
    if (current_coloring == 'activity')
        colorScale = d3.scale.ordinal().range(Object.values(activity_colors_map)).domain(Object.keys(activity_colors_map));
    else
        colorScale = d3.scale.ordinal().range(d3.scale.category20().range()).domain(Array.from(coloring_keys));

    var chart = d3.timeline()
        .colors(colorScale)
        .colorProperty('_color')
        .showAxisTop()
        .margin({ left: 90, right: 10, top: 10, bottom: 10 })
        .tickFormat({
            format: d3.time.format('%I %p'),
            tickTime: d3.time.hours,
            tickInterval: 3,
            tickSize: 1
        })
        .stack();

    var width = document.querySelector('#timeline').clientWidth - 40; // FIXME: magic number
    var svg = d3.select('#timeline').append('svg').attr('width', width)
        .datum(chartRows)
        .call(chart);

    updateLegend(chart, coloring_keys, current_coloring, document.getElementById('timeline-legend'));

    svg.selectAll('.timeline-label')
        .html((d, i) => {
            return `<a href="javascript:onPlanSelected(${plans[i].id});" class="button2" style="fill:blue;border: 3px solid red;filter: drop-shadow();">Route ${plans[i].id}</a>`;
        });

    svg.selectAll('text')
        .style('cursor', 'default')
    [0].forEach((e) => {
        assignTooltip(e);
        var d = e.__data__;
        if (d && d._label)
            e.innerHTML = d._label;

        //if (e.getClientRects()[0].width < e.textLength.baseVal.value)
        //    e.innerHTML = '';
    });
    svg.selectAll('rect')
    [0].forEach((e) => assignTooltip(e));
    svg.selectAll('tspan')
    [0].forEach((e) => assignTooltip(e));
}

function updateLegend(chart, coloring_keys, current_coloring, legend_element) {
    coloring_keys = Array.from(coloring_keys);
    var colorsRange = chart.colors().range();
    var colorsDomain = chart.colors().domain();
    var legend = "Legend: ";
    for (var i = 0; i < colorsRange.length && i < coloring_keys.length; i++) {
        n = colorsDomain.indexOf(coloring_keys[i]);
        c = colorsRange[n];
        legend += `<span>&nbsp;&nbsp;`;
        legend += `<div style="display:inline-block;height:1em;width:1em;vertical-align:middle;background-color:${c}">&nbsp;</div>&nbsp;`;
        if (current_coloring == 'activity') {
            var activity_info = activities_info[coloring_keys[i]];
            legend += `<span class="${activity_info.icon_class}">${activity_info.icon}</span>`;
        }
        legend += `&nbsp;${coloring_keys[i]}</span>`;
    }
    legend_element.innerHTML = legend;
}

function assignTooltip(e) {
    e.onmousemove = (e) => {
        var n = e.target;
        if (n.nodeName == 'tspan')
            n = n.parentNode;
        if (n.nodeName == 'text')
            n = n.parentNode;
        var r = n.getBoundingClientRect();
        console.log(r);
        tooltip
            .style('left', (r.x + window.scrollX) + 'px')
            .style('top', (r.bottom + + window.scrollY + 3) + 'px');
    };
    e.onmouseout = (e) => {
        tooltip
            .transition()
            .duration(100)
            .style('opacity', 0);
    };
    e.onmouseover = (e) => {
        var o = e.target.__data__;
        if (!o)
            o = e.target.parentNode.__data__;
        if (!o || !o.description)
            return;
        //var r = n.getBoundingClientRect();
        tooltip
            .html(timeToString(o.starting_time) + ' ' + o.description)
            .transition()
            .duration(100)
            //.style('left', (r.x) + 'px')
            //.style('top', (r.bottom + 3) + 'px')
            .style('opacity', 1);
    };
}

function onPlanSelected(id) {
    schedule_card.hidden = false;
    var plan = plans.find(p => p.id == id);
    document.getElementById('rid').value = plan.hash;

    // clear table
    while (schedule_table.firstChild)
        schedule_table.removeChild(schedule_table.firstChild);

    // schedule.appendChild(node = document.createElement('div').className('schedule-header'));
    document.getElementById('schedule-header').textContent = `${plan.segments[0].connection.origin.name} to ${plan.segments.slice(-1)[0].connection.destination.name}`
    // schedule.appendChild(node = document.createElement('div').className('schedule-via'));
    document.getElementById('schedule-via').textContent = 'via ' + [...new Set(plan.segments.slice(0, -1).map(s => s.connection.destination.name))].join(', ');

    document.getElementById('schedule-details').innerHTML =
        `Route ${plan.id}.` +
        ` Total time: <strong>${durationToString(plan.duration * 1000)}</strong>,` +
        ` driving distance ${plan.driving_distance.toFixed(1)} km.`;
    // ` <a href="${plan.map_url}" target="_blank">View on Google Maps</a>`;
    var schedule_map = document.getElementById('schedule-map');
    if (plan.map_url && plan.map_url.length > 0) {
        schedule_map.href = plan.map_url;
        schedule_map.hidden = false;
    }
    else {
        schedule_map.hidden = true;
    }

    for (var s of plan.segments) {
        for (var t of s.times) {
            var tr = document.createElement('tr');
            schedule_table.appendChild(tr);

            var td = document.createElement('td');
            td.classList.add('w3-center');
            td.innerHTML = timeToString(t.start).replace(' ', '&nbsp;');
            tr.appendChild(td);

            var desc = t.description;
            if (s.schedule_url && t.type == 'TRAVEL')
                desc += ` <a class="w3-button w3-right w3-border w3-round-medium" style="padding:1px 8px!important" href="${s.schedule_url}" target="_blank"><i class="fa fa-list-alt"></i>&nbsp;Schedule</a>`;
            var td = document.createElement('td');
            td.innerHTML = desc;
            tr.appendChild(td);

            var duration = new Date(t.end) - new Date(t.start);

            var td = document.createElement('td');
            td.classList.add('w3-center');
            td.textContent = duration > 0 ? durationToString(duration) : '--';
            tr.appendChild(td);
        }
    }
    schedule_card.scrollIntoView({ block: 'start', inline: 'nearest', behavior: 'smooth' });
}

function sortPlans(sortBy) {
    if (sortBy == current_sort)
        return;
    plans.sort((a, b) => {
        if (a[sortBy] > b[sortBy])
            return 1;
        return -1;
    });
    current_sort = sortBy;
    sort_option.value = sortBy;
    updateTabsData();
}

function updateTabsData() {
    updateRoutesTable();
    updateTimelines();
}

function showTab(id) {
    if (current_tab) {
        if (current_tab.id == id)
            return;
        current_tab.hidden = true;
    }
    current_tab = document.getElementById(id);
    current_tab.hidden = false; // .style.display = 'block'/'none';
    updateTabsData();
}

function toggleShow(id) {
    var e = document.getElementById(id);
    e.hidden = !e.hidden;
}

function onPrint(card) {
    routes_card.classList.add('no-print');
    schedule_card.classList.add('no-print');
    document.getElementById(card).classList.remove('no-print');
    print();
}
