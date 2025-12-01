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
            <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Dataset</h2>
            <p class="my-6 text-lg text-slate-700 leading-8">
                The knowledge graph has been created using public metadata and antibiotic resistance analysis data from the ABRomics plateform.
            </p>
            <p class="my-6 text-lg text-slate-700 leading-8">
                The genomic sequences and metadata of multiple harmfull strains of bacterias found in human, animal and environmental origins have been integrated and processed into the ABRomics platform. The resulting 1613 analysis reports gather sample metadata as well as antibiotic resistance genes detected with the ABRomics bioinformatics workflows were then extracted and formated using the graph structure described below.
            </p>
            <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Knowledge graph structure</h2>
            <div class="px-10 w-full flex flex-col gap-10">
                <img src="assets/sample-modelisation-sosa.png"/>
                <img src="assets/measure-modelisation-sosa.png"/>
            </div>
        </div>

        <div v-else>
            <p>No results found</p>
        </div>
  </div>
</template>
