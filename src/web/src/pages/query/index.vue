<script setup>

    const config = useRuntimeConfig();

    // local states
    const queries = ref([])

    // on render
    getCompetencyQuestions()

    function getCompetencyQuestions() {
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
        }).then((data) => {
            queries.value = data
        }).catch(err => {
            console.error("Error fetching competency questions: ", err)
        })
    }

</script>

<template>
    <div class="flex justify-between items-start">
        <div>
            <h1 class="mb-1 text-2xl text-slate-900 font-bold">List of all the prewritten queries</h1>
        </div>
        <div class="px-4 py-1 bg-sky-200 text-sky-500 rounded-sm">
            <NuxtLink :to="'/query'">/query</NuxtLink>
        </div>
    </div>
    <div>
        <p class="my-6 text-lg text-slate-700">
            Discover a lot of prewritten queries that will help you discover the knowledge graph, 
            understand its structure and get ideas to create your own queries !
        </p>
    </div>
    <div class="my-6">
        <h3 class="my-6 text-slate-600 text-lg">Competency questions</h3>
        <div class="mx-4">
            <SmallCard 
                v-for="(query, index) in queries"
                :title="query.name"
                :description="query.title"
                :link="`/query/${query.id}`"
            />
        </div>
    </div>
</template>