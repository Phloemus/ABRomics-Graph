<script setup>

    import { ref } from 'vue'
    import WorldMap from '~/components/WorldMap.vue'
    import DonutChart from '~/components/DonutChart.vue'

    import { codeToHtml } from 'shiki'

    const { cdnURL, baseURL } = useRuntimeConfig().app
    const hostUrl = useRuntimeConfig().public.hostUrl
    const apiUrl = useRuntimeConfig().public.apiUrl
    const appName = useRuntimeConfig().public.appName

    // To store the competency questions data
    const queryMetadata = ref({})
    const queryContent = ref("")
    const queryHtml = ref({})

    const queries = ref([])

    // For SEO, page title, metadescriptions etc...
    useHead({
        title: `${appName} - Linking microbiome data`,
        meta: [
          { name: 'description', content: `${appName}, an interoperable platform to analyse anti microbial resistance and perform data integration from different datasources` },
          { name: 'viewport', content: 'width=device-width, initial-scale=1.0' },
          { name: 'author', content: 'Brieuc Quemeneur' },
          { name: 'robots', content: 'index, follow' },
          { name: 'og:locale', content: 'en_US' },
          { name: 'og:type', content: 'website' },
          { name: 'og:description', content: `${appName}, an interoperable platform for anti microbial resistance analysis and data integration` },
          { name: 'og:title', content: `${appName}, an interoperable platform to analyse anti microbial resistance and perform data integration from different datasources` },
          { name: 'og:url', content: `${hostUrl}` },
          { name: 'og:site_name', content: `${appName}` },
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

    // Shiki code to display the competency question query
    getCompetencyQuestion(0)

    // Get the competency qestions to showcase how the knowledge graph works
    getCompetencyQuestions()

    function getCompetencyQuestion(id) {
        const uri = apiUrl + "/query/competency-question"
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

    function getCompetencyQuestions() {
        const uri = apiUrl + "/query/competency-question"
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

    // sample resistance genes data
    const genes = {
        blaTEM: 182,
        tetA: 90,
        sul1: 23,
        aadA1: 45,
        qnrS: 67
    }

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

    var nbAllNodes = ref("xx.x")
    var nbResistanceGenes = ref("xxx")

    const countAllNodesQuery = `
        SELECT (COUNT(*) AS ?count) WHERE {
   	        ?s ?p ?o .
        }
    `

    const countNbResistanceGenesQuery = `
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX schema: <https://schema.org/>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl>
        PREFIX aro: <http://purl.obolibrary.org/obo/ARO_>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT (COUNT(?gene) as ?gene_nb)
        FROM <http://www.ontotext.com/explicit>
        WHERE {
            ?sample rdf:type sio:001050 .

            ?observableProperty rdf:type sosa:ObservableProperty ;
                rdfs:label 'Resistance gene' .

            ?observation sosa:observedProperty ?observableProperty ;
                sio:000332 ?sample ;
                sosa:hasFeatureOfInterest ?gene .

            ?gene rdf:type ncit:C16612 ;
                rdf:type [ rdfs:subClassOf+ aro:3000000 ] ;
                rdfs:label ?gene_name .
        }
    `

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

    function getTotalNbNodes() {
        const uri = apiUrl + "/query/custom"
        fetch(uri,
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "query": countAllNodesQuery
                })
            }
        ).then((response) => {
            console.log(response)
            if(response.status != 200) {
                console.log(response.json())
                return
            }
            return response.json()
        }).then((data) => {
            nbAllNodes.value = data.results[0].count.value
            console.log(data.results[0].count.value)
        }).catch(err => {
            console.error("Error while processing response: ", err)
        })

    }

    function getTotalNbResistanceGenes() {
        const uri = apiUrl + "/query/custom"
        fetch(uri,
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "query": countNbResistanceGenesQuery 
                })
            }
        ).then((response) => {
            console.log(response)
            if(response.status != 200) {
                console.log(response.json())
                return
            }
            return response.json()
        }).then((data) => {
            nbResistanceGenes.value = data.results[0].gene_nb.value
            console.log(data.results[0].gene_nb.value)
        }).catch(err => {
            console.error("Error while processing response: ", err)
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

    function formatNumber(num) {
      if (num >= 1_000_000_000) {
        return `${(num / 1_000_000_000).toFixed(1).replace(/\.0$/, '')}b`;
      }
      if (num >= 1_000_000) {
        return `${(num / 1_000_000).toFixed(1).replace(/\.0$/, '')}m`;
      }
      if (num >= 1_000) {
        return `${(num / 1_000).toFixed(1).replace(/\.0$/, '')}k`;
      }
      return num.toString();
    }

    fetchQueryResult()
    getTotalNbResistanceGenes()
    getTotalNbNodes()

</script>

<template>
    <div class="">
        <div class="px-2 mx-auto my-10">
            <h1 class="mx-6 mb-6 text-center text-3xl text-slate-900 leading-relaxed font-bold">Welcome to {{appName}}</h1>
            <p class="sm:mx-6 md:mx-auto md:max-w-screen-sm md:mt-8 md:mb-6 text-lg text-slate-600 text-center">
                Level up your data exploration with <span class="text-pink-500 font-medium">ABRomics Knowlegde Graph</span>, the best <span class="text-purple-500 font-medium">interoperable</span> platform to track and analyse anti-microbial resistance
            </p>
            <div class="md:flex md:justify-center">
                <div class="mx-2 sm:mx-6 md:mx-0 my-14 md:my-6 md:flex md:gap-2">
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <div v-if="nbAllNodes == 'xx.x'" class="my-3 h-3 w-20 animate-pulse bg-slate-200 rounded"></div>
                        <p v-else-if="nbAllNodes != 'xx.x'" class="py-1 text-xl text-slate-800 font-semibold">{{ formatNumber(nbAllNodes) }}</p> 
                        <p class="text-md text-slate-500 font-medium">nodes</p>
                    </div>
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <div v-if="nbResistanceGenes == 'xxx'" class="my-3 h-3 w-20 animate-pulse bg-slate-200 rounded"></div>
                        <p v-else-if="nbResistanceGenes != 'xxx'" class="py-1 text-xl text-slate-800 font-semibold">{{ nbResistanceGenes }}</p> 
                        <p class="text-md text-slate-500 font-medium">antibiotic resistance genes</p>
                    </div>
                    <div class="my-2 px-4 py-2 md:w-72 bg-white rounded-md border border-slate-200 cursor-pointer">
                        <p class="py-1 text-xl text-slate-800 font-semibold">1</p> 
                        <p class="text-md text-slate-500 font-medium">different datasources</p>
                    </div>
                </div>
            </div>
            <div class="mx-2 mt-10 lg:hidden flex justify-center gap-2">
                <NuxtLink to="/query" class="px-10 py-3 bg-slate-900 text-md font-medium hover:bg-slate-800 text-white text-md flex gap-4 items-center rounded-md">
                    <span>Start Exploring</span>
                </NuxtLink>
                <NuxtLink to="https://github.com/Phloemus/ABRomics-Graph" class="p-2 bg-white rounded-md border border-slate-200 hover:bg-slate-50">
                    <img class="h-8 w-8" src="assets/github-icon.svg" />
                </NuxtLink>
            </div>
            <div class="my-10 flex justify-center">
                <hr class="w-56 fill-slate-200 border border-slate-200 rounded-sm">
            </div>
            <div class="mx-2 my-10 flex md:justify-center">
                <div class="flex flex-col gap-2 w-full max-w-screen-lg">
                    <div class="mt-6">
                        <h2 class="text-slate-800 text-2xl text-center font-semibold">Explore samples from all around the world</h2>
                        <p class="my-6 text-lg text-center text-slate-600">
                            In close relation with the <NuxtLink to="https://analysis.abromics.fr" class="text-sky-500 hover:underline">ABRomics</NuxtLink> platform, we propose an alternative database with interoperability 
                            first in mind. Ideal for world wide data exploration !
                        </p>
                    </div>
                    <div class="">
                        <div class="w-full bg-white rounded-md border border-slate-200">
                            <div class="py-4 px-0">
                                <WorldMap />
                            </div>
                            <div class="py-2 px-4 w-full bg-slate-100 flex justify-between">
                                <div class="flex gap-3 items-center">
                                    <div class="h-2 w-2 bg-green-500 rounded-full"></div>
                                    <NuxtLink to="/map" class="text-sm text-slate-600 hover:underline hover:cursor-pointer">samples world map</NuxtLink>
                                </div>
                            </div>
                        </div>
                        <div class="mt-20 lg:hidden">
                            <h2 class="text-slate-800 text-2xl font-semibold text-center">Visualize growing public health threat head of time</h2>
                            <p class="my-6 text-lg text-slate-600 text-center">
                                Use {{ appName }} visualization tools to track anti-microbial resistance genes and identify emerging threat to public 
                                safety before they occur. 
                            </p>
                        </div>
                        <div class="lg:mt-6 w-full bg-white rounded-md border border-slate-200">
                            <div class="py-4 px-0 lg:px-6 lg:py-6">
                                <DonutChart :data="genes" />
                            </div>
                            <div class="py-2 px-4 w-full bg-slate-100 flex justify-between">
                                <div class="flex gap-3 items-center">
                                    <div class="h-2 w-2 bg-green-500 rounded-full"></div>
                                    <NuxtLink to="/" class="text-sm text-slate-600 hover:underline hover:cursor-pointer">samples resistance genes</NuxtLink>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-20 md:hidden">
            <div class="w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
            <div class="py-10 bg-slate-800 border-b-2 border-slate-600">
                <h2 class="px-8 text-white text-2xl font-semibold text-center">Want to have a look to a gene you study ?</h2>
                <p class="px-4 my-6 text-lg text-slate-100 text-center">
                    Check if a resistance gene you study is present in other researchers datasets now !
                </p>
                <div class="mt-12 px-4">
                    <input 
                        class="w-full px-4 py-2 bg-slate-700 placeholder:italic placeholder:text-slate-500 border border-slate-800 focus:outline-none text-slate-100 rounded-md" 
                        placeholder="Enter a gene name"     
                    />
                    <div class="mt-6 flex justify-center">
                        <button class="px-1 py-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-md">
                            <span class="px-8 py-2 bg-slate-50 text-lg text-slate-800 rounded-md">Search</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="mx-auto my-14 flex justify-center max-w-screen-lg hidden lg:block">
            <hr class="w-56 fill-slate-200 border border-slate-200 rounded-sm">
        </div>
        <div class="mx-auto max-w-screen-lg">
            <div class="mx-4 my-16 lg:my-20">
                <h2 class="text-slate-800 text-2xl text-center font-semibold">Perform your own query</h2>
                <p class="my-6 text-lg text-slate-600 text-center">
                    Our knowledge graph contains data from the <NuxtLink to="https://analysis.abromics.fr" class="text-sky-500 hover:underline">ABRomics</NuxtLink> platform and provide a structure compatible 
                    with W3C standards. The structured data is available directly to anyone using the SPARQL language through our
                    endpoint.
                </p>
                <p class="my-6 text-lg text-slate-600 text-center">
                    Overall, {{ appName }}, provide a FAIR structured Knowledge Graph and an ecosystem of tools for external data 
                    integration, quering, data exploration and pattern recognition. 
                </p>
                <div class="my-14">
                    <NuxtLink to="/query/1">
                        <h3 class="text-xl text-slate-800 font-semibold">Get all the resistance genes found in a specific sample</h3>
                        <span class="text-slate-400 text-md">competency question 1</span>
                    </NuxtLink>
                    <div class="my-4 w-full bg-slate-800 rounded-md">
                        <div class="py-2 px-4 flex items-center justify-between border-b border-slate-700">
                            <span class="text-white">sparql</span>
                            <div class="flex items-center gap-2">
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                            </div>
                        </div>
                        <div class="p-4 w-full bg-slate-800 rounded-b-md overflow-scroll">
                            <code>
                                <div v-html="queryHtml"></div>
                            </code>
                        </div>
                    </div>
                    <div class="px-2 py-1 bg-white rounded-sm">
                        <SmallCard 
                            v-for="(query, index) in queries.slice(1, 5)"
                            :title="query.name"
                            :description="query.title"
                            :link="`/query/${query.id}`"
                        />
                    </div>
                </div>
            </div>
            <div class="mx-4 my-16">
                <h2 class="text-slate-800 text-2xl text-center font-semibold">Integrate your own data</h2>
                <p class="my-6 text-lg text-slate-600 text-center">
                <NuxtLink to="/integration" class="text-sky-500 hover:underline">Integrate</NuxtLink> your research data into the {{ appName }} to combine your samples with public data 
                    to see matching returns or explore redundant patterns !
                </p>
                <h3 class="text-slate-800 text-lg text-center font-semibold">Want the full ABRomics experience ?</h3>
                <p class="my-4 text-lg text-slate-600 text-center">
                    <NuxtLink to="/tutorials/bind-accounts" class="text-sky-500 hover:underline">Follow</NuxtLink> our guide to bind your ABRomics account to {{ appName }}
                </p>     
            </div>
        </div>
    </div>
    <footer>
        <div class="w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
        <div class="px-6 mt-16 sm:flex sm:justify-between">
            <div class="my-16">
                <div class="my-8">
                    <span class="text-slate-800 font-medium">Quick access</span>
                    <ul class="my-4">
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Perform a Query</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Map exploration</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Submit my data</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Integrate {{ appName }}</NuxtLink></li>
                    </ul>
                </div>
                <div class="my-8">
                    <span class="text-slate-800 font-medium">Documentation</span>
                    <ul class="my-4">
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Check our data model</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Write your own query</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Index new data</NuxtLink></li>
                        <li class="my-2 text-slate-600 hover:underline cursor-pointer"><NuxtLink>Analyse with our model</NuxtLink></li>
                    </ul>
                </div>
            </div>
            <div class="my-8">
                <div>
                    <p class="my-1 text-slate-800 text-lg">{{ appName }} - {{ new Date().getFullYear() }}</p>
                    <p class="text-slate-600 text-sm">Linking micrombiome data</p>
                </div>
            </div>
        </div>
    </footer>
    <!--
    <div>
        <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Knowledge graph content</h2>
        <div v-if="!isQueryError && !isQueryLoading">
            <PackedBubbleChart :data="bubbleChartData"/>
        </div>
    </div>
    -->
</template>
