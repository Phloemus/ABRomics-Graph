<script setup>
    import { ref } from 'vue'
    const count = ref(0)

    function incrementBy2() {
        count.value += 2 
    }

    function fetchQueryResult(id) {
        console.log(id)
        // Don't forget to change the port or the host in prod ;)
        fetch("http://localhost:5000/graph-api/node/count").then(response => { 
            return response.json()
        }).then((data) => {
            console.log(data)
        }).catch(err => {
            console.error("Error fetching data: ", err)
        })
    }
</script>


<template>
  <div>
      <h1>ABRomics KG</h1>
      <button
          class="px-6 py-1 bg-slate-900 text-white text-md rounded-sm"
          @click="incrementBy2"
      >
        count is {{ count }}
      </button>
      <button @click="fetchQueryResult(1)">Execute Query 1</button>
  </div>
</template>
