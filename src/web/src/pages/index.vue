<script setup>
    import { ref } from 'vue'
    import PackedBubbleChart from '../components/PackedBubbleChart.vue'

    const { cdnURL, baseURL } = useRuntimeConfig().app
    const hostUrl = useRuntimeConfig().public.hostUrl

    // For SEO, page title, metadescriptions etc...
    useHead({
        title: 'ABRomics KG - Linking microbiome data',
        meta: [
          { name: 'description', content: 'ABRomics KG, an interoperable platform to analyse anti microbial resistance and perform data integration from different datasources' },
          { name: 'viewport', content: 'width=device-width, initial-scale=1.0' },
          { name: 'author', content: 'Brieuc Quemeneur' },
          { name: 'robots', content: 'index, follow' },
          { name: 'og:locale', content: 'en_US' },
          { name: 'og:type', content: 'website' },
          { name: 'og:description', content: 'ABRomics KG, an interoperable platform for anti microbial resistance analysis and data integration' },
          { name: 'og:title', content: 'ABRomics KG, an interoperable platform to analyse anti microbial resistance and perform data integration from different datasources' },
          { name: 'og:url', content: 'https://abromics-kg.bird.glicid.fr' },
          { name: 'og:site_name', content: 'ABRomics KG' },
          { name: 'og:image', content: `${hostUrl}/thumbnails/thumbnail.png` },
          { name: 'og:image:secure_url', content: `${hostUrl}/thumbnails/thumbnail.png` },
          { name: 'og:image:type', content: 'image/png' },
          { name: 'og:image:width', content: '1440' },
          { name: 'og:image:height', content: '740' },
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: `${cdnURL || baseURL}logos/abromicskg-logo-xs.svg` },
        ],
    })

    const testData = {
      name: "root",
      children: [
        {
          name: "Class A",
          children: [
            { name: "Big", value: 83 },
            { name: "Medium", value: 10 }
          ]
        },
        {
          name: "Class B",
          children: [
            { name: "Small1", value: 5 },
            { name: "Small2", value: 20 },
            { name: "Tiny", value: 1 }
          ]
        }
      ]
    }
    
    const config = useRuntimeConfig()

    var queryResponse = ref([])
    var isQueryPerformed = ref(false)
    var isQueryError = ref(false)
    var isQueryLoading = ref(false)
    var bubbleChartData = ref({name: "root", children: []})
    var queryError = ref("")

    const sparqlQuery = `
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl>
        PREFIX aro: <http://purl.obolibrary.org/obo/ARO_>
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX prov: <http://www.w3.org/ns/prov#>

        SELECT ?gene_name (COUNT(?gene_name) as ?total_nb_occurences) ?aroClass ?aroParentClass ?aroParentClassLabel
        FROM <http://www.ontotext.com/explicit>
        WHERE {

            ?sample rdf:type sio:001050 . 

            ?observableProperty rdf:type sosa:ObservableProperty ;
                rdfs:label 'Resistance gene' .

            ?gene rdf:type ncit:C16612 ;
                rdf:type ?aroClass ;
                rdfs:label ?gene_name .

            ?aroClass rdfs:subClassOf+ aro:3000000 ;
                rdfs:subClassOf ?aroParentClass .

            ?aroParentClass rdfs:subClassOf+ aro:3000000 ;
                rdfs:label ?aroParentClassLabel .

            ?observation sosa:observedProperty ?observableProperty ;
                sio:000332 ?sample ;
                sosa:hasFeatureOfInterest ?gene .

        } GROUP BY ?gene_name ?aroClass ?aroParentClass ?aroParentClassLabel 
        ORDER BY DESC(?total_nb_occurences)
    `

    function fetchQueryResult() {
        isQueryLoading.value = true
        isQueryError.value = false
        isQueryPerformed.value = false
        const uri = config.public.apiUrl + "/query/custom"
        fetch(uri,
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "query": sparqlQuery
                })
            }
        ).then((response) => {
            console.log(response)
            if(response.status != 200) {
                isQueryError.value = true
                queryError.value = response.json()
                return
            } else {
                isQueryError.value = false
                isQueryLoading.value = false
            }
            return response.json()
        }).then((data) => {
            queryResponse.value = data.results
            isQueryPerformed.value = true
            console.log(data)
            generatePackedBubblePlotData(data)
            isQueryLoading.value = false
            console.log(data)
        }).catch(err => {
            console.error("Error while processing response: ", err)
            isQueryError.value = true
            queryError.value = "The syntax of the query wrong or empty"
            isQueryLoading.value = false
        })
    }

    function generatePackedBubblePlotData(data) {
        var plotData = {
          name: "root",
          children: []
        };

        var parentAroClasses = []
        var parentAroClassesLabels = []

        const dataFiltered = data.results.filter(item => item.total_nb_occurences.value > 1 && data.results.filter(i => i.aroParentClass.value == item.aroParentClass.value).length > 1 ) // Check if the item.parentAroClass is unincluded 

        dataFiltered.forEach(item => {
            parentAroClasses.push(item.aroParentClass.value)
            parentAroClassesLabels.push(item.aroParentClassLabel.value)
        });

        parentAroClasses = [...new Set(parentAroClasses)];
        parentAroClassesLabels = [...new Set(parentAroClassesLabels)];

        parentAroClassesLabels.forEach(parentAroClassLabel => {
            plotData.children.push({name: parentAroClassLabel, children: []})
        })

        dataFiltered.forEach(item => {
            const bubbleData = { name: item.gene_name.value, value: item.total_nb_occurences.value }
            const index = parentAroClasses.indexOf(item.aroParentClass.value)
            plotData.children[index].children.push(bubbleData)
        })
        
        bubbleChartData.value = plotData
        console.log(plotData)
    }

    fetchQueryResult()

</script>

<template>
    <div class="">
        <div class="mx-auto my-10">
            <h1 class="mx-6 mb-6 text-center text-3xl text-slate-900 leading-relaxed font-bold">Welcome to ABRomics KG</h1>
            <p class="sm:mx-6 md:mx-auto md:max-w-screen-sm md:mt-8 md:mb-6 text-lg text-slate-600 text-center">
                Level up your data exploration with <span class="text-pink-500 font-medium">ABRomics Knowlegde Graph</span>, the best <span class="text-purple-500 font-medium">interoperable</span> platform to track and analyse anti-microbial resistance
            </p>
            <div class="md:flex md:justify-center">
                <div class="mx-2 sm:mx-6 md:mx-0 my-14 md:my-6 md:flex md:gap-2">
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <p class="py-1 text-xl text-slate-800 font-semibold">18.1</p> 
                        <p class="text-md text-slate-500 font-medium">million nodes</p>
                    </div>
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <p class="py-1 text-xl text-slate-800 font-semibold">xx.x</p> 
                        <p class="text-md text-slate-500 font-medium">antibiotic resistance genes</p>
                    </div>
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <p class="py-1 text-xl text-slate-800 font-semibold">xx</p> 
                        <p class="text-md text-slate-500 font-medium">different datasources</p>
                    </div>
                </div>
            </div>
            <div class="mx-2 mt-10 lg:hidden flex justify-center">
                <NuxtLink to="/query" class="px-10 py-3 bg-slate-900 text-md font-medium hover:bg-slate-800 text-white text-md flex gap-4 items-center rounded-md">
                    <span>Start Exploring</span>
                </NuxtLink>
            </div>
        </div>
        <div class="mx-auto max-w-screen-lg">
            <div class="mx-4 my-16 lg:my-20">
                <h2 class="text-slate-800 text-2xl font-semibold">Consult the data</h2>
                <p class="my-6 text-lg text-slate-600">
                    In close relation with the <NuxtLink to="https://analysis.abromics.fr" class="text-sky-500 hover:underline">ABRomics</NuxtLink> platform, we propose an alternative data structure with interoperability 
                    first in mind.
                </p>
                <p class="my-6 text-lg text-slate-600">
                    Our knowledge graph contains data from the <NuxtLink to="https://analysis.abromics.fr" class="text-sky-500 hover:underline">ABRomics</NuxtLink> platform and provide a structure compatible 
                    with W3C standards. The structured data is available directly to anyone using the SPARQL language through our
                    endpoint.
                </p>
                <p class="my-6 text-lg text-slate-600">
                    Overall, ABRomics KG, provide a FAIR structured Knowledge Graph and an ecosystem of tools for external data 
                    integration, quering, data exploration and pattern recognition. 
                </p>
            </div>
            <div class="mx-4 my-16">
                <h2 class="text-slate-800 text-2xl font-semibold">Visualize the data</h2>
                <p class="my-6 text-lg text-slate-600">
                    <NuxtLink to="/integration" class="text-sky-500 hover:underline">Integrate</NuxtLink> your research data into the ABRomics Knoweldge Graph to combine your samples with public data 
                    to see matching returns or explore redundant patterns !
                </p>
                <h3 class="text-slate-800 text-lg font-semibold">Want the full ABRomics experience ?</h3>
                <p class="my-4 text-lg text-slate-600">
                    <NuxtLink to="/tutorials/bind-accounts" class="text-sky-500 hover:underline">Follow</NuxtLink> our guide to bind your ABRomics account to ABRomics KG
                </p>     
            </div>
        </div>
    </div>
    <!--
    <div>
        <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Knowledge graph content</h2>
        <div v-if="!isQueryError && !isQueryLoading">
            <PackedBubbleChart :data="bubbleChartData"/>
        </div>
    </div>
    -->
</template>
