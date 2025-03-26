<script setup>

    // Global state
    const userAuthToken = useState('userAuthToken')

    function executeQuery() {
        
        fetch(
            "http://localhost:5000/graph-api/protected", 
            { 
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({token: userAuthToken.value})
            }
        )
        .then(response => { 
            return response.json() // handle the case in which the token has expired
        }).then((data) => {
            console.log(data)
        }).catch(err => {
            console.error("Error fetching data: ", err)
        })
    }

</script>

<template>
    <div class="flex justify-between items-start">
        <div>
            <h1 class="mb-1 text-2xl text-slate-900 font-bold">Test API admin route</h1>
            <span class="text-md text-slate-600">admin query</span>
        </div>
        <div class="px-4 py-1 bg-sky-200 text-sky-500 rounded-sm">
            <NuxtLink to="http://localhost:5000/graph-api/protected">[POST] /protected</NuxtLink>
        </div>
    </div>
    <div class="mt-4">
        <ActionButton content="Execute query" @click="executeQuery"/>
    </div>
</template>

