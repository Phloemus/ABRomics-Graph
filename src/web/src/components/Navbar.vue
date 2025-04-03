<script setup>

    // Imports
    import SearchInput from './SearchInput.vue'

    // Global state
    const isUserLoggedIn = useState('isUserLoggedIn')
    const userAuthToken = useState('userAuthToken')
    const isLoginPanelOpened = useState('isLoginPanelOpened')

    function displayLoginPanel() { 
        isLoginPanelOpened.value = true
    }

    async function logout() {
        isUserLoggedIn.value = false
        userAuthToken.value = ""
        await navigateTo("/")
    }

    const searchTerm = ref("")
    const organs = ref([])

    const data = { "head": { "link": [], "vars": ["specie", "organs", "organLabels"] },
  "results": { "distinct": false, "ordered": true, "bindings": [
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0000038" }	, "organLabels": { "type": "literal", "value": "follicular fluid" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0000170" }	, "organLabels": { "type": "literal", "value": "pair of lungs" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0001814" }	, "organLabels": { "type": "literal", "value": "brachial nerve plexus" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0003254" }	, "organLabels": { "type": "literal", "value": "amniotic ectoderm" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0003262" }	, "organLabels": { "type": "literal", "value": "amniotic mesoderm" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0003725" }	, "organLabels": { "type": "literal", "value": "cervical nerve plexus" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0004100" }	, "organLabels": { "type": "literal", "value": "renal collecting system" }},
    { "specie": { "type": "uri", "value": "http://purl.obolibrary.org/obo/NCBITaxon_9606" }	, "organs": { "type": "uri", "value": "http://purl.obolibrary.org/obo/UBERON_0034713" }	, "organLabels": { "type": "literal", "value": "cranial neuron projection bundle" }} ], }, }

    data.results.bindings.forEach((data) => {
        organs.value.push({ "name": data.organLabels.value, "ontology": data.organs.value })
    })

    function filterOntologyList(event) {
        console.log("hahaha")
        searchTerm.value = event.target.value
        console.log(searchTerm.value)
        const query= searchTerm.value.toLowerCase();
        organs.value = []
        data.results.bindings.forEach(suggestion => {
            if(suggestion.organLabels.value.toLowerCase().includes(query)) {
                const elem = {
                    "name": suggestion.organLabels.value,
                    "ontology": suggestion.organs.value
                }
                organs.value.push(elem)
            }
        });
    }

</script>

<template>
    <nav class="px-6 py-3 w-full flex justify-between items-center bg-white border-b border-slate-200">
        <SearchInput 
            :searchTerm="searchTerm"
            @input="filterOntologyList"
            placeholder="Search for ontology term.."
            :results="organs"
        />
        <div class="flex flex-row-reverse gap-4">
            <ActionButton @click="displayLoginPanel" v-show="!isUserLoggedIn" content="Login"/>
            <SecondaryButton @click="logout" v-show="isUserLoggedIn" content="Log out"/>
        </div>
    </nav>
</template>
