<script setup>

    import { ref } from 'vue'
    import { useRoute } from 'vue-router'

    import { codeToHtml } from 'shiki'

    // Test code editor
    const code = ref(`console.log("Hello from Shiki + CodeMirror!")`)


    const query = {content: "SELECT ?s ?p ?o WHERE {\n\t?s ?p ?o . \n}\nLIMIT 10"}
    const queryHtml = await codeToHtml(query.content, { lang: 'sparql', theme: 'catppuccin-mocha', colorReplacements: { '#1e1e2e': '#1e293b' }})

    var queryResponse = ref([])
    var isQueryPerformed = ref(false)
    var isQueryError = ref(false)
    var queryError = ref("")

    function fetchQueryResult(id) {

    }
</script>

<template>
    <div class="px-8 py-4 flex justify-between items-start">
                <div class="w-full">
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
                            <code class="w-full h-full relative">
                                <div class="w-full h-full" v-html="queryHtml"></div>
                                <textarea class="bg-red-500 w-max absolute top-0 left-0 z-10" v-model="query.content"></textarea>
                            </code>
                        </div>
                    </div>
                </div>
                <div>
                </div>
    </div>
</template>
