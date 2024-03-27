# ABRomics KG 

Abromics KG correspond to the WP2.4 of the Abromics project, which should ensure the FAIR principles by using 
finding appropriate ontologies for Abromics usecases and setting up a knowledge graph to integrate more data
in the graph.

## Main goals of ABRomics KG

The ABRomics KG provide a graph in which the ABRomics platforme can get data from and easily get access to 
informations available in other knowledge graphs provided by external data sources.

1. Provide graph structure for the ABRomics data that can support SPARQL request making the project more FAIR
2. Laverage the graph structure to access fine descriptions in external specific ontologies. Making possible
   queries that will give more information about the entities manipulated in the graph.
3. Provide a way to make requests to external graph databases
4. Provide an integration of the graph with existing ABRomics codebase and compatibility with the relational 
   database set up by the developping team

## Download the codebase of the project

To get the whole codebase of the ABRomics-kg project run:

```
bash 
git clone https://gitlab.univ-nantes.fr/BiRD/abromics-kg.git
```

## Parts of the project

To ensure the goal written previously, ABRomics KG is composed of multiple parts.

### Graph structure

The design of the graph structure require to have a deep understanding of the underlying ontologies that are 
used to make such knowledge graph. The goal of the knowledge graph is to be a close representation of the 
data that are used in ABRomics as well as keeping the relations between the data. A knowledge graph define 
the structure that all data should be following. This is important to ensure that the data instanciated 
with the knowledge graph follows a consistant structure, so users know how to retrive data from the graph
using SPARQL requests (which will be consistant as the sturcture of the graph is). 

Thus the structure of the graphs should:

1. Follow the terms of ontologies of references (ontologies that are already used by a lot of people and 
   which have their structure proven to be efficient to represent data)
2. Use the terms of the ontology that are relevant to the ABRomics project. This means that all the 
   data treatment made by ARBomics must be represented in a way in the knowledge graph

### Set up the projet correctly

The project contains multiple parts but is as portable as possible. Follow all the instruction below to 
host the ABRomics KG on a server (which could be a physical machine or a VM)

Pay attention to:

1. Have the right hardware
2. Setting up the different software with the version indicated below

#### Necessary hardware and software to install

Necessary hardware: 

- A physical machine or VM with at least 20Go of memory and 16Go of RAM

Necessary software:

- A linux OS (preferably a Debian derived distro like Ubuntu)
- Anaconda (to enable different python environment)
- Nginx server (with configurations corresponding to the ones present in the project)
- Virtuoso server (opensource distribution)

The project has been tested on:

- Ubuntu server 22.04 LTS | 19.20 GB
    - Anaconda 1.12.1
    - conda 23.7.4
    - nginx/1.18.0 (Ubuntu) | built with OpenSSL 3.0.2
    - virtuso 7.2.11 (Virtuoso Open Source Edition)

### Setting up with Docker 

Build the Docker image of the project with this command

```
bash
# in the project directory where there is the Dockerfile
docker build -t abromics-kg .
```

Check if there is the abromics-kg docker image that can be used to create the container

```
bash
docker images
```

Running the Docker image of the project with this command

```
bash
docker run --name my-nginx-container -d -p 8081:80 abromics-kg
```

Go to the nginx default webpage on *localhost:8081*

#### Setting up the VM 

--> I don't have enough knowledge to set up an Ubuntu VM. This section should be filled in when the 
--> information will be available 

#### Installing nginx

-- continue

#### Installing Anaconda 

Download Anaconda

```
bash
cd ~/
curl https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
chmod +x Anaconda3-2024.02-1-Linux-x86_64.sh
./Anaconda3-2024.02-1-Linux-x86_64.sh
```

Fill the fields the installer asks for. Then source your **.bashrc** as Anaconda adds the path to the **conda**
program in PATH. 

```
bash 
source ~/.bashrc
```

Try to use **conda**

```
bash 
conda --version
```

If conda is an unknown command, simply add this line to you **.bashrc**

```
bash 
nano ~/.bashrc
# Add conda disponible from everywhere on the system
export PATH=~/anaconda3/bin:$PATH
```

**conda** should be usable from anywhere in your system now

```
bash
# Should display the version of conda 
conda --version
```

#### Installing virtuoso 

--- continue the documentation of the virtuoso installation

### Setting up the python envrionments

Conda environments are sets of python packages with fixed versions that are bundled together. Having multiple 
conda environments reduce the risk of incompatibilites/conflict between python packages as well as ensuring
maximum portability of the codebase.

1. **FastAPI environment:** (env-name: *fastAPI-env*) : Environment to activate to be able to use the API of the 
   ABRomics KG project. This is a rest API using the FastAPI package of python and which allows a client to 
   perform simple CRUD on the graph only by calling the API endpoint instead of doing some sort of SPARQL
   requests. 

2. **Analysis environment:** (env-name: *analysis-env*) : Environment with SPARQL Wrapper (package that helps
   to perform SPARQL requests) and jupyter lab. This environment is perfect to do analysis on the graph with 
   some jupyter notebooks.

3. **Streamlit environment:** (env-name: *streamlit-env*) : Environment with all the packages necessary to 
   launch the demo web page. These webpages serves as visual demonstrations of SPARQL queries, how to use 
   them and how to build relevant SPARQL requests relying on the structure of the knowledge graph.

To create the following conda environments there you have to create them using their respective environment.yaml
files present in <project-name>/envs/<env-name>

```
bash
## replace <env-name> with the name of the environment you want to create
conda env create --name <env-name> -f environment.yaml
```

Otherwise, if you want to create them automatically you can run the script **build_envs.sh** in **<project-name>/envs**

```
bash
cd <project-name>/envs
chmod +x build_envs.sh
./build_envs.sh
```

### Ontologies used and knowledge graph associated

The SOSA and SSN ontologies are used to represent how the data is stored in the graph as well as the way to
navigate in the graph and perform queries. 

Those ontologies are reused in the knowledge graph structure to represent the way the data are generated, 
and what is the informations associated with the ABRomics data. 

--> insert a picture of the knowledge graph here

### Methods to create the ABRomics KG from ABRomics report data

The data contained in ABRomics reports come from different analysis workflows. These reports are stored in 
the relational database and can be accessed with the API of ABRomics. 

Using admin credentials, all the reports can be extreacted and the data can then be stored in the knowledge 
graph. The script is able to retrieve reports from the ABRomics API and create a graph in ttl format 
accordingly. This step should be done when creating the graph from scratch and should not be done when the 
goal is to update the graph with small bits of fresh data from the relational database. 

To create the graph from scratch: 

1. Call the graph creator

```
bash

```
