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
                <div class="my-3 p-2 bg-slate-50 rounded-md">
                    <h4 class="text-slate-800 text-md">
                        <span class="font-medium text-slate-900">Competency Question 1:</span> 
                        What are the most common antibiotic resistance genes present in all samples
                    </h4>
                </div>
                <div class="my-3 p-2 bg-slate-50 rounded-md">
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
            <main class="p-6">
                <h1>ABRomics KG</h1>
                <button @click="fetchQueryResult(1)">Execute Query 1</button>

            </main>
        </div>
    </div>
</template>
