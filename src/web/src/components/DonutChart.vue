<script setup>

    import * as d3 from "d3"
    import { ref, computed, onMounted, watch } from "vue"

    const props = defineProps({
      data: {
        type: Object,
        required: true
      }
    })

    const svgRef = ref(null)

    const width = 350
    const height = 350
    const radius = Math.min(width, height) / 2

    const dataset = computed(() =>
      Object.entries(props.data).map(([gene, count]) => ({
        gene,
        count
      }))
    )

    const color = computed(() =>
      d3.scaleOrdinal()
        .domain(dataset.value.map(d => d.gene))
        .range(d3.quantize(d3.interpolateRdPu, dataset.value.length))
    )

    function drawChart() {
      if (!svgRef.value) return

      d3.select(svgRef.value).selectAll("*").remove()

      const svg = d3.select(svgRef.value)
        .attr("viewBox", `0 0 ${width} ${height}`)

      const g = svg.append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`)

      const pie = d3.pie()
        .value(d => d.count)
        .sort(null)

      const arc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius)

      g.selectAll("path")
        .data(pie(dataset.value))
        .join("path")
        .attr("d", arc)
        .attr("fill", d => color.value(d.data.gene))
        .attr("stroke", "#fff")
        .attr("stroke-width", 2)
    }

    onMounted(drawChart)

    watch(
      () => props.data,
      drawChart,
      { deep: true }
    )
</script>

<template>
  <div class="flex flex-col items-center gap-6 lg:flex-row">
    <svg ref="svgRef" class="w-40 h-40" />
    <div class="grid grid-cols-2 gap-x-6 gap-y-2 text-sm">
      <div
        v-for="item in dataset"
        :key="item.gene"
        class="flex items-center gap-2"
      >
        <span
          class="w-4 h-4 rounded"
          :style="{ backgroundColor: color(item.gene) }"
        ></span>
        <span>{{ item.gene }}</span>
        <span class="ml-auto font-semibold">
          {{ item.count }}
        </span>
      </div>
    </div>
  </div>
</template>