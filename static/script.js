// globals
let plans;
let timelinesFilled;
let routesTableFilled;
let currentTab;
let currentSort = "duration";
let locations = {};
let locationsToId = {};
let locationNames = [];
let messageHidden = true;
let tooltip;
let currentPlan;

// elements
const elements = {
  body: document.getElementsByTagName("body"),
  inputForm: document.querySelector("#input-form"),
  inputOrigin: document.querySelector("#origin"),
  inputDestination: document.querySelector("#destination"),
  inputDate: document.querySelector("#date"),
  buttonSubmit: document.querySelector("#submit"),
  loadingSpinner: document.querySelector("#loading-spinner"),
  messageCard: document.querySelector("#message-card"),
  routesCard: document.querySelector("#routes-card"),
  routesTable: document.querySelector("#routes-table"),
  // schedule: document.querySelector('#schedule'),
  scheduleCard: document.querySelector("#schedule-card"),
  scheduleTable: document.querySelector("#schedule-table"),
  timeline: document.querySelector("#timeline"),
  sortOption: document.querySelector("#sort-option"),
  tabRoutesTable: document.querySelector("#tab-routes-table"),
  tabRoutesTimelines: document.querySelector("#tab-routes-timeline"),
  tabRoutesTableHeaderRow: document.querySelector("#tab-routes-table-header-row"),
  debug: document.querySelector("#debug"),
};

const columns = {
  Route: "id",
  "Depart Time": "depart_time",
  "Arrival Time": "arrive_time",
  "Total Time": "duration",
  "Driving Time": "driving_duration",
  "Driving Distance": "driving_distance",
  Via: "via",
};

let tabsState = {
  routesTableSort: currentSort,
  columnsCount: columnsCount(),
  timelinesSort: currentSort,
  timelinesColoring: document.getElementById("color-option").value,
  screenWidth: screen.width,
};

const activityColorsMap = {
  FREE: "lightgreen",
  WAIT: "lightgray",
  CAR: "orange",
  FERRY: "aqua",
  BUS: "darkblue",
  AIR: "aqua",
};

const activitiesInfo = {
  FREE: {
    color: "lightgreen",
    icon: "\uf118", // far fa-smile
    iconClass: "fa",
  },
  WAIT: {
    color: "lightgray",
    icon: "\uf017", // fa fa-clock-o, far fa-clock, fas fa-clock
    iconClass: "fa",
  },
  CAR: {
    color: "orange",
    icon: "\uf1b9", // fa/fas fa-car, fas fa-car-alt:f5de, fas fa-car-side:f5e4 directions_car:e531
    iconClass: "fa",
  },
  FERRY: {
    color: "aqua",
    icon: "\uf21a", // fa/fas fa-ship
    iconClass: "fa",
  },
  BUS: {
    color: "darkblue",
    icon: "\uf207", // fa/fas fa-bus
    iconClass: "fa",
  },
  AIR: {
    color: "lightblue",
    icon: "\uf072", // fa/fas fa-plane
    iconClass: "fa",
  },
};

function showMessage(heading, text, color) {
  elements.messageCard.hidden = false;
  messageHidden = false;
  if (!heading) heading = "";
  if (heading.length > 0) heading += ": ";
  elements.messageCard.querySelector("#message-heading").textContent = heading;
  elements.messageCard.querySelector("#message-content").textContent = text;
  elements.messageCard.setAttribute("class", `w3-panel w3-card-4 w3-${color}`);
  debug.textContent = `${debug.textContent}${heading}${text}\n`; 
}

function hideMessage() {
  if (messageHidden == true) return;
  messageHidden = true;
  elements.messageCard.hidden = true;
}

function showError(message) {
  showMessage("Error", message, "red");
  console.error(message);
}

function showWarning(message) {
  showMessage("Warning", message, "yellow");
  console.warn(message);
}

function resetState() {
  elements.routesCard.hidden = true;
  elements.scheduleCard.hidden = true;
  elements.tabRoutesTable.hidden = true;
  elements.tabRoutesTimelines.hidden = true;
  tabsState = {};
  currentTab = null;
  plans = null;
  routesTableFilled = false;
  timelinesFilled = false;
}

async function fetchApiData(request, body, method = "GET") {
  const fetchOptions = {
    method: method,
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  };
  const response = await fetch("/api" + request, fetchOptions);
  // if (response.type) // FIXME: check if valid json
  const responseJson = await response.json();
  if (!response.ok) {
    msg = response.statusText;
    if (responseJson && responseJson.detail) msg += " " + JSON.stringify(responseJson.detail);
    throw new Error(msg);
  }
  return responseJson;
}

async function loadLocations() {
  locations = await fetchApiData("/locations");
  for (const id in locations) {
    locationsToId[locations[id]] = id;
  }

  locationNames = Object.values(locations);
  locationNames.sort((a, b) => a.localeCompare(b));

  const locationsList = document.getElementById("locations");
  for (const name of locationNames) {
    const option = document.createElement("option");
    option.value = name;
    locationsList.appendChild(option);
  }

  // parse parameters from URL
  const options = urlToOptions(window.location);
  await applyOptions(options);
}

function initInput(input) {
  input.addEventListener("input", onInput);
  input.addEventListener("focusout", (event) => {
    autoComplete(event.target);
  });
}

function onInput() {
  hideMessage();
}

function autoComplete(input) {
  const value = input.value.trim();
  if (value != "" && !isValidLocation(value)) {
    let locationName = value;
    if (value in locations) {
      locationName = locations[value];
    } else {
      const r = new RegExp(value, "i");
      for (const name of locationNames) {
        if (name.search(r) >= 0) {
          locationName = name;
          break;
        }
      }
    }
    if (locationName != value) {
      input.value = locationName;
      onInput();
    }
  }
}

function getOptions(excludeDefaults) {
  let options = {};
  for (const input of document.getElementsByTagName("input")) {
    const value = inputValue(input);
    if (excludeDefaults == true && value == input.default) continue;
    options[input.id] = value;
  }
  if (currentPlan) options["hash"] = currentPlan.hash;
  return options;
}

async function applyOptions(options) {
  let changed = false;
  let hash = "";
  for (const o in options) {
    const value = options[o];
    if (value == undefined) continue;
    if (o == "hash") {
      // will apply later below
      hash = value;
      continue;
    }
    const element = document.getElementById(o);
    if (!element) {
      console.warn("Unknown option: " + o);
      continue;
    }
    const currentValue = inputValue(element);
    if (value == currentValue) continue;

    switch (element.type) {
      case "checkbox":
      case "radio":
        element.checked = value;
        break;
      case "text":
        element.value = value;
        autoComplete(element);
        break;
      default:
        element.value = value;
    }
    changed = true;
  }
  //if (changed) await submit();
  await goto(hash);
}

function optionsToUrl(options, url) {
  if (!options) options = getOptions(true);
  if (!url) url = new URL(window.location);
  url.search = "";
  url.hash = "";
  for (const key in options) {
    const value = options[key];
    if (value != undefined && value != null) {
      if (key == "hash") {
        if (value != "") url.hash = value;
      } else {
        url.searchParams.append(key, value);
      }
    }
  }
  return url;
}

function urlToOptions(url) {
  if (url instanceof Location) url = new URL(url.href);
  else if (url instanceof string) url = new URL(url);
  else if (url instanceof URL);
  else throw new Error("Unexpected url type:" + typeof url);

  let options = {};
  for (const param of url.searchParams.entries()) options[param[0]] = param[1];
  if (url.hash != "") options["hash"] = url.hash;

  return options;
}

function saveHistory(options, hash) {
  if (!options) options = getOptions(true);
  if (hash) options['hash'] = hash;
  url = optionsToUrl(options);

  // don't push duplicate states
  if (url.href == window.location.href) return;

  history.pushState(options, null, url);
}

async function goto(hash,clickEvent) {
  console.log(`goto: ${hash}`);
    
  if (!hash) hash = "";
  if (hash.length > 0 && hash[0] == "#") hash = hash.substring(1);

  if (clickEvent && clickEvent.ctrlKey)
  {
    let url = new URL(window.location);
    url.hash = hash;
    window.open(url, "_blank").focus();
    return;
  }

  hideMessage();
  
  if (hash != "")
  {
    if (plans == null) await submit();
    if (plans != null)
    {
      if (hash == "routes")
      {
      }
      else
      {
        const plan = plans.find((p) => p.hash == hash);
        if (plan) {
          onPlanSelected(plan.id);
        } else {
          showWarning("The route specified in link is not found or not valid anymore.");
          hash = "routes";
        }
      }
    }
  }

  if (plans == null) hash = "";
  if (hash == "") currentPlan = null;
 
  // mark selected row in routes table
  for (const row of elements.routesTable.children) {
    row.classList.remove("selected-row");
    if (currentPlan && row.plan == currentPlan) row.classList.add("selected-row");
  }

  elements.scheduleCard.hidden = (currentPlan == null || hash == "routes");
  elements.routesCard.hidden = (hash != "routes");
  elements.inputForm.hidden = (hash != "");  

  //if (window.location.hash != hash)
  //  window.location.hash = hash;
  saveHistory(null, hash);
}

async function getRoutePlans() {
  currentPlan = null;
  let options = getOptions();
  plans = await fetchApiData("/routeplans", options, "POST");

  // pre-process plans data
  for (let i = 0; i < plans.length; i++) {
    let plan = plans[i];
    plan.id = i + 1;
    let via = new Set();
    for (const s of plan.segments) {
      let lg = s.connection.origin.land_group;
      if (lg) {
        const pos = lg.indexOf(" (");
        if (pos > 0) lg = lg.substring(0, pos).trim();
        via.add(lg);
      }
    }
    if (via.size < 2) plan.via = Array.from(via);
    if (via.size > 1) plan.via = [Array.from(via)[1]];
    plan.origin = plan.segments[0].connection.origin;
    plan.destination = plan.segments.slice(-1)[0].connection.destination;
  }

  return plans;
}

function isValidLocation(name) {
  name = name.trim();
  return name != " " && name in locationsToId;
}

async function submit() {
  hideMessage();
  resetState();
  if (!isValidLocation(elements.inputOrigin.value)) showError("Please select start location");
  else if (!isValidLocation(elements.inputDestination.value)) showError("Please select destination location");
  else if (elements.inputOrigin.value == elements.inputDestination.value)
    showError("Start and destination location cannot be the same");
  else {
    try {
      elements.loadingSpinner.hidden = false;
      elements.buttonSubmit.disabled = true;
      plans = await getRoutePlans();
      if (!plans) showError("Failed to fetch schedule information");
      else if (plans.length == 0)
        showMessage("", "No itineraries found. Try select another date and/or locations.", "yellow");
      else {
        // force sort
        const sort = currentSort;
        currentSort = null;
        sortPlans(sort);
        // show routes
        elements.routesCard.hidden = false;
        showTab("tab-routes-table");
      }
    } catch (error) {
      showError(error.message);
    } finally {
      elements.loadingSpinner.hidden = true;
      elements.buttonSubmit.disabled = false;
    }
  }
}

function secondsToString(seconds) {
  dateObj = new Date(seconds * 1000);
  hours = dateObj.getUTCHours();
  minutes = dateObj.getUTCMinutes();
  seconds = dateObj.getSeconds();
  let timeString =
    hours.toString().padStart(2, "0") +
    ":" +
    minutes.toString().padStart(2, "0") +
    ":" +
    seconds.toString().padStart(2, "0");
  return timeString;
}

function timeToString(time, roundSeconds = true) {
  const dateObj = new Date(time);
  if (roundSeconds) dateObj.setSeconds(0);
  return dateObj.toLocaleTimeString().toLowerCase().replace(":00 ", "");
  // hours = dateObj.getHours();
  // minutes = dateObj.getMinutes();
  // ampm = "am";
  // if (hours >= 12) {
  //   hours -= 12;
  //   ampm = "pm";
  // }
  // if (hours == 0) hours = 12;
  // const timeString = hours.toString().padStart(2, "0") + ":" + minutes.toString().padStart(2, "0") + ampm;
  // return timeString;
}

function durationToString(time) {
  dateObj = new Date(time);
  days = Math.floor(dateObj.getTime() / 60 / 60 / 24 / 1000);
  hours = dateObj.getUTCHours();
  minutes = dateObj.getUTCMinutes();
  seconds = dateObj.getUTCSeconds();
  timeString = "";
  if (days < 1) timeString = "";
  else if (days >= 2) timeString = `${days} days `;
  else timeString = "1 day ";
  timeString += hours.toString().padStart(2, "0") + ":" + minutes.toString().padStart(2, "0");
  return timeString;
}

function columnsCount() {
  const w = window.outerWidth;
  if (w > 600) return 7;
  if (w > 500) return 6;
  if (w > 400) return 5;
  return 4;
}

function updateRoutesTable() {
  if (elements.tabRoutesTable.hidden) return;
  if (tabsState.routesTableSort == currentSort && tabsState.columnsCount == columnsCount()) return;
  tabsState.routesTableSort = currentSort;
  tabsState.columnsCount = columnsCount();

  let headerRowHtml = "";
  let c = 0;
  for (const k in columns) {
    if (c++ == tabsState.columnsCount) break;
    headerRowHtml += `<th class="w3-center hover-underline" onclick="sortPlans('${columns[k]}')">${k}</th>`;
  }
  elements.tabRoutesTableHeaderRow.innerHTML = headerRowHtml;

  // clear table
  while (elements.routesTable.firstChild) elements.routesTable.removeChild(elements.routesTable.firstChild);

  for (let i = 0; i < plans.length; i++) {
    const plan = plans[i];

    let tr = document.createElement("tr");
    tr.setAttribute("onclick", `javascript: goto(this.plan.hash, event);`);
    tr.classList.add("routes-table-row");
    tr.plan = plan;

    let td;
    td = document.createElement("td");
    td.textContent = `Route ${plan.id}`;
    tr.appendChild(td);

    td = document.createElement("td");
    td.classList.add("w3-center");
    td.innerHTML = timeToString(plan.depart_time);
    tr.appendChild(td);

    td = document.createElement("td");
    td.classList.add("w3-center");
    td.innerHTML = timeToString(plan.arrive_time);
    tr.appendChild(td);

    td = document.createElement("td");
    td.classList.add("w3-center");
    td.innerHTML = durationToString(plan.duration * 1000);
    tr.appendChild(td);

    if (tabsState.columnsCount > 4) {
      td = document.createElement("td");
      td.classList.add("w3-center");
      td.innerHTML = durationToString(plan.driving_duration * 1000);
      tr.appendChild(td);
    }

    if (tabsState.columnsCount > 5) {
      td = document.createElement("td");
      td.classList.add("w3-center");
      td.textContent = `${plan.driving_distance.toFixed(1)} km`;
      tr.appendChild(td);
    }

    if (tabsState.columnsCount > 6) {
      td = document.createElement("td");
      td.classList.add("w3-center");
      td.textContent = plan.via.join(",");
      tr.appendChild(td);
    }

    elements.routesTable.appendChild(tr);
  }
}

function updateTimelines() {
  if (elements.tabRoutesTimelines.hidden) return;
  const currentColoring = document.getElementById("color-option").value;
  if (
    tabsState.timelinesSort == currentSort &&
    tabsState.timelinesColoring == currentColoring &&
    tabsState.screenWidth == screen.width
  )
    return;
  tabsState.timelinesSort = currentSort;
  tabsState.timelinesColoring = currentColoring;
  tabsState.screenWidth = screen.width;
  d3.select("#timeline").select("svg").remove();
  let chartRows = [];
  let coloringKeys = new Set();
  for (const plan of plans) {
    let chartRow = {
      label: `Route ${plan.id}`,
      times: [],
    };
    let location;
    let landGroup;
    for (const s of plan.segments) {
      for (const t of s.times) {
        let label = "";
        const segmentType = t.type == "TRAVEL" ? s.connection.type : t.type;
        const activityInfo = activitiesInfo[segmentType];
        if (location == null || t.type == "TRAVEL") {
          if (location != s.connection.destination) {
            location = s.connection.destination;
            landGroup = location.land_group;
            if (landGroup == undefined) {
              landGroup = null;
              if (location.address.indexOf("Island") > 0 || location.name.indexOf("Island") > 0) landGroup = "Islands";
            }
            if (landGroup && landGroup.indexOf("(") > 0)
              landGroup = landGroup.substring(0, landGroup.indexOf("(")).trim();

            //label = location.id.length == 3 ? location.id : location.name;
          }
        }
        if (activityInfo.icon) label = `<tspan class="${activityInfo.iconClass}">${activityInfo.icon}<tspan>` + label;

        const t2 = {
          description: t.description,
          segmentType: segmentType,
          startingTime: new Date(t.start).getTime(),
          endingTime: new Date(t.end).getTime(),
        };
        if (label.length > 0) {
          t2.label = ""; // just a placeholder now, will be replaced with _label later
          t2._label = label;
        }
        const colorKey = currentColoring == "activity" ? segmentType : landGroup;
        if (colorKey != null) {
          coloringKeys.add(colorKey);
          t2._color = colorKey;
        }
        if (t.end == t.start) {
          t2.display = "circle";
          t2._label = ""; // don't show labels for start/finish
          chartRow.times.splice(0, 0, t2);
        } else {
          chartRow.times.push(t2);
        }
      }
    }
    chartRows.push(chartRow);
  }

  let colorScale;
  if (currentColoring == "activity") {
    colorScale = d3.scaleOrdinal().range(Object.values(activityColorsMap)).domain(Object.keys(activityColorsMap));
  } else {
    colorScale = d3.scaleOrdinal().range(d3.scaleOrdinal(d3.schemeAccent).range()).domain(Array.from(coloringKeys));
  }

  let chart = d3
    .timeline()
    .colors(colorScale)
    .colorProperty("_color")
    .showAxisTop()
    .margin({ left: 90, right: 10, top: 10, bottom: 10 })
    .tickFormat({
      format: d3.timeFormat("%I %p"),
      tickTime: d3.timeHours,
      tickInterval: 3,
      tickSize: 1,
    })
    .stack();

  const width = elements.timeline.clientWidth - 40; // FIXME: magic number
  const svg = d3.select("#timeline").append("svg").attr("width", width).datum(chartRows).call(chart);

  updateLegend(chart, coloringKeys, currentColoring, document.getElementById("timeline-legend"));

  svg.selectAll(".timeline-label").html((d, i) => {
    return `<a href="#${plans[i].hash}" class="button2" style="fill:blue;border: 3px solid red;filter: drop-shadow();">Route ${plans[i].id}</a>`;
  });

  svg
    .selectAll("text")
    .style("cursor", "default")
    ._groups[0].forEach((e) => {
      assignTooltip(e);
      const d = e.__data__;
      if (d && d._label) e.innerHTML = d._label;
      //if (e.getClientRects()[0].width < e.textLength.baseVal.value)
      //    e.innerHTML = '';
    });

  svg.selectAll("rect")._groups[0].forEach((e) => assignTooltip(e));
  svg.selectAll("tspan")._groups[0].forEach((e) => assignTooltip(e));
}

function updateLegend(chart, coloringKeys, currentColoring, legendElement) {
  coloringKeys = Array.from(coloringKeys);
  const colorsRange = chart.colors().range();
  const colorsDomain = chart.colors().domain();
  let legend = "Legend: ";
  for (let i = 0; i < colorsRange.length && i < coloringKeys.length; i++) {
    n = colorsDomain.indexOf(coloringKeys[i]);
    c = colorsRange[n];
    legend += `<span>&nbsp;&nbsp;`;
    legend += `<div style="display:inline-block;height:1em;width:1em;vertical-align:middle;background-color:${c}">&nbsp;</div>&nbsp;`;
    if (currentColoring == "activity") {
      const activityInfo = activitiesInfo[coloringKeys[i]];
      legend += `<span class="${activityInfo.iconClass}">${activityInfo.icon}</span>`;
    }
    legend += `&nbsp;${coloringKeys[i]}</span>`;
  }
  legendElement.innerHTML = legend;
}

function assignTooltip(element) {
  if (!tooltip) tooltip = d3.select("#tooltip");
  element.onmousemove = (event) => {
    let n = event.target;
    if (n.nodeName == "tspan") n = n.parentNode;
    if (n.nodeName == "text") n = n.parentNode;
    const rect = n.getBoundingClientRect();
    tooltip.style("left", rect.x + window.scrollX + "px").style("top", rect.bottom + +window.scrollY + 3 + "px");
  };
  element.onmouseout = (event) => {
    tooltip.transition().duration(100).style("opacity", 0);
  };
  element.onmouseover = (event) => {
    let o = event.target.__data__;
    if (!o) o = event.target.parentNode.__data__;
    if (!o || !o.description) return;
    //const rect = n.getBoundingClientRect();
    tooltip
      .html(timeToString(o.startingTime) + " " + o.description)
      .transition()
      .duration(100)
      //.style('left', (rect.x) + 'px')
      //.style('top', (rect.bottom + 3) + 'px')
      .style("opacity", 1);
  };
}


function onPlanSelected(id) {
  elements.scheduleCard.hidden = false;
  const plan = plans.find((p) => p.id == id);
  currentPlan = plan;

  // clear table
  while (elements.scheduleTable.firstChild) {
    elements.scheduleTable.removeChild(elements.scheduleTable.firstChild);
  }

  // schedule.appendChild(node = document.createElement('div').className('schedule-header'));
  document.getElementById("schedule-header").textContent = `${plan.origin.name} to ${plan.destination.name}`;
  // schedule.appendChild(node = document.createElement('div').className('schedule-via'));
  document.getElementById("schedule-via").textContent =
    "via " + [...new Set(plan.segments.slice(0, -1).map((s) => s.connection.destination.name))].join(", ");

  const depart_time = new Date(plan.depart_time.substring(0, 16));
  document.getElementById("schedule-details").innerHTML =
    `Route ${plan.id}.` +
    ` Departing:&nbsp;<strong>${depart_time.toDateString()} at ${timeToString(depart_time)}</strong>.` +
    ` Total time:&nbsp;<strong>${durationToString(plan.duration * 1000)}</strong>.` +
    ` Driving distance:&nbsp;${plan.driving_distance.toFixed(1)} km.`;
  // ` <a href="${plan.map_url}" target="_blank">View on Google Maps</a>`;
  const scheduleMap = document.getElementById("schedule-map");
  if (plan.map_url && plan.map_url.length > 0) {
    scheduleMap.href = plan.map_url;
    scheduleMap.hidden = false;
  } else {
    scheduleMap.hidden = true;
  }

  for (const s of plan.segments) {
    for (const t of s.times) {
      const tr = document.createElement("tr");
      elements.scheduleTable.appendChild(tr);

      let td;
      td = document.createElement("td");
      td.classList.add("w3-center");
      td.innerHTML = timeToString(t.start).replace(" ", "&nbsp;");
      tr.appendChild(td);

      let desc = t.description;
      if (s.schedule_url && t.type == "TRAVEL" && t.start != t.end)
        desc += ` <a class="w3-button w3-right w3-border w3-round-medium" style="padding:1px 8px!important" href="${s.schedule_url}" target="_blank"><i class="fa fa-list-alt"></i>&nbsp;Schedule</a>`;
      td = document.createElement("td");
      td.innerHTML = desc;
      tr.appendChild(td);

      const duration = new Date(t.end) - new Date(t.start);

      td = document.createElement("td");
      td.classList.add("w3-center");
      td.textContent = duration > 0 ? durationToString(duration) : "--";
      tr.appendChild(td);
    }
  }
  elements.scheduleCard.scrollIntoView({
    block: "start",
    inline: "nearest",
    behavior: "smooth",
  });
}

function sortPlans(sortBy) {
  if (sortBy == currentSort) return;
  plans.sort((a, b) => {
    if (a[sortBy] >= b[sortBy]) return 1;
    return -1;
  });
  currentSort = sortBy;
  elements.sortOption.value = sortBy;
  updateTabsData();
}

function updateTabsData() {
  updateRoutesTable();
  updateTimelines();
}

function showTab(id) {
  if (currentTab) {
    if (currentTab.id == id) return;
    currentTab.hidden = true;
  }
  currentTab = document.getElementById(id);
  currentTab.hidden = false; // .style.display = 'block'/'none';
  updateTabsData();
}

function toggleShow(id) {
  const element = document.getElementById(id);
  element.hidden = !element.hidden;
}

function onPrint(card) {
  elements.routesCard.classList.add("no-print");
  elements.scheduleCard.classList.add("no-print");
  document.getElementById(card).classList.remove("no-print");
  print();
}

async function onShare() {
  try {
    const data = {
      url: window.location.href,
      title: "FerryPlanner link",
    };
    if (currentPlan) {
      const depart_time = new Date(currentPlan.depart_time);
      data.text = `Route from ${currentPlan.origin.name} to ${
        currentPlan.destination.name
      } departing on ${depart_time.toDateString()} at ${timeToString(depart_time)}`;
    } else {
      data.text = `Routes from ${elements.inputOrigin.text} to ${elements.destination.text} on ${new Date(
        elements.inputDate.value
      ).toDateString()}`;
    }

    if (!window.navigator.canShare) throw new Error("Browser doesn't support sharing");
    if (!window.navigator.canShare(data)) throw new Error("Browser cannot share data");
    await window.navigator.share(data);
  } catch (e) {
    await navigator.clipboard.writeText(window.location.href);
    alert("Link copied to clipboard.");
  }
}

function pad(num, size) {
  num = num.toString();
  while (num.length < size) num = "0" + num;
  return num;
}

// DEPRECATED
// onorientationchange = (event) => {
//   updateTabsData();
// };

function inputValue(input) {
  const value = input.value;
  switch (input.type) {
    case "text":
      if (value in locationsToId) return locationsToId[value];
      return value;
    case "number":
      return parseInt(value);
    case "checkbox":
    case "radio":
      return input.checked;
  }
  return value;
}

function init()
{
  window.addEventListener('error', (event) => {
    showMessage(event.type, event.message, 'red');
  });
  
  screen.orientation.onchange = (event) => {
    updateTabsData();
  };

  window.onresize = () => {
    updateTabsData();
  };

  window.onhashchange = (e) => {
    goto(new URL(e.newURL).hash);
  };

  window.onpopstate = (e) => {
    if (e.state)
      applyOptions(e.state);
  };

  resetState();
  loadLocations();

  // initialize input controls
  {
    const d = new Date();
    const today = `${d.getFullYear()}-${pad(d.getMonth() + 1, 2)}-${pad(d.getDate(), 2)}`;
    elements.inputDate.setAttribute("value", today);
    elements.inputDate.setAttribute("min", today);
    initInput(elements.inputOrigin);
    initInput(elements.inputDestination);
    for (const input of document.getElementsByTagName("input")) {
      input.default = inputValue(input);
    }
  }

  // initialize sort options
  elements.sortOption.setAttribute("onchange", "sortPlans(this.value);");
  for (const k in columns) {
    const opt = document.createElement("option");
    opt.text = k;
    opt.value = columns[k];
    elements.sortOption.add(opt, null);
  }
}

init();