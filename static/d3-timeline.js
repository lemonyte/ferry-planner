import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

export const timeline = () => {
  const DISPLAY_TYPES = ["circle", "rect"];

  let hover = () => {};
  let mouseover = () => {};
  let mouseout = () => {};
  let click = () => {};
  let scroll = () => {};
  let labelFunction = (label) => {
    return label;
  };
  let navigateLeft = () => {};
  let navigateRight = () => {};
  let orient = "bottom";
  let width = null;
  let height = null;
  let rowSeparatorsColor = null;
  let backgroundColor = null;
  let tickFormat = {
    format: d3.timeFormat("%I %p"),
    tickTime: d3.timeHours,
    tickInterval: 1,
    tickSize: 6,
    tickValues: null,
  };
  let colorCycle = d3.scaleOrdinal(d3.schemeAccent);
  let colorPropertyName = null;
  let display = "rect";
  let beginning = 0;
  let labelMargin = 0;
  let ending = 0;
  let margin = {
    left: 30,
    right: 30,
    top: 30,
    bottom: 30,
  };
  let stacked = false;
  let rotateTicks = false;
  let timeIsRelative = false;
  let fullLengthBackgrounds = false;
  let itemHeight = 20;
  let itemMargin = 5;
  let navMargin = 60;
  let showTimeAxis = true;
  let showAxisTop = false;
  let showTodayLine = false;
  let timeAxisTick = false;
  let timeAxisTickFormat = { stroke: "stroke-dasharray", spacing: "4 10" };
  let showTodayFormat = {
    marginTop: 25,
    marginBottom: 0,
    width: 1,
    color: colorCycle,
  };
  let showBorderLine = false;
  let showBorderFormat = {
    marginTop: 25,
    marginBottom: 0,
    width: 1,
    color: colorCycle,
  };
  let showAxisHeaderBackground = false;
  let showAxisNav = false;
  let showAxisCalendarYear = false;
  let axisBgColor = "white";
  let chartData = {};

  function appendTimeAxis(g, xAxis, yPosition) {
    if (showAxisHeaderBackground) {
      appendAxisHeaderBackground(g, 0, 0);
    }

    if (showAxisNav) {
      appendTimeAxisNav(g);
    }

    g.append("g").attr("class", "axis").attr("transform", `translate(${0},${yPosition})`).call(xAxis);
  }

  function appendTimeAxisCalendarYear(nav) {
    let calendarLabel = beginning.getFullYear();

    if (beginning.getFullYear() != ending.getFullYear()) {
      calendarLabel = `${beginning.getFullYear()}-${ending.getFullYear()}`;
    }

    nav
      .append("text")
      .attr("transform", `translate(${20}, 0)`)
      .attr("x", 0)
      .attr("y", 14)
      .attr("class", "calendarYear")
      .text(calendarLabel);
  }

  function appendTimeAxisNav(g) {
    const timelineBlocks = 6;
    const leftNavMargin = margin.left - navMargin;
    const incrementValue = (width - margin.left) / timelineBlocks;
    const rightNavMargin = width - margin.right - incrementValue + navMargin;

    const nav = g.append("g").attr("class", "axis").attr("transform", "translate(0, 20)");

    if (showAxisCalendarYear) {
      appendTimeAxisCalendarYear(nav);
    }

    nav
      .append("text")
      .attr("transform", `translate(${leftNavMargin}, 0)`)
      .attr("x", 0)
      .attr("y", 14)
      .attr("class", "chevron")
      .text("<")
      .on("click", () => {
        return navigateLeft(beginning, chartData);
      });

    nav
      .append("text")
      .attr("transform", `translate(${rightNavMargin}, 0)`)
      .attr("x", 0)
      .attr("y", 14)
      .attr("class", "chevron")
      .text(">")
      .on("click", () => {
        return navigateRight(ending, chartData);
      });
  }

  function appendAxisHeaderBackground(g, xAxis, yAxis) {
    g.insert("rect")
      .attr("class", "row-green-bar")
      .attr("x", xAxis)
      .attr("width", width)
      .attr("y", yAxis)
      .attr("height", itemHeight)
      .attr("fill", axisBgColor);
  }

  function appendTimeAxisTick(g, xAxis, maxStack) {
    g.append("g")
      .attr("class", "axis")
      .attr("transform", `translate(${0},${margin.top + (itemHeight + itemMargin) * maxStack})`)
      .attr(timeAxisTickFormat.stroke, timeAxisTickFormat.spacing)
      .call(xAxis.tickFormat("").tickSize(-(margin.top + (itemHeight + itemMargin) * (maxStack - 1) + 3), 0, 0));
  }

  function appendBackgroundBar(yAxisMapping, index, g, data, datum) {
    const greenbarYAxis = (itemHeight + itemMargin) * yAxisMapping[index] + margin.top;
    g.selectAll("svg")
      .data(data)
      .enter()
      .insert("rect")
      .attr("class", "row-green-bar")
      .attr("x", fullLengthBackgrounds ? 0 : margin.left)
      .attr("width", fullLengthBackgrounds ? width : width - margin.right - margin.left)
      .attr("y", greenbarYAxis)
      .attr("height", itemHeight)
      .attr("fill", backgroundColor instanceof Function ? backgroundColor(datum, index) : backgroundColor);
  }

  function appendLabel(gParent, yAxisMapping, index, hasLabel, datum) {
    const fullItemHeight = itemHeight + itemMargin;
    const rowsDown = margin.top + fullItemHeight / 2 + fullItemHeight * (yAxisMapping[index] || 1);

    gParent
      .append("text")
      .attr("class", "timeline-label")
      .attr("transform", `translate(${labelMargin},${rowsDown})`)
      .text(hasLabel ? labelFunction(datum.label) : datum.id)
      .on("click", (d, i) => {
        click(d, index, datum);
      });
  }

  function timeline(selection) {
    const gParent = selection;
    const g = gParent.append("g");
    const gParentSize = gParent._groups[0][0].getBoundingClientRect();

    const gParentItem = d3.select(gParent._groups[0][0]);

    const yAxisMapping = {};
    let maxStack = 1;
    let minTime = 0;
    let maxTime = 0;

    setWidth();

    // check if the user wants relative time
    // if so, substract the first timestamp from each subsequent timestamps
    if (timeIsRelative) {
      g.each((d, i) => {
        d.forEach((datum, index) => {
          datum.times.forEach((time, j) => {
            if (index === 0 && j === 0) {
              const originTime = time.startingTime; // store the timestamp that will serve as origin
              time.startingTime = 0; // set the origin
              time.endingTime = time.endingTime - originTime; // store the relative time (millis)
            } else {
              time.startingTime = time.startingTime - originTime;
              time.endingTime = time.endingTime - originTime;
            }
          });
        });
      });
    }

    // check how many stacks we're gonna need
    // do this here so that we can draw the axis before the graph
    if (stacked || ending === 0 || beginning === 0) {
      g.each((d, i) => {
        d.forEach((datum, index) => {
          // create y mapping for stacked graph
          if (stacked && Object.keys(yAxisMapping).indexOf(index) == -1) {
            yAxisMapping[index] = maxStack;
            maxStack++;
          }

          // figure out beginning and ending times if they are unspecified
          datum.times.forEach((time, i) => {
            if (beginning === 0)
              if (time.startingTime < minTime || (minTime === 0 && timeIsRelative === false))
                minTime = time.startingTime;
            if (ending === 0) if (time.endingTime > maxTime) maxTime = time.endingTime;
          });
        });
      });

      if (ending === 0) {
        ending = maxTime;
      }
      if (beginning === 0) {
        beginning = minTime;
      }
    }

    const scaleFactor = (1 / (ending - beginning)) * (width - margin.left - margin.right);

    // draw the axis
    const xScale = d3
      .scaleTime()
      .domain([beginning, ending])
      .range([margin.left, width - margin.right]);

    let xAxis;
    if (orient === "top") xAxis = d3.axisTop(xScale);
    if (orient === "bottom") xAxis = d3.axisBottom(xScale);
    if (orient === "left") xAxis = d3.axisLeft(xScale);
    if (orient === "right") xAxis = d3.axisRight(xScale);

    xAxis.tickFormat(tickFormat.format).tickSize(tickFormat.tickSize);

    if (tickFormat.tickValues != null) {
      xAxis.tickValues(tickFormat.tickValues);
    } else {
      xAxis.ticks(tickFormat.numTicks || tickFormat.tickTime, tickFormat.tickInterval);
    }

    // draw the chart
    g.each((d, i) => {
      chartData = d;
      d.forEach((datum, index) => {
        const data = datum.times;
        //data = data.sort((a,b) => {return b.endingTime-a.endingTime;})
        const hasLabel = typeof datum.label != "undefined";

        // issue warning about using id per data set. Ids should be individual to data elements
        if (typeof datum.id != "undefined") {
          console.warn(
            "d3Timeline Warning: Ids per dataset is deprecated in favor of a 'class' key. Ids are now per data element.",
          );
        }

        if (backgroundColor) {
          appendBackgroundBar(yAxisMapping, index, g, data, datum);
        }

        const groups = g.selectAll("svg").data(data).enter().append("g");

        groups
          .append((d, i) => {
            return document.createElementNS(d3.namespaces.svg, "display" in d ? d.display : display);
          })
          .attr("x", getXPos)
          .attr("y", getStackPosition)
          .attr("width", (d, i) => {
            return (d.endingTime - d.startingTime) * scaleFactor;
          })
          .attr("cy", (d, i) => {
            return getStackPosition(d, i) + itemHeight / 2;
          })
          .attr("cx", getXPos)
          .attr("r", itemHeight / 2)
          .attr("height", itemHeight)
          .style("fill", (d, i) => {
            let dColorPropName;
            if (d.color) return d.color;
            if (colorPropertyName) {
              dColorPropName = d[colorPropertyName];
              if (dColorPropName) {
                return colorCycle(dColorPropName);
              } else {
                return colorCycle(datum[colorPropertyName]);
              }
            }
            return colorCycle(index);
          })
          .on("mousemove", (d, i) => {
            hover(d, index, datum);
          })
          .on("mouseover", (d, i) => {
            mouseover(d, i, datum);
          })
          .on("mouseout", (d, i) => {
            mouseout(d, i, datum);
          })
          .on("click", (d, i) => {
            click(d, index, datum);
          })
          .attr("class", (d, i) => {
            return datum.class ? `timelineSeries_${datum.class}` : `timelineSeries_${index}`;
          })
          .attr("id", (d, i) => {
            // use deprecated id field
            if (datum.id && !d.id) {
              return `timelineItem_${datum.id}`;
            }

            return d.id ? d.id : `timelineItem_${index}_${i}`;
          });
        groups
          .append("text")
          .attr("x", getXTextPos)
          .attr("y", getStackTextPosition)
          .text((d) => {
            return d.label;
          });

        // g.selectAll("svg").data(data).enter()
        //   .append("text")
        //   .attr("x", getXTextPos)
        //   .attr("y", getStackTextPosition)
        //   .text((d) => {
        //     return d.label;
        //   })
        // ;

        if (rowSeparatorsColor) {
          const lineYAxis = itemHeight + itemMargin / 2 + margin.top + (itemHeight + itemMargin) * yAxisMapping[index];
          gParent
            .append("svg:line")
            .attr("class", "row-separator")
            .attr("x1", 0 + margin.left)
            .attr("x2", width - margin.right)
            .attr("y1", lineYAxis)
            .attr("y2", lineYAxis)
            .attr("stroke-width", 1)
            .attr("stroke", rowSeparatorsColor);
        }

        // add the label
        if (hasLabel) {
          appendLabel(gParent, yAxisMapping, index, hasLabel, datum);
        }

        if (typeof datum.icon !== "undefined") {
          gParent
            .append("image")
            .attr("class", "timeline-label")
            .attr("transform", `translate(${0},${margin.top + (itemHeight + itemMargin) * yAxisMapping[index]})`)
            .attr("xlink:href", datum.icon)
            .attr("width", margin.left)
            .attr("height", itemHeight);
        }

        function getStackPosition(d, i) {
          if (stacked) {
            return margin.top + (itemHeight + itemMargin) * yAxisMapping[index];
          }
          return margin.top;
        }

        function getStackTextPosition(d, i) {
          if (stacked) {
            return margin.top + (itemHeight + itemMargin) * yAxisMapping[index] + itemHeight * 0.75;
          }
          return margin.top + itemHeight * 0.75;
        }
      });
    });

    const belowLastItem = margin.top + (itemHeight + itemMargin) * maxStack;
    const aboveFirstItem = margin.top;
    const timeAxisYPosition = showAxisTop ? aboveFirstItem : belowLastItem;
    if (showTimeAxis) {
      appendTimeAxis(g, xAxis, timeAxisYPosition);
    }
    if (timeAxisTick) {
      appendTimeAxisTick(g, xAxis, maxStack);
    }

    if (width > gParentSize.width) {
      let move = () => {
        const x = Math.min(0, Math.max(gParentSize.width - width, d3.event.transform.x));
        zoom.translate([x, 0]);
        g.attr("transform", `translate(${x},0)`);
        scroll(x * scaleFactor, xScale);
      };

      let zoom = d3.zoom().x(xScale).on("zoom", move);

      gParent.attr("class", "scrollable").call(zoom);
    }

    if (rotateTicks) {
      g.selectAll(".tick text").attr("transform", (d) => {
        return `rotate(${rotateTicks})translate(${this.getBBox().width / 2 + 10},${
          /* TODO: change this 10 */ this.getBBox().height / 2
        })`;
      });
    }

    const gSize = g._groups[0][0].getBoundingClientRect();
    setHeight();

    if (showBorderLine) {
      g.each((d, i) => {
        d.forEach((datum) => {
          const times = datum.times;
          times.forEach((time) => {
            appendLine(xScale(time.startingTime), showBorderFormat);
            appendLine(xScale(time.endingTime), showBorderFormat);
          });
        });
      });
    }

    if (showTodayLine) {
      const todayLine = xScale(new Date());
      appendLine(todayLine, showTodayFormat);
    }

    function getXPos(d, i) {
      return margin.left + (d.startingTime - beginning) * scaleFactor;
    }

    function getXTextPos(d, i) {
      return margin.left + (d.startingTime - beginning) * scaleFactor + 5;
    }

    function setHeight() {
      if (!height && !gParentItem.attr("height")) {
        if (itemHeight) {
          // set height based off of item height
          height = gSize.height + gSize.top - gParentSize.top;
          // set bounding rectangle height
          d3.select(gParent._groups[0][0]).attr("height", height);
        } else {
          throw new Error("height of the timeline is not set");
        }
      } else {
        if (!height) {
          height = gParentItem.attr("height");
        } else {
          gParentItem.attr("height", height);
        }
      }
    }

    function setWidth() {
      if (!width && !gParentSize.width) {
        try {
          width = gParentItem.attr("width");
          if (!width) {
            throw new Error("width of the timeline is not set. As of Firefox 27, timeline().with(x) needs to be explicitly set in order to render");
          }
        } catch (err) {
          console.log(err);
        }
      } else if (!(width && gParentSize.width)) {
        try {
          width = gParentItem.attr("width");
        } catch (err) {
          console.log(err);
        }
      }
      // if both are set, do nothing
    }

    function appendLine(lineScale, lineFormat) {
      gParent
        .append("svg:line")
        .attr("x1", lineScale)
        .attr("y1", lineFormat.marginTop)
        .attr("x2", lineScale)
        .attr("y2", height - lineFormat.marginBottom)
        .style("stroke", lineFormat.color) //"rgb(6,120,155)")
        .style("stroke-width", lineFormat.width);
    }
  }

  // SETTINGS

  timeline.margin = (p) => {
    if (!p) return margin;
    margin = p;
    return timeline;
  };

  timeline.orient = (orientation) => {
    if (!orientation) return orient;
    orient = orientation;
    return timeline;
  };

  timeline.itemHeight = (h) => {
    if (!h) return itemHeight;
    itemHeight = h;
    return timeline;
  };

  timeline.itemMargin = (h) => {
    if (!h) return itemMargin;
    itemMargin = h;
    return timeline;
  };

  timeline.navMargin = (h) => {
    if (!h) return navMargin;
    navMargin = h;
    return timeline;
  };

  timeline.height = (h) => {
    if (!h) return height;
    height = h;
    return timeline;
  };

  timeline.width = (w) => {
    if (!w) return width;
    width = w;
    return timeline;
  };

  timeline.display = (displayType) => {
    if (!displayType || DISPLAY_TYPES.indexOf(displayType) == -1) return display;
    display = displayType;
    return timeline;
  };

  timeline.labelFormat = (f) => {
    if (!f) return labelFunction;
    labelFunction = f;
    return timeline;
  };

  timeline.tickFormat = (format) => {
    if (!format) return tickFormat;
    tickFormat = format;
    return timeline;
  };

  timeline.hover = (hoverFunc) => {
    if (!hoverFunc) return hover;
    hover = hoverFunc;
    return timeline;
  };

  timeline.mouseover = (mouseoverFunc) => {
    if (!mouseoverFunc) return mouseover;
    mouseover = mouseoverFunc;
    return timeline;
  };

  timeline.mouseout = (mouseoutFunc) => {
    if (!mouseoutFunc) return mouseout;
    mouseout = mouseoutFunc;
    return timeline;
  };

  timeline.click = (clickFunc) => {
    if (!clickFunc) return click;
    click = clickFunc;
    return timeline;
  };

  timeline.scroll = (scrollFunc) => {
    if (!scrollFunc) return scroll;
    scroll = scrollFunc;
    return timeline;
  };

  timeline.colors = (colorFormat) => {
    if (!colorFormat) return colorCycle;
    colorCycle = colorFormat;
    return timeline;
  };

  timeline.beginning = (b) => {
    if (!b) return beginning;
    beginning = b;
    return timeline;
  };

  timeline.ending = (e) => {
    if (!e) return ending;
    ending = e;
    return timeline;
  };

  timeline.labelMargin = (m) => {
    if (!m) return labelMargin;
    labelMargin = m;
    return timeline;
  };

  timeline.rotateTicks = (degrees) => {
    if (!degrees) return rotateTicks;
    rotateTicks = degrees;
    return timeline;
  };

  timeline.stack = () => {
    stacked = !stacked;
    return timeline;
  };

  timeline.relativeTime = () => {
    timeIsRelative = !timeIsRelative;
    return timeline;
  };

  timeline.showBorderLine = () => {
    showBorderLine = !showBorderLine;
    return timeline;
  };

  timeline.showBorderFormat = (borderFormat) => {
    if (!borderFormat) return showBorderFormat;
    showBorderFormat = borderFormat;
    return timeline;
  };

  timeline.showToday = () => {
    showTodayLine = !showTodayLine;
    return timeline;
  };

  timeline.showTodayFormat = (todayFormat) => {
    if (!todayFormat) return showTodayFormat;
    showTodayFormat = todayFormat;
    return timeline;
  };

  timeline.colorProperty = (colorProp) => {
    if (!colorProp) return colorPropertyName;
    colorPropertyName = colorProp;
    return timeline;
  };

  timeline.rowSeparators = (color) => {
    if (!color) return rowSeparatorsColor;
    rowSeparatorsColor = color;
    return timeline;
  };

  timeline.background = (color) => {
    if (!color) return backgroundColor;
    backgroundColor = color;
    return timeline;
  };

  timeline.showTimeAxis = () => {
    showTimeAxis = !showTimeAxis;
    return timeline;
  };

  timeline.showAxisTop = () => {
    showAxisTop = !showAxisTop;
    return timeline;
  };

  timeline.showAxisCalendarYear = () => {
    showAxisCalendarYear = !showAxisCalendarYear;
    return timeline;
  };

  timeline.showTimeAxisTick = () => {
    timeAxisTick = !timeAxisTick;
    return timeline;
  };

  timeline.fullLengthBackgrounds = () => {
    fullLengthBackgrounds = !fullLengthBackgrounds;
    return timeline;
  };

  timeline.showTimeAxisTickFormat = (format) => {
    if (!format) return timeAxisTickFormat;
    timeAxisTickFormat = format;
    return timeline;
  };

  timeline.showAxisHeaderBackground = (bgColor) => {
    showAxisHeaderBackground = !showAxisHeaderBackground;
    if (bgColor) {
      axisBgColor = bgColor;
    }
    return timeline;
  };

  timeline.navigate = (navigateBackwards, navigateForwards) => {
    if (!navigateBackwards && !navigateForwards) return [navigateLeft, navigateRight];
    navigateLeft = navigateBackwards;
    navigateRight = navigateForwards;
    showAxisNav = !showAxisNav;
    return timeline;
  };

  return timeline;
};
