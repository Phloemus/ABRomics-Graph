<script setup>

</script>

<template>
    <div class="p-8 flex justify-between items-start">
        <div>
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
</template>
