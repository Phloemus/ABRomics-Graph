<script setup>
    import { ref } from 'vue'

    import Sidebar from "./components/Sidebar.vue"
    import ActionButton from "./components/ActionButton.vue"

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
            <nav class="px-6 py-3 w-full bg-white border-b border-slate-200">
                <div class="flex flex-row-reverse gap-4">
                    <ActionButton content="Login"/>
                </div>
            </nav>
            <div class="px-10 my-10">
                <main class="mx-auto p-8 bg-white max-w-screen-xl border border-slate-200 rounded-md">
                    <h1 class="mb-1 text-2xl text-slate-900 font-bold">What are the most common antibiotic resistance genes in all samples ?</h1>
                    <span class="text-md text-slate-600">competency question 1</span>
                    <div>
                        <p class="my-6 text-lg text-slate-700">
                            This competency question allows to explore the whole database in order to find relevant data for 
                            further exploration. The query is a template that can be easily reused to build new SPARQL queries
                            that will rely on different data sources using Uniprot or Wikidata. It serves as the test request 
                            when deploying the application, so this query should always work perfectly !
                        </p>
                    </div>
                    <div>
                        <h2 class="text-xl text-slate-900 font-bold">Ontologies involved</h2>
                        <div class="my-6 flex gap-4">
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">GO: Gene Ontology</span>
                                <p class="mt-4 text-slate-800">
                                    Provides structured controlled vocabularies for the annotation of gene products with... 
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">GO: Gene Ontology</span>
                                <p class="mt-4 text-slate-800">
                                    Provides structured controlled vocabularies for the annotation of gene products with... 
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                            <div class="p-4 bg-slate-50 hover:bg-slate-100 w-96 rounded-md cursor-pointer">
                                <span class="px-4 py-1 text-md bg-sky-200 text-sky-500 rounded-sm">GO: Gene Ontology</span>
                                <p class="mt-4 text-slate-800">
                                    Provides structured controlled vocabularies for the annotation of gene products with... 
                                    <span class="text-slate-900 font-semibold hover:underline">more</span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="mt-6 flex gap-4">
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
                                        <p class="text-white">test !!</p>
                                        <p class="text-white">test !!</p>
                                        <p class="text-white">test !!</p>
                                        <p class="text-white">test !!</p>
                                        <p class="text-white">test !!</p>
                                        <p class="text-white">test !!</p>
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
                        <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
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
