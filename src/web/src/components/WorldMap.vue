<script setup lang="ts">

    import { ref, computed, onMounted } from 'vue'
    import {
      geoNaturalEarth1,
      geoPath,
      scaleSequential,
      interpolateRdPu,
    } from 'd3'

    const width = 900
    const height = 520

    // Example analytics data.
    const samples = {
      France: 340,
      Germany: 128,
      Italy: 81,
      Spain: 17,
      Belgium: 90,
      Sweden: 12,
      Norway: 2,
      Canada: 25,
      Brazil: 4,
      England: 89,
      USA: 67,
      China: 45,
      India: 21, 
      Australia: 4
    }

    const countries = ref([])
    const hovered = ref(null)
    const projection = geoNaturalEarth1()
    const path = geoPath(projection)

    const maxVisitors = computed(() =>
      Math.max(...Object.values(samples), 1)
    )

    const color = computed(() =>
      scaleSequential([0, maxVisitors.value], interpolateRdPu)
    )

    onMounted(async () => {
      const geojson = await $fetch('/maps/world.geojson')
      countries.value = geojson.features
      projection.fitSize([width, height], geojson)
    })

    function getVisitors(country) {
      return samples[country.properties.name] ?? 0
    }

    function getColor(country) {
      if(getVisitors(country) == 0) {
        return "#e4e4e7"
      } else {
        return color.value(getVisitors(country))
      }
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
        class="stroke-white stroke-[0.4] transition-all duration-150 hover:opacity-80 cursor-pointer"
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
        {{ getVisitors(hovered) }} samples
      </div>
    </div>

  </div>
</template>