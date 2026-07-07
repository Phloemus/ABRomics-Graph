<script setup>
    import { ref } from 'vue'
    import { useRoute } from 'vue-router'

    import { codeToHtml } from 'shiki'

    import ActionButton from "../../components/ActionButton.vue"
    import Table from "../../components/Table.vue"

    const config = useRuntimeConfig()

    const route = useRoute()
    const queryId = route.params.id - 1

    const queryMetadata = ref({})
    const queryContent = ref("")
    const queryHtml = ref({})
    var queryResponse = ref([])
    var isQueryPerformed = ref(false)
    var isQueryError = ref(false)
    var queryError = ref("")

    // on render
    getCompetencyQuestion(queryId)

    function getCompetencyQuestion(id) {
        const uri = config.public.apiUrl + "/query/competency-question"
        fetch(
            uri,
            { 
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )
        .then(response => { 
            if(response.status != 200) {
                console.log("Error fetching competency questions")
                return 
            }
            return response.json()
        }).then(async (data) => {
            queryMetadata.value = data[id]
            queryContent.value = data[id]["content"]
            queryHtml.value = await codeToHtml(queryContent.value, { lang: 'sparql', theme: 'catppuccin-mocha', colorReplacements: { '#1e1e2e': '#1e293b' }})
        }).catch(err => {
            console.error("Error fetching competency questions: ", err)
        })
    }

    function fetchQueryResult() {
        fetch(queryMetadata.value.route, 
            {
                method: queryMetadata.value.method,
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then((response) => {
            console.log(response)
            if(response.status != 200) {
                isQueryError.value = true
                queryError.value = response.json()
                return
            } else {
                isQueryError.value = false
            }
            return response.json()
        }).then((data) => {
            queryResponse.value = data
            isQueryPerformed.value = true
            console.log(data)
        }).catch(err => {
            console.error("Error fetching data: ", err)
            isQueryError.value = true
            queryError.value = err
        })
    }
</script>



<template>
    <div class="flex justify-between items-start">
        <div>
            <h1 class="mb-1 text-2xl text-slate-900 font-bold">{{ queryMetadata.title }}</h1>
            <span class="text-md text-slate-600">{{ queryMetadata.name }}</span>
        </div>
        <div class="px-4 py-1 bg-sky-200 text-sky-500 rounded-sm">
            <NuxtLink :to="queryMetadata.route">{{ queryMetadata.smallRoute }}</NuxtLink>
        </div>
    </div>
    <div>
        <p class="my-6 text-lg text-slate-700">{{ queryMetadata.description }}</p>
    </div>
    <div class="my-10">
        <h2 class="text-xl text-slate-900 font-bold">Ontologies involved</h2>
        <div class="my-6 flex gap-4">
            <OntologyCard 
                v-for="(ontology, index) in queryMetadata.ontologies"
                :name="ontology.name"
                :shortName="ontology.shortName"
                :type="ontology.type"
                :description="ontology.description"
                :link="ontology.bioportalUrl"
            />
        </div>
    </div>
    <div class="mt-8 flex gap-6">
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
        </div>
        <div class="flex flex-col justify-between">
            <div>
                <h2 class="text-xl text-slate-900 font-bold">Datasources</h2>
                <div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>


<div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>
<div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>
<div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>
<div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>
<div class="my-4">
                    <div class="p-6 bg-slate-50 hover:bg-slate-100 rounded-md cursor-pointer">
                        <h3 class="text-slate-900 text-lg font-semibold">ABRomics database</h3>
                        <p class="my-4 text-slate-800">
                            <b>ABRomics</b> is a national platform designed to monitor the spread of antibiotic resistance genes in <b>human</b>, <b>animal</b> and <b>environmental</b>
                            reservoirs. 
                        </p>
                        <NuxtLink to="https://analysis.abromics.fr/" class="text-sky-500 font-semibold hover:underline">https://analysis.abromics.fr/</NuxtLink>
                    </div>
                </div>



            </div>
            <div class="my-4">
                <h2 class="text-xl text-slate-900 font-bold">Reuse this query</h2>
                <NuxtLink to="/sparql" class="my-4 p-4 bg-slate-50 flex justify-between rounded-md hover:bg-slate-100 hover:cursor-pointer">
                    <p>
                        <b>Reuse</b> this query as a <b>base</b> for your own
                    </p>
                    <img class="w-6 h-6" src="assets/arrow-right.svg">
                </NuxtLink>
            </div>
        </div>
    </div>
    <div class="w-full">
        <ActionButton
            content="Execute query"
            @click="fetchQueryResult(1)"
        >
        </ActionButton>
    </div>
    <div v-if="isQueryError" class="mt-6 py-2 px-4 bg-red-200 text-red-500 rounded-md">
        Error: {{ queryError }}
    </div>
    <div v-if="isQueryPerformed" class="my-6">
        <div class="flex justify-between items-center">
            <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
        </div>
        <Table :data="queryResponse" />
    </div>
</template>
