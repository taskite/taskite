<script setup>
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";

const props = defineProps(['data'])

const heatmap = ref(null);

const drawHeatmap = () => {
    const width = 900;
    const height = 160;
    const cellSize = 15;
    const year = 2024;

    // Clear previous SVG if it exists
    d3.select(heatmap.value).select("svg").remove();

    const svg = d3
        .select(heatmap.value)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(30, 20)`);

    // const colorScale = d3
    //     .scaleSequential(d3.interpolateGreens)
    //     .domain([0, d3.max(Object.values(props.data)) || 1]);

    // Define a custom color scale using shades of #8B5CF6
    const colorScale = d3
        .scaleLinear()
        .domain([0, d3.max(Object.values(props.data)) || 1])
        .range(["#FFFFFF", "#8B5CF6"]); // Light to primary color

    // Create a day scale and axis for day labels
    const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    svg
        .selectAll(".day-label")
        .data(daysOfWeek)
        .enter()
        .append("text")
        .attr("x", -5)
        .attr("y", (d, i) => i * cellSize + 10)
        .attr("text-anchor", "end")
        .attr("font-size", "10px")
        .text((d) => d);

    // Draw each day in the year
    const timeFormat = d3.timeFormat("%Y-%m-%d");
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31);
    const dateRange = d3.timeDays(startDate, endDate);

    svg
        .selectAll(".day")
        .data(dateRange)
        .enter()
        .append("rect")
        .attr("class", "day")
        .attr("width", cellSize - 3)
        .attr("height", cellSize - 3)
        .attr("x", (d) => d3.timeWeek.count(startDate, d) * cellSize)
        .attr("y", (d) => d.getDay() * cellSize)
        .attr("fill", (d) => colorScale(props.data[timeFormat(d)] || 0))
        .attr("stroke", "#ccc")
        .attr("rx", 3) // Set the x-axis corner radius
        .attr("ry", 3) // Set the y-axis corner radius
        .append("title")
        .text((d) => `${timeFormat(d)}: ${props.data[timeFormat(d)] || 0} tasks`);
};

onMounted(() => {
    drawHeatmap()
})
watch(() => props.data, drawHeatmap, { deep: true });
</script>

<template>
    <div ref="heatmap" class="calendar-heatmap"></div>
</template>

<style scoped>
.calendar-heatmap {
  display: inline-block;
}
</style>