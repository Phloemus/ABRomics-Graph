<script setup>
    import { ref } from 'vue'

    import { codeToHtml } from 'shiki'

    import Sidebar from "./components/Sidebar.vue"
    import Navbar from "./components/Navbar.vue"
    import ActionButton from "./components/ActionButton.vue"

    import queries from './static/queries.json'

    const textQuery = `
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX go: <http://purl.org/obo/owl/GO#>
PREFIX schema: <https://schema.org/>
        
## Q1: Get the resistances genes for a specific sample (sample ARDIG32)
## 
SELECT ?sample_id (?gene_name as ?resistance_gene_name) WHERE {
        
    ?obs_prop rdf:type sosa:ObservableProperty ;
        rdfs:label "Resistance gene" .
                        
    ?sample rdf:type sio:001050 ;
        schema:identifier ?sample_id .
        
    FILTER(?sample_id = "ARDIG32")
        
    ?gene rdf:type go:Gene ;
        rdfs:label ?gene_name .
                        
    ?observations sosa:hasObservableProperty ?obs_prop ;
        sosa:hasFeatureOfInterest ?gene ;
        sosa:hasFeatureOfInterest ?sample ;
        sosa:hasSimpleResult ?gene_name .
        
}
    `

    const queryHtml = await codeToHtml(textQuery, { lang: 'sparql', theme: 'catppuccin-mocha', colorReplacements: { '#1e1e2e': '#1e293b' }})
    console.log(queryHtml)

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
    <div class="w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
    <div class="h-screen w-full bg-slate-50 flex">
        <Sidebar />
        <div class="w-full">
            <Navbar />
            <div class="px-10 my-10">
                <main class="mx-auto p-8 bg-white max-w-screen-xl border border-slate-200 rounded-md">
                    <h1 class="mb-1 text-2xl text-slate-900 font-bold">{{ queries[0].title }}</h1>
                    <span class="text-md text-slate-600">{{ queries[0].name }}</span>
                    <div>
                        <p class="my-6 text-lg text-slate-700">{{ queries[0].definition }}</p>
                    </div>
                    <div>
                        <h2 class="text-xl text-slate-900 font-bold">Ontologies involved</h2>
                        <div class="my-6 flex gap-4">
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">
                                    {{ queries[0].ontologies[0].shortName }}: {{ queries[0].ontologies[0].name }}
                                </span>
                                <p class="mt-4 text-slate-800">
                                    {{ queries[0].ontologies[0].definition }}
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">
                                    {{ queries[0].ontologies[0].shortName }}: {{ queries[0].ontologies[0].name }}
                                </span>
                                <p class="mt-4 text-slate-800">
                                    {{ queries[0].ontologies[0].definition }}
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">
                                    {{ queries[0].ontologies[0].shortName }}: {{ queries[0].ontologies[0].name }}
                                </span>
                                <p class="mt-4 text-slate-800">
                                    {{ queries[0].ontologies[0].definition }}
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="mt-6 flex gap-6">
                        <div class="w-3/5">
                            <h2 class="text-xl text-slate-900 font-bold">Query</h2>
                            <div class="my-4 w-full bg-slate-800 rounded-md">
                                <div class="py-2 px-4 flex items-center justify-between border-b border-slate-700">
                                    <span class="text-white">sparql</span>
                                    <div class="flex items-center gap-2">
                                        <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                        <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                        <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                    </div>
                                </div>
                                <div class="p-4 w-full bg-slate-800 rounded-b-md">
                                    <code>
                                        <div v-html="queryHtml"></div>
                                    </code>
                                </div>
                            </div>
                            <div>
                                <ActionButton
                                    content="Execute query"
                                    @click="fetchQueryResult(1)"
                                >
                                </ActionButton>
                            </div>
                        </div>
                        <div>
                            <h2 class="text-xl text-slate-900 font-bold">Datasources</h2>
                        </div>
                    </div>

                    <div class="my-6 hidden">
                        <div class="flex justify-between items-center">
                            <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
                        </div>
                        <div class="my-4 w-full bg-slate-800 rounded-md">
                            <div class="py-2 px-4 flex items-center justify-between border-b border-slate-700">
                                <span class="text-white">csv</span>
                                <div class="flex items-center gap-2">
                                    <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                    <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                    <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                </div>
                            </div>
                            <div class="p-4 w-full bg-slate-800 rounded-b-md">
                                <code>
                                    <p class="text-white">test !!</p>
                                    <p class="text-white">test !!</p>
                                    <p class="text-white">test !!</p>
                                    <p class="text-white">test !!</p>
                                    <p class="text-white">test !!</p>
                                    <p class="text-white">test !!</p>
                                </code>
                            </div>
                        </div>
                    </div>

                </main>
            </div>
        </div>
    </div>
</template>
