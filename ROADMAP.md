# Abromics KG Roadmap

The ABRomics KG project has to store data in a graph format to make possible data annotation with existing 
ontologies and to allow to perform queries to multiple datasources with a single request.

The ABRomics KG project also have to follow the structuration of the data imposed by the ABRomics project 
as well as providing an interface to ensure a smooth connexion with between the two part of the project

## Milestones

1. Creating a knowedge graph that both uses ontologies already in use in similar project and that makes 
sens in the case of the ABRomics project (as well as the **MUDIS4LS** and **CLOUD4SAMS projects**)

2. Providing a tool that is capable to extract data from the ABRomics relational database and enrich this 
data with pre-selected ontologies

3. Providing and interface tool capable to perform custom SPARQL requests directly onto the knwoledge graph
with enbeded security measure to pervent private data from leaking out

4. Providing a programming interface giving the possibility to the ABRomics frontend and backend to perform 
stereotyped requests onto the graph without ever having to manually call the SPARQL endpoint themselves

## Passive goals

1. Creating a tool that could be exported anywhere : the machine that will run the knowledge graph could change
and the codebases should allow fast deployment if an other instance is needed for testing purposes or for a full
production redeployment

## Tasks

1. **Make the set_up.sh file trigger on virtuoso container launch**: It would be great make the set_up.sh file
automatically trigger when the virtuoso container has been launched to prevent having to perform a manual docker 
exec to trigger the script and to integrate the graph files to the virtuoso graph database
