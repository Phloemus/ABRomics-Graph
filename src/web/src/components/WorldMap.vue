<script setup lang="ts">

    import { ref, computed, onMounted } from 'vue'
    import {
      geoNaturalEarth1,
      geoPath,
      scaleSequential,
      interpolateBlues,
    } from 'd3'

    const width = 900
    const height = 520

    // Example analytics data.
    // Replace this with a prop or data from your API.
    const visitors = {
      France: 340,
      Germany: 128,
      Italy: 81,
      Spain: 17,
      Belgium: 90
    }

    const countries = ref([])
    const hovered = ref(null)
    const projection = geoNaturalEarth1()
    const path = geoPath(projection)

    const maxVisitors = computed(() =>
      Math.max(...Object.values(visitors), 1)
    )

    const color = computed(() =>
      scaleSequential(interpolateBlues)
        .domain([0, maxVisitors.value])
    )

    onMounted(async () => {
      const geojson = await $fetch('/maps/world.geojson')
      countries.value = geojson.features
      projection.fitSize([width, height], geojson)
    })

    function getVisitors(country) {
      return visitors[country.properties.name] ?? 0
    }

    function getColor(country) {
      return color.value(getVisitors(country))
    }


</script>

<template>
  <div class="relative w-full">

    <svg
      :viewBox="`0 0 ${width} ${height}`"
      class="w-full h-full"
      preserveAspectRatio="xMidYMid meet"
    >
      <path
        v-for="country in countries"
        :key="country.properties.name"
        :d="path(country) ?? ''"
        :fill="getColor(country)"
        class="fill-zinc-200 stroke-white stroke-[0.4] transition-all duration-150 hover:opacity-80 cursor-pointer"
        @mouseenter="hovered = country"
        @mouseleave="hovered = null"
      />
    </svg>

    <div
      v-if="hovered"
      class="absolute left-4 top-4 rounded-lg bg-white shadow-lg border px-3 py-2 text-sm pointer-events-none"
    >
      <div class="font-semibold">
        {{ hovered.properties.name }}
      </div>

      <div class="text-gray-600">
        {{ getVisitors(hovered) }} visitors
      </div>
    </div>

  </div>
</template>