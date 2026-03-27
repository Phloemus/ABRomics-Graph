<script setup>
  import * as d3 from "d3";
  import { ref, watch, onMounted } from "vue";

  const chartContainer = ref(null);

  const props = defineProps({
    data: Object,
  });

  function renderChart() {
    if (!props.data || !chartContainer.value) return;

    d3.select(chartContainer.value).selectAll("*").remove();

    const width = chartContainer.value.clientWidth;
    const height = width;

    const svg = d3.select(chartContainer.value)
      .append("svg")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .classed("w-full h-auto", true);

    const color = d3.scaleOrdinal()
      .domain(props.data.children.map(d => d.name))
      .range(["#e6194b","#f58231","#ffe119","#bfef45","#3cb44b","#42d4f4","#4363d8",
  "#911eb4","#f032e6","#a9a9a9","#fabebe","#ffd8b1","#fffac8","#aaffc3",
  "#e6beff","#9a6324","#800000","#808000","#469990","#000075","#a0522d",
  "#ff7f50","#6495ed","#dc143c","#00ced1","#9400d3","#ff1493","#00bfff",
  "#696969","#1e90ff","#b22222","#228b22","#ff69b4","#cd5c5c","#4b0082",
  "#f08080","#20b2aa","#87cefa","#778899","#b0c4de","#ffff54","#dda0dd",
  "#98fb98"])
      //.range(["#38bdf8", "#a78bfa", "#34d399", "#fbbf24"]);

    const pack = d3.pack()
      .size([width, height])
      .padding(10);

    const root = d3.hierarchy(props.data)
      .sum(d => d.value);

    pack(root);

    const nodes = svg.selectAll("g")
      .data(root.descendants())
      .enter()
      .append("g")
      .attr("transform", d => `translate(${d.x},${d.y})`);

    nodes.append("circle")
      .attr("r", d => d.r)
      .attr("fill", d => {
        if (d.depth === 2) return color(d.parent.data.name);
        return "transparent";
      });

    nodes.append("text")
      .text(d => (d.depth > 0 ? d.data.name : ""));
  }

  onMounted(renderChart);

  watch(
    () => props.data,
    () => {
      renderChart();
    },
    { deep: true } // important if nested data changes
  );
</script>

<template>
  <div class="relative w-full flex justify-center items-center py-8">
    <div ref="chartContainer" class="w-full h-10 max-w-3xl"></div>
  </div>
</template>

<style scoped>
:host {
  display: block;
}
</style>
