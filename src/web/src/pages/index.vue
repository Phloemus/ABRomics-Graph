<script setup>

    import { Index, Charset } from 'flexsearch'

    import data from "../static/result-10k-first-classes.json"

    const query = ref("")
    const results = ref([])

    const index = new Index({
      encoder: Charset.LatinBalance,
      tokenize: "forward", 
      async: true, 
    });

    console.log(data.results.bindings.length)

    data.results.bindings.forEach((data) => {
        index.add(data.class.value, data.label.value)
    })

    function performSearch() {
        if(query.value.length > 0) {
            results.value = index.search(query.value)
        } else {
            results.value = []
        }
    }

</script>

<template>
    <div>
        <input v-model="query" @input="performSearch" placeholder="Search..." />
        
        <div v-if="results.length > 0">
            <ul>
                <li v-for="(result, index) in results" :key="index">
                    {{ result }}
                </li>
            </ul>
        </div>

        <div v-else>
            <p>No results found</p>
        </div>
  </div>
</template>
