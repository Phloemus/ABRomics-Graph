<script>

    import SearchInput from "../components/SearchInput.vue"

    // import data from "../static/result-10k-first-classes.json"
    import data from "../static/test-classes.json"

    const searchTerm = ref("")
    const organs = ref([])

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

    <SearchInput 
        :searchTerm="searchTerm"
        @input="filterOntologyList"
        placeholder="Searching an ontology term.."
        :results="organs"
    />

</template>
