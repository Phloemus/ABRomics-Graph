<script setup>
    import { ref } from 'vue'

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
        <div class="px-4 w-96 h-full bg-white border-r border-slate-200 z-20">
            <div>

            </div>
            <div class="w-full relative">
                <h3 class="mx-1 my-4 text-slate-600 text-lg">Queries</h3>
                <div class="my-3 p-2 bg-slate-50 rounded-md hover:bg-slate-100 hover:cursor-pointer">
                    <h4 class="text-slate-800 text-md">
                        <span class="font-medium text-slate-900">Competency Question 1:</span> 
                        What are the most common antibiotic resistance genes present in all samples
                    </h4>
                </div>
                <div class="my-3 p-2 bg-slate-50 rounded-md hover:bg-slate-100 hover:cursor-pointer">
                    <h4 class="text-slate-800 text-md">
                        <span class="font-medium text-slate-900">Competency Question 1:</span> 
                        What are the most common antibiotic resistance genes present in all samples
                    </h4>
                </div>
                <div class="flex justify-center">
                    <button
                        class="px-8 py-2 bg-slate-900 hover:bg-slate-800 text-white text-md rounded-md"
                    >
                        More queries
                    </button>
                </div>
            </div>
            <div class="mx-12 px-6 pb-4 absolute bottom-0 left-0 border-t-2 border-slate-200">
                <div class="py-3 flex gap-2 text-slate-500">
                    <span>v0.0.1</span>
                    <span>ABRomicsKG</span>
                    <span>2025</span>
                </div>
            </div>
        </div>
        <div class="w-full">
            <nav class="px-6 py-3 w-full bg-white border-b border-slate-200">

                <div class="flex flex-row-reverse gap-4">
                    <button
                       class="px-8 py-2 bg-slate-900 hover:bg-slate-800 text-white text-md rounded-md"
                    >
                        Login
                    </button>
                </div>
            </nav>
            <div class="px-10 my-10">
                <main class="mx-auto p-6 bg-white max-w-screen-2xl border border-slate-200 rounded-md">
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
                    <div class="my-6 flex gap-4">
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
                                <button 
                                    class="px-8 py-2 bg-slate-900 hover:bg-slate-800 text-white text-md rounded-md" 
                                    @click="fetchQueryResult(1)"
                                >
                                    Execute query
                                </button>
                            </div>
                        </div>
                        <div>
                            <h2 class="text-xl text-slate-900 font-bold">Datasources</h2>
                        </div>
                    </div>
                    <div class="my-6">
                        <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
                        <div class="my-4 w-full h-6 bg-slate-800 rounded-md">
                    
                        </div>
                    </div>


                </main>
            </div>
        </div>
    </div>
</template>
