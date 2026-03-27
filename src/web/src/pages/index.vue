<script setup>
    import { ref } from 'vue'
    import PackedBubbleChart from '../components/PackedBubbleChart.vue'

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
        const uri = config.public.graphServerUrl + "/repositories/abromics-kg?query=" + encodeURIComponent(sparqlQuery)
        fetch(uri,
            {
                method: "GET",
                headers: {
                    'Content-Type': 'application/sparql-query',
                    'Accept': 'application/sparql-results+json'
                }
            }
        ).then((response) => {
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
            queryResponse.value = data.results.bindings
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

        const dataFiltered = data.results.bindings.filter(item => item.total_nb_occurences.value > 1 && data.results.bindings.filter(i => i.aroParentClass.value == item.aroParentClass.value).length > 1 ) // Check if the item.parentAroClass is included 

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
    <div class="p-8 flex justify-between items-start">
        <div>
            <div class="mb-8 p-4 w-full bg-sky-100 rounded-md flex justify-between">
                <p class="text-sky-500 text-md font-medium">Check the full graph schema documentation</p>
                <a class="text-sky-500 text-md font-medium hover:underline" href="docs/">Go to docs</a>
            </div>
            <h1 class="mb-10 text-3xl text-slate-900 font-bold">Welcome to ABRomics KG</h1>
            <p class="my-6 text-lg text-slate-700 leading-8">
                Understanding how antibiotic resistance genes spread is essential for protecting human, animal, and environmental health. It requires collaboration across multiple fields and expertise under One Health initiatives, emphasizing the pressing need to consolidate diverse antibiotic data from human, animal, and environmental samples. 
            </p>
            <p class="my-6 text-lg text-slate-700 leading-8">
            In this paper, we propose a domain-specific Knowledge Graph leveraging the SOSA ontology to uniformly represent multi-modal data and their analysis while allowing the description of provenance metadata covering both time and geographical locations. This work is driven by a national consortium of antibiotic resistance experts (ABRomics). 
            </p>
            <p class="my-6 text-lg text-slate-700 leading-8">
            As experimental results, we show how this domain knowledge can be used to answer a specific expert question as well as increasing the FAIRness of antibiotic resistance data.
            </p> 
            <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Summary</h2>
            <ul>
                <li>Dataset</li>
                <li>Knowledge graph structure</li>
                <li>Execute demo queries</li>
                <li>Count query</li>
                <li>Antibiotic resistances by country</li>
                <li>Antibiotic resistances in different timeframes</li>
            </ul>
            <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Dataset</h2>
            <p class="my-6 text-lg text-slate-700 leading-8">
                The knowledge graph has been created using public metadata and antibiotic resistance analysis data from the ABRomics plateform.
            </p>
            <p class="my-6 text-lg text-slate-700 leading-8">
                The genomic sequences and metadata of multiple harmfull strains of bacterias found in human, animal and environmental origins have been integrated and processed into the ABRomics platform. The resulting 1613 analysis reports gather sample metadata as well as antibiotic resistance genes detected with the ABRomics bioinformatics workflows were then extracted and formated using the graph structure described below.
            </p>
            <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Knowledge graph structure</h2>
            <div class="px-10 w-full flex flex-col gap-10">
                <img src="assets/sample-modelisation-sosa.png"/>
                <img src="assets/measure-modelisation-sosa.png"/>
            </div>
        </div>
    </div>
    <div>
        <h2 class="mt-10 mb-6 text-xl text-slate-900 font-bold">Knowledge graph content</h2>
        <div v-if="!isQueryError && !isQueryLoading">
            <PackedBubbleChart :data="bubbleChartData"/>
        </div>
    </div>
</template>
