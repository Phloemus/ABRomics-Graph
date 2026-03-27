<script setup>
    import { onMounted, ref, watch } from 'vue'
    import * as d3 from 'd3'

    const props = defineProps({
      data: {
        type: Array,
        required: true
      },
      width: {
        type: Number,
        default: 400
      },
      height: {
        type: Number,
        default: 200
      }
    })

    const svg = ref(null)

    const drawChart = () => {
      const svgEl = d3.select(svg.value)
      svgEl.selectAll('*').remove() // Clear previous renders

      svgEl.attr('width', props.width).attr('height', props.height)

      const x = d3
        .scaleBand()
        .domain(props.data.map((d, i) => i))
        .range([0, props.width])
        .padding(0.1)

      const y = d3
        .scaleLinear()
        .domain([0, d3.max(props.data)])
        .nice()
        .range([props.height, 0])

      svgEl
        .selectAll('rect')
        .data(props.data)
        .join('rect')
        .attr('x', (_, i) => x(i))
        .attr('y', d => y(d))
        .attr('width', x.bandwidth())
        .attr('height', d => props.height - y(d))
        .attr('fill', 'steelblue')
    }

    onMounted(drawChart)
    watch(() => props.data, drawChart)
</script>

<template>
  <div class="relative">
    <svg ref="svg"></svg>
  </div>
</template>
