<script setup>
    import { ref } from 'vue'
    import { useRoute } from 'vue-router'

    import { codeToHtml } from 'shiki'

    import ActionButton from "../../components/ActionButton.vue"
    import Table from "../../components/Table.vue"

    import queries from '../../static/queries.json'
    import query from '../../static/cq1.json'

    const route = useRoute()
    const queryId = route.params.id - 1
    const queryFilename = queries[queryId].sparqlQuery
    const ontologies = queries[queryId].ontologies
    const queryApiLink = `http://localhost:5000/graph-api/${queries[queryId].apiLink}`

    const queryHtml = await codeToHtml(query.content, { lang: 'sparql', theme: 'catppuccin-mocha', colorReplacements: { '#1e1e2e': '#1e293b' }})

    var queryResponse = ref([])
    var isQueryPerformed = ref(false)
    console.log(isQueryPerformed)

    function fetchQueryResult(id) {
        console.log(id)
        // Don't forget to change the port or the host in prod ;)
        fetch(`http://localhost:5000/graph-api/${queries[queryId].apiLink}`).then(response => { 
            return response.json()
        }).then((data) => {
            console.log(data)
            queryResponse.value = data
            isQueryPerformed.value = true
        }).catch(err => {
            console.error("Error fetching data: ", err)
        })
    }
</script>



<template>
    <div class="flex justify-between items-start">
        <div>
            <h1 class="mb-1 text-2xl text-slate-900 font-bold">{{ queries[queryId].title }}</h1>
            <span class="text-md text-slate-600">{{ queries[queryId].name }}</span>
        </div>
        <div class="px-4 py-1 bg-sky-200 text-sky-500 rounded-sm">
            <NuxtLink :to="queryApiLink">{{ queries[queryId].apiLink }}</NuxtLink>
        </div>
    </div>
    <div>
        <p class="my-6 text-lg text-slate-700">{{ queries[queryId].description }}</p>
    </div>
    <div>
        <h2 class="text-xl text-slate-900 font-bold">Ontologies involved</h2>
        <div class="my-6 flex gap-4">
            <OntologyCard 
                v-for="(ontology, index) in ontologies"
                :name="ontology.name"
                :shortName="ontology.shortName"
                :type="ontology.type"
                :description="ontology.description"
                :link="ontology.bioportalUrl"
            />
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
    <div v-show="isQueryPerformed" class="my-6">
        <div class="flex justify-between items-center">
            <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
        </div>
        <!-- <Table :data="queryResponse"/> -->
    </div>
</template>
