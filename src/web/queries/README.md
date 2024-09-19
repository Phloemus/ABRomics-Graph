# SPARQL Queries and competency questions

The SPARQL queries corresponding to the competency questions are listed here. The content of each request are availble 

- Q1: Search for antibiotic resistance genes in a specific biological sample
- Q2: List the TOP-K antibiotic resistance genes by coverage 
- Q2bis: List the TOP-K antibiotic resistance genes by sample type (human / animal / environment) 

## Q1: Search for antibiotic resistance genes in a specific biological sample:
 
This query allows get the sample having an identifier of **"F1361"**, get all
the observations associated with this sample and that have the observableProperty
labeled "Resistance gene". 

The query returns the simpleResults of these filtered observations. The simpleResults 
are strings corresponding to the name of the resistance gene

## Q2: List the TOP-K antibiotic resistance genes by coverage

get all the samples present in the graph and as well as the observableProperty with the label "Coverage %"
filter all the observations made on the samples for the specific coverage observableProperty and get the 
value of the coverage for each observations. 

The results are then returned in the coverage descending order (limited to 10 observations returned)  

## Q2bis: List the TOP-K antibiotic resistance genes by sample type (human / animal / environment) 

Get the list of the antibiotic genes the most present in specific sample types as well as the number 
of samples the resistance gene have been found in the samples
 
Getting only the samples having a sample type defined to "human" (this value can be changed to "animal" or "environmental"
to explore the list of the most present antibiotic resistance genes in those sample types). Filtration of the 
observations to have an observationProperty of "Resistance gene". Counts the number of each time a sample has the 
same gene_name in its linked observations. Returns a list of the k top antibiotic genes in descending order for 
a specific sample type


