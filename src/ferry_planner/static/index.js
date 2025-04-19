import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import { timeline } from "./d3-timeline.js";

// globals
let plans;
// let timelinesFilled;
// let routesTableFilled;
let currentTab;
let currentSort = "duration";
let locations = {};
const locationsToId = {};
let locationNames = [];
let messageHidden = true;
let currentPlan;

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
  scheduleTable: document.querySelector("#schedule-table-body"),
  timeline: document.querySelector("#timeline"),
  timelineSwitch: document.querySelector("#timeline-switch"),
  sortOption: document.querySelector("#sort-option"),
  tabRoutesTable: document.querySelector("#tab-routes-table"),
  tabRoutesTimelines: document.querySelector("#tab-routes-timeline"),
  tabRoutesTableHeaderRow: document.querySelector("#tab-routes-table-header-row"),
  debug: document.querySelector("#debug"),
  inputs: document.querySelector("#input-form").querySelectorAll("input, button"),
  tooltip: document.querySelector("#tooltip"),
};

const cards = [elements.inputForm, elements.routesCard, elements.scheduleCard];

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

function debug(text) {
  console.log(text);
  elements.debug.textContent = `${elements.debug.textContent}${text}\n`;
}

function showMessage(heading, text, theme) {
  window.createNotification({
    closeOnClick: true,
    displayCloseButton: false,
    positionClass: "nfc-top-right",
    onclick: false,
    showDuration: 3500,
    theme,
  })({
    title: heading,
    message: text,
  });
}

function hideMessage() {
  if (messageHidden === true) return;
  messageHidden = true;
  elements.messageCard.hidden = true;
}

function showError(message) {
  showMessage("Error", message, "error");
}

function showWarning(message) {
  showMessage("Warning", message, "warning");
}

function resetState() {
  elements.routesCard.hidden = true;
  elements.scheduleCard.hidden = true;
  elements.tabRoutesTable.hidden = true;
  elements.tabRoutesTimelines.hidden = true;
  tabsState = {};
  currentTab = null;
  plans = null;
  // routesTableFilled = false;
  // timelinesFilled = false;
}

async function fetchApiData(request, body, method = "GET") {
  if (!request.startsWith("/")) {
    request = `/${request}`;
  }
  const fetchOptions = {
    method,
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  };
  const response = await fetch(`/api${request}`, fetchOptions);
  if (!response.ok) {
    let msg = response.statusText;
    try {
      const responseJson = await response.json();
      if (responseJson?.detail) msg += ` ${JSON.stringify(responseJson.detail)}`;
    } finally {
      throw new Error(msg);
    }
  }
  return response.json();
}

async function loadLocations() {
  locations = await fetchApiData("/locations");

  for (const id in locations) {
    locationsToId[locations[id].name] = id;
  }

  locationNames = Object.values(locations).map((location) => location.name);
  locationNames.sort((a, b) => a.localeCompare(b));

  const locationsList = document.getElementById("locations");
  for (const name of locationNames) {
    const option = document.createElement("option");
    option.value = name;
    locationsList.appendChild(option);
  }
}

function initInput(input) {
  input.addEventListener("input", onInput);
  input.addEventListener("focusout", (event) => {
    autoComplete(event.target);
  });
  input.addEventListener("focusin", (event) => {
    event.target.setSelectionRange(0, event.target.value.length);
  });
}

function onInput() {
  hideMessage();
}

function escapeRegex(string) {
  return string.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
}

function autoComplete(input) {
  const value = input.value.trim();
  if (value !== "" && !isValidLocation(value)) {
    let locationName = value;
    if (value in locations) {
      locationName = locations[value].name;
    } else {
      // find name containing entered text, this is also the 1st shown in filtered drop down list
      const regexp = new RegExp(escapeRegex(value), "i");
      for (const name of locationNames) {
        if (name.search(regexp) >= 0) {
          locationName = name;
          break;
        }
      }
    }
    if (locationName !== value) {
      input.value = locationName;
      onInput();
    }
  }
}

function getOptions(excludeDefaults) {
  const options = {};
  for (const input of elements.inputForm.getElementsByTagName("input")) {
    const value = inputValue(input);
    const defaultValue = defaultInputValue(input);
    if (excludeDefaults === true && value === defaultValue) continue;
    options[input.id] = value;
  }
  if (currentPlan) options.hash = currentPlan.hash;
  return options;
}

async function applyOptions(options) {
  let changed = false;
  let hash = "";
  for (const o in options) {
    const value = options[o];
    if (value === undefined) continue;
    if (o === "hash") {
      // will apply later below
      hash = value;
      continue;
    }
    const element = document.getElementById(o);
    if (!element) {
      debug(`Unknown option: ${o}`);
      continue;
    }
    const currentValue = inputValue(element);
    if (`${value}` === `${currentValue}`) continue;

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
  // invalidate cached data
  if (changed) plans = null;
  await goto(hash);
}

function optionsToUrl(options, url) {
  if (!options) options = getOptions(true);
  if (!url) url = new URL(window.location);
  url.search = "";
  url.hash = "";
  for (const key in options) {
    const value = options[key];
    if (value !== undefined && value !== null) {
      if (key === "hash") {
        if (value !== "") url.hash = value;
      } else {
        url.searchParams.append(key, value);
      }
    }
  }
  return url;
}

function urlToOptions(url) {
  if (url instanceof Location) url = new URL(url.href);
  else if (typeof url === "string") url = new URL(url);
  else if (url instanceof URL);
  else throw new Error(`Unexpected url type: ${typeof url}`);

  const options = {};
  for (const param of url.searchParams.entries()) options[param[0]] = param[1];
  if (url.hash !== "") options.hash = url.hash;

  return options;
}

function trim(str, ch) {
  let start = 0;
  let end = str.length;
  while (start < end && str[start] === ch) ++start;
  while (end > start && str[end - 1] === ch) --end;
  return start > 0 || end < str.length ? str.substring(start, end) : str;
}

function trimEnd(str, ch) {
  let end = str.length;
  while (end > 0 && str[end - 1] === ch) --end;
  return end < str.length ? str.substring(0, end) : str;
}

function saveHistory(options, hash) {
  if (!options) options = getOptions(true);
  if (hash) options.hash = hash;
  const url = optionsToUrl(options);

  // don't push duplicate states
  if (trimEnd(url.href, "#") === trimEnd(window.location.href, "#")) {
    return;
  }

  history.pushState(options, null, url);
}

function validatePlans(options) {
  if (!plans || !plans.options) return false;
  for (const k in options) if (k !== "hash" && options[k] !== plans.options[k]) return false;
  for (const k in plans.options) if (k !== "hash" && options[k] !== plans.options[k]) return false;
  return true;
}

function welcomeClick() {
  const moreinfo = document.querySelector("#welcome-more-info");
  const button = document.querySelector("#welcome-more");
  const lastState = moreinfo.hidden;
  moreinfo.hidden = !lastState;
  button.textContent = `see ${lastState ? "less" : "more"}`;
}

function showElements(elements) {
  for (const c of cards) {
    const show = elements.includes(c);
    c.hidden = !show;
  }
}

export async function goto(hash, clickEvent) {
  menuClose();
  if (!hash) hash = "";
  if (hash.length > 0 && hash[0] === "#") hash = hash.substring(1);

  if (clickEvent?.ctrlKey) {
    const url = new URL(window.location);
    url.hash = hash;
    window.open(url, "_blank").focus();
    return;
  }

  hideMessage();
  const options = getOptions();
  if (!validatePlans(options)) plans = null;

  if (hash !== "") {
    if (plans === null) await fetchRoutes();
    if (plans !== null) {
      if (hash === "routes") {
        /* pass */
      } else {
        const plan = plans.find((p) => p.hash === hash);
        if (plan) {
          onPlanSelected(plan.id);
        } else {
          showWarning("The route specified in link is not found or not valid anymore.");
          hash = "routes";
        }
      }
    }
  }

  if (plans && plans.length === 0) plans = null;
  if (plans === null) hash = "";
  if (hash === "") currentPlan = null;

  // mark selected row in routes table
  for (const row of elements.routesTable.children) {
    row.classList.remove("selected-row");
    if (currentPlan && row.plan === currentPlan) row.classList.add("selected-row");
  }

  if (hash === "") {
    showElements([elements.inputForm]);
    document.title = "Ferry Planner";
  } else if (hash === "routes") {
    const depart_time = new Date(plans[0].depart_time.substring(0, 16));
    const cardHeader = document.createElement("div");
    cardHeader.className = "card-header";
    cardHeader.innerText = `${elements.inputOrigin.value} to ${elements.inputDestination.value}`;
    const cardHeaderDate = document.createElement("div");
    cardHeaderDate.className = "card-header-date";
    cardHeaderDate.innerText = depart_time.toDateString();
    const routesCardHeader = elements.routesCard.querySelector("#routes-card-header");
    routesCardHeader.innerText = "";
    routesCardHeader.appendChild(cardHeader).appendChild(cardHeaderDate);
    showElements([/*elements.inputForm,*/ elements.routesCard]);
    document.title = `${elements.inputOrigin.value} to ${
      elements.inputDestination.value
    } on ${depart_time.toDateString()}`;
  } else {
    showElements([elements.scheduleCard]);
    // window.scrollTo(0,0);
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "instant",
    });
    // elements.scheduleCard.scrollIntoView({
    //   block: "start",
    //   inline: "nearest",
    //   behavior: "smooth",
    // });
    document.title = `${elements.inputOrigin.value} to ${elements.inputDestination.value} on ${new Date(
      currentPlan.depart_time,
    ).toDateString()} at ${timeToString(currentPlan.depart_time)}`;
  }

  /*  elements.inputForm.hidden = hash !== "" && hash !== "routes";
  elements.routesCard.hidden = hash !== "routes";
  elements.scheduleCard.hidden = currentPlan === null || hash === "routes";
*/
  //if (window.location.hash !== hash) {
  //  window.location.hash = hash;
  // }
  saveHistory(null, hash);
}

async function getRoutePlans() {
  currentPlan = null;
  const options = getOptions();
  plans = await fetchApiData("/routeplans", options, "POST");
  plans.options = options;

  // pre-process plans data
  const land_groups = new Set();
  for (let i = 0; i < plans.length; i++) {
    const plan = plans[i];
    plan.id = i + 1;
    const via = new Set();
    for (const s of plan.segments) {
      if (s.connection.type === "FERRY") {
        let lg = s.connection.destination.land_group;
        if (lg) {
          const pos = lg.indexOf(" (");
          if (pos > 0) lg = lg.substring(0, pos).trim();
          land_groups.add(lg);
          via.add(lg);
        }
      }
    }
    plan.via = Array.from(via);
    if (plan.via.length > 1) plan.via.pop();
    plan.origin = plan.segments[0].connection.origin;
    plan.destination = plan.segments.slice(-1)[0].connection.destination;
  }

  // delete "via" that are common for all routes
  land_groups.forEach((lg) => {
    if (Array.from(plans).every((p) => p.via.includes(lg))) {
      plans.forEach((p) => {
        if (p.via.length > 1) p.via = p.via.filter((l) => l !== lg);
      });
    }
  });

  return plans;
}

function isValidLocation(name) {
  name = name.trim();
  return name !== " " && name in locationsToId;
}

export async function submit() {
  await goto("routes");
}

async function fetchRoutes() {
  hideMessage();
  resetState();
  saveHistory();
  if (!isValidLocation(elements.inputOrigin.value)) showMessage("", "Please select start location", "warning");
  else if (!isValidLocation(elements.inputDestination.value)) showWarning("Please select destination location");
  else if (elements.inputOrigin.value === elements.inputDestination.value) {
    showError("Start and destination location cannot be the same");
  } else {
    try {
      elements.inputForm.hidden = true;
      elements.loadingSpinner.hidden = false;
      //for (const element of elements.inputs) element.disabled = true;
      plans = await getRoutePlans();
      if (!plans) showError("Failed to fetch schedule information");
      else if (plans.length === 0) {
        showMessage("", "No itineraries found. Try select another date and/or locations.", "warning");
        plans = null;
      } else {
        // force sort
        const sort = currentSort;
        currentSort = null;
        sortPlans(sort);
        // show routes
        elements.routesCard.hidden = false;
        showTab(elements.timelineSwitch.checked ? "tab-routes-timeline" : "tab-routes-table");
      }
    } catch (error) {
      showError(error.message);
    } finally {
      elements.loadingSpinner.hidden = true;
      //for (const element of elements.inputs) element.disabled = false;
    }
  }
}

function secondsToString(seconds) {
  const dateObj = new Date(seconds * 1000);
  const hours = dateObj.getUTCHours();
  const minutes = dateObj.getUTCMinutes();
  seconds = dateObj.getSeconds();
  const timeString = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
  return timeString;
}

function timeToString(time, roundSeconds = true) {
  const dateObj = new Date(time);
  if (roundSeconds) dateObj.setSeconds(0);
  return dateObj.toLocaleTimeString("en-CA", {
    hour: "2-digit",
    minute: "2-digit",
  }).toLowerCase();
  // let hours = dateObj.getHours();
  // const minutes = dateObj.getMinutes();
  // let ampm = "am";
  // if (hours >= 12) {
  //   hours -= 12;
  //   ampm = "pm";
  // }
  // if (hours === 0) hours = 12;
  // const timeString = hours.toString().padStart(2, "0") + ":" + minutes.toString().padStart(2, "0") + ampm;
  // return timeString;
}

function durationToString(time) {
  const dateObj = new Date(time);
  const days = Math.floor(dateObj.getTime() / 60 / 60 / 24 / 1000);
  const hours = dateObj.getUTCHours();
  const minutes = dateObj.getUTCMinutes();
  let timeString = "";
  if (days < 1) timeString = "";
  else if (days >= 2) timeString = `${days} days `;
  else timeString = "1 day ";
  timeString += `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;
  return timeString;
}

function columnsCount() {
  const width = window.outerWidth;
  if (width > 600) return 7;
  if (width > 500) return 6;
  if (width > 400) return 5;
  return 4;
}

function updateRoutesTable() {
  if (elements.tabRoutesTable.hidden) return;
  if (tabsState.routesTableSort === currentSort && tabsState.columnsCount === columnsCount()) return;
  tabsState.routesTableSort = currentSort;
  tabsState.columnsCount = columnsCount();

  let headerRowHtml = "";
  let c = 0;
  for (const k in columns) {
    if (c++ === tabsState.columnsCount) break;
    headerRowHtml += `<th onclick="exports.sortPlans('${columns[k]}')">${k}</th>`;
  }
  elements.tabRoutesTableHeaderRow.innerHTML = headerRowHtml;

  // clear table
  while (elements.routesTable.firstChild) elements.routesTable.removeChild(elements.routesTable.firstChild);

  for (let i = 0; i < plans.length; i++) {
    const plan = plans[i];

    const tr = document.createElement("tr");
    tr.setAttribute("onclick", "exports.goto(this.plan.hash, event);");
    tr.classList.add("routes-table-row");
    tr.plan = plan;
    if (new Date(plan.depart_time) < Date.now() - 60000) {
      tr.classList.add("past-route");
    }

    let td = document.createElement("td");
    td.innerHTML = `Route&nbsp;${plan.id}`;
    tr.appendChild(td);

    td = document.createElement("td");
    td.innerHTML = timeToString(plan.depart_time);
    tr.appendChild(td);

    td = document.createElement("td");
    td.innerHTML = timeToString(plan.arrive_time);
    tr.appendChild(td);

    td = document.createElement("td");
    td.innerHTML = durationToString(plan.duration * 1000);
    tr.appendChild(td);

    if (tabsState.columnsCount > 4) {
      td = document.createElement("td");
      td.innerHTML = durationToString(plan.driving_duration * 1000);
      tr.appendChild(td);
    }

    if (tabsState.columnsCount > 5) {
      td = document.createElement("td");
      td.textContent = `${plan.driving_distance.toFixed(1)} km`;
      tr.appendChild(td);
    }

    if (tabsState.columnsCount > 6) {
      td = document.createElement("td");
      td.textContent = plan.via.join(", ");
      tr.appendChild(td);
    }

    elements.routesTable.appendChild(tr);
  }
}

export function updateTimelines() {
  if (!d3) {
    elements.timeline.innerHTML = "<h4>D3 library not found</h4>";
    return;
  }

  if (elements.tabRoutesTimelines.hidden || elements.tabRoutesTimelines.clientWidth === 0) return;
  const currentColoring = document.getElementById("color-option").value;
  if (
    tabsState.timelinesSort === currentSort &&
    tabsState.timelinesColoring === currentColoring &&
    tabsState.timelineWidth === elements.tabRoutesTimelines.clientWidth
  )
    return;
  tabsState.timelinesSort = currentSort;
  tabsState.timelinesColoring = currentColoring;
  tabsState.timelineWidth = elements.tabRoutesTimelines.clientWidth;
  d3.select(elements.timeline).select("svg").remove();
  const chartRows = [];
  const coloringKeys = new Set();
  for (const plan of plans) {
    const chartRow = {
      label: `Route ${plan.id}`,
      times: [],
    };
    let location;
    let landGroup;
    for (const s of plan.segments) {
      for (const t of s.times) {
        let label = "";
        const segmentType = t.type === "TRAVEL" ? s.connection.type : t.type;
        const activityInfo = activitiesInfo[segmentType];
        if (location === null || t.type === "TRAVEL") {
          if (location !== s.connection.destination) {
            location = s.connection.destination;
            landGroup = location.land_group;
            if (landGroup === undefined) {
              landGroup = null;
              if (location.address.indexOf("Island") > 0 || location.name.indexOf("Island") > 0) landGroup = "Islands";
            }
            if (landGroup && landGroup.indexOf("(") > 0) {
              landGroup = landGroup.substring(0, landGroup.indexOf("(")).trim();
            }

            // label = location.id.length === 3 ? location.id : location.name;
          }
        }
        if (activityInfo.icon) label = `<tspan class="${activityInfo.iconClass}">${activityInfo.icon}</tspan>${label}`;

        const t2 = {
          description: t.description,
          segmentType,
          startingTime: new Date(t.start).getTime(),
          endingTime: new Date(t.end).getTime(),
        };
        if (label.length > 0) {
          t2.label = ""; // just a placeholder now, will be replaced with _label later
          t2._label = label;
        }
        const colorKey = currentColoring === "activity" ? segmentType : landGroup;
        if (colorKey !== null) {
          coloringKeys.add(colorKey);
          t2._color = colorKey;
        }
        if (t.end === t.start) {
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
  if (currentColoring === "activity") {
    colorScale = d3.scaleOrdinal().range(Object.values(activityColorsMap)).domain(Object.keys(activityColorsMap));
  } else {
    colorScale = d3.scaleOrdinal().range(d3.scaleOrdinal(d3.schemeAccent).range()).domain(Array.from(coloringKeys));
  }

  const width = elements.timeline.clientWidth - 10; // FIXME: magic number (righht margin?)

  const chart = timeline()
    .colors(colorScale)
    .colorProperty("_color")
    .showAxisTop()
    .margin({ left: 90, right: 10, top: 10, bottom: 10 })
    .tickFormat({
      format: d3.timeFormat("%I %p"),
      tickTime: d3.timeHours,
      numTicks: width / 100,
      tickInterval: 3,
      tickSize: 4,
    })
    .stack();

  const svg = d3.select(elements.timeline).append("svg").attr("width", width).datum(chartRows).call(chart);

  updateLegend(chart, coloringKeys, currentColoring, document.getElementById("timeline-legend"));

  svg.selectAll(".timeline-label").html((d, i) => {
    return `<a href="#${plans[i].hash}">Route ${plans[i].id}</a>`;
  });

  svg
    .selectAll("text")
    .style("cursor", "default")
    ._groups[0].forEach((element) => {
      assignTooltip(element);
      if (element.__data__?._label) element.innerHTML = element.__data__._label;
      // if (element.getClientRects()[0].width < element.textLength.baseVal.value) {
      //    element.innerHTML = '';
      // }
    });

  svg.selectAll("rect")._groups[0].forEach((element) => assignTooltip(element));
  svg.selectAll("tspan")._groups[0].forEach((element) => assignTooltip(element));
}

function updateLegend(chart, coloringKeys, currentColoring, legendElement) {
  coloringKeys = Array.from(coloringKeys);
  const colorsRange = chart.colors().range();
  const colorsDomain = chart.colors().domain();
  let legend = "Legend: ";
  for (let i = 0; i < colorsRange.length && i < coloringKeys.length; i++) {
    const n = colorsDomain.indexOf(coloringKeys[i]);
    legend += "<span>&nbsp;&nbsp;";
    legend += `<div style="display:inline-block;height:1em;width:1em;vertical-align:middle;background-color:${colorsRange[n]}">&nbsp;</div>&nbsp;`;
    if (currentColoring === "activity") {
      const activityInfo = activitiesInfo[coloringKeys[i]];
      legend += `<span class="${activityInfo.iconClass}">${activityInfo.icon}</span>`;
    }
    legend += `&nbsp;${coloringKeys[i]}</span>`;
  }
  legendElement.innerHTML = legend;
}

function assignTooltip(element) {
  const tooltip = d3.select(elements.tooltip);
  element.onmousemove = (event) => {
    let n = event.target;
    if (n.nodeName === "tspan") n = n.parentNode;
    if (n.nodeName === "text") n = n.parentNode;
    const rect = n.getBoundingClientRect();
    let x = rect.x + window.scrollX;
    const y = rect.bottom + window.scrollY + 3;
    if (x + elements.tooltip.scrollWidth > window.visualViewport.width)
      x = window.visualViewport.width - elements.tooltip.scrollWidth;
    tooltip.style("left", `${x}px`).style("top", `${y}px`);

    // widen tooltip to fit two lines
    while (elements.tooltip.scrollHeight > 50 && x > window.scrollX + 10) {
      x -= 10;
      tooltip.style("left", `${x}px`).style("top", `${y}px`);
    }
  };
  element.onmouseout = (event) => {
    tooltip.style("opacity", 0).style("visibility", "hidden");
  };
  element.onmouseover = (event) => {
    let data = event.target.__data__;
    if (!data) data = event.target.parentNode.__data__;
    if (!data || !data.description) return;
    // const rect = n.getBoundingClientRect();
    tooltip
      .html(`${timeToString(data.startingTime)} ${data.description}`)
      // .style('left', (rect.x) + 'px')
      // .style('top', (rect.bottom + 3) + 'px')
      .style("opacity", 1)
      .style("visibility", "visible");
  };
}

function onPlanSelected(id) {
  elements.scheduleCard.hidden = false;
  const plan = plans.find((p) => p.id === id);
  currentPlan = plan;

  // clear table
  while (elements.scheduleTable.firstChild) {
    elements.scheduleTable.removeChild(elements.scheduleTable.firstChild);
  }

  const depart_time = new Date(plan.depart_time.substring(0, 16));
  elements.scheduleCard.querySelector("#schedule-header").innerHTML =
    `<div class='card-header'>${plan.origin.name} to ${plan.destination.name}</div>` +
    `<div class='card-header-date'>${depart_time.toDateString()} at ${timeToString(depart_time)}</div>`;
  const via = [...new Set(plan.segments.slice(0, -1).map((s) => s.connection.destination.name))];
  elements.scheduleCard.querySelector("#schedule-via").textContent = via.length > 0 ? `via ${via.join(", ")}` : "";

  elements.scheduleCard.querySelector("#schedule-details").innerHTML =
    //`Route ${plan.id}.` +
    //` Departing:&nbsp;<strong>${depart_time.toDateString()} at ${timeToString(depart_time)}</strong>.` +
    `Total&nbsp;time:&nbsp;<strong>${durationToString(plan.duration * 1000)}</strong>.` +
    ` Driving&nbsp;distance:&nbsp;${plan.driving_distance.toFixed(1)}&nbsp;km.`;
  const scheduleMap = elements.scheduleCard.querySelector("#schedule-map");
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
      if (new Date(t.start) < Date.now() - 60000) tr.classList.add("past-route");

      let td;
      td = document.createElement("td");
      td.innerHTML = timeToString(t.start).replace(" ", "&nbsp;");
      tr.appendChild(td);

      let desc = t.description;
      if (s.schedule_url && t.type === "TRAVEL" && t.start !== t.end) {
        desc += `<a class="schedule-button no-print" href="${s.schedule_url}" target="_blank" type="button"><span class="icon"><i class="fa fa-list-alt"></i></span>Schedule</a>`;
      }
      td = document.createElement("td");
      if (t.description.startsWith("Ferry")) {
        desc = `<span class="icon"><i class="fa fa-ship"></i></span>${desc}`;
      }
      else if (t.description.startsWith("Drive")) {
        desc = `<span class="icon"><i class="fa fa-car"></i></span>${desc}`;
      }
      else if (t.description.startsWith("Free time")) {
        desc = `<span class="icon"><i class="fa fa-smile-o"></i></span>${desc}`;
      }
      else if (t.description.startsWith("Depart")) {
        desc = `<span class="icon"><i class="fa fa-sign-out"></i></span>${desc}`;
      }
      else if (t.description.startsWith("Arrive")) {
        desc = `<span class="icon"><i class="fa fa-sign-in"></i></span>${desc}`;
      }
      td.innerHTML = desc;
      tr.appendChild(td);

      const duration = new Date(t.end) - new Date(t.start);

      td = document.createElement("td");
      td.textContent = duration > 0 ? durationToString(duration) : "--";
      tr.appendChild(td);
    }
  }
}

export function sortPlans(sortBy) {
  if (sortBy === currentSort) return;
  plans.sort((a, b) => {
    if (a[sortBy] > b[sortBy]) return 1;
    if (a[sortBy] < b[sortBy]) return -1;
    return 0;
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
    if (currentTab.id === id) return;
    currentTab.hidden = true;
  }
  currentTab = document.getElementById(id);
  currentTab.hidden = false;
  updateTabsData();
}

export function toggleShow(id) {
  const element = document.getElementById(id);
  element.hidden = !element.hidden;
}

export function onPrint(card) {
  //elements.routesCard.classList.add("no-print");
  //elements.scheduleCard.classList.add("no-print");
  //document.getElementById(card).classList.remove("no-print");
  print();
}

export function onShare() {
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
        elements.inputDate.value,
      ).toDateString()}`;
    }

    if (!window.navigator.canShare) throw new Error("Browser doesn't support sharing");
    if (!window.navigator.canShare(data)) throw new Error("Browser cannot share data");
    window.navigator.share(data).then();
  } catch (error) {
    if (!navigator.clipboard) {
      showError("Cannot copy link to clipboard");
    } else {
      navigator.clipboard
        .writeText(window.location.href)
        .then(() => {
          showMessage("Link copied to clipboard");
        })
        .catch((r) => {
          showError(`Cannot copy link to clipboard: ${r}`);
        });
    }
  }
}

export function swap() {
  const origin = elements.inputOrigin.value;
  elements.inputOrigin.value = elements.inputDestination.value;
  elements.inputDestination.value = origin;
  saveHistory(null, window.location.hash);
}

function pad(num, size) {
  num = num.toString();
  while (num.length < size) num = `0${num}`;
  return num;
}

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

function defaultInputValue(input) {
  switch (input.type) {
    case "number":
      return parseInt(input.defaultValue);
    case "checkbox":
    case "radio":
      return input.defaultChecked;
    default:
      return input.defaultValue;
  }
}

function outputsize(event) {
  const target = event[0].target;
  if (target.clientWidth !== 0) {
    window.setTimeout(updateTabsData, 0);
  }
}

async function init() {
  window.addEventListener("error", (event) => {
    showMessage(event.type, event.message, event.type);
  });

  if (screen.orientation) {
    screen.orientation.onchange = (event) => {
      window.setTimeout(updateTabsData, 0);
    };
  } else {
    // FIXME: deprecated
    window.onorientationchange = (event) => {
      window.setTimeout(updateTabsData, 0);
    };
  }

  window.onresize = () => {
    window.setTimeout(updateTabsData, 0);
  };
  new ResizeObserver(outputsize).observe(elements.routesCard);
  new ResizeObserver(outputsize).observe(elements.timeline);

  window.onhashchange = async (event) => {
    await goto(new URL(event.newURL).hash);
  };

  window.onpopstate = async (event) => {
    if (!locations) {
      await loadLocations();
    }
    await applyOptions(event.state ?? urlToOptions(window.location));
  };

  // for insecure context clipboard and sharing are unavailable
  if (!navigator.clipboard) {
    elements.scheduleCard.querySelector("#share-button").style.display = "none";
  }

  resetState();

  // initialize input controls
  const date = new Date();
  const today = `${date.getFullYear()}-${pad(date.getMonth() + 1, 2)}-${pad(date.getDate(), 2)}`;
  elements.inputDate.defaultValue = today;
  elements.inputDate.min = today;

  elements.inputDate.addEventListener("keypress", async (event) => {
    if (event.code === "Enter") await submit();
  });
  elements.timelineSwitch.addEventListener("change", () => {
    window.setTimeout(() => {
      showTab(elements.timelineSwitch.checked ? "tab-routes-timeline" : "tab-routes-table");
    }, 0);
  });

  // initialize sort options
  elements.sortOption.setAttribute("onchange", "exports.sortPlans(this.value);");
  for (const k in columns) {
    const opt = document.createElement("option");
    opt.text = k;
    opt.value = columns[k];
    elements.sortOption.add(opt, null);
  }

  initInput(elements.inputOrigin);
  initInput(elements.inputDestination);
  // Load location data before applying options so that location names are substituted instead of ids.
  await loadLocations();
  await applyOptions(urlToOptions(window.location));
}

await init();
