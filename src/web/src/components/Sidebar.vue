<script setup>

    import SmallCard from '../components/SmallCard.vue'
    import queries from '../static/queries.json'

    const config = useRuntimeConfig();
    const appName = config.public.appName

    const isUserLoggedIn = useState("isUserLoggedIn")

</script>

<template>
    <div class="px-4 w-96 h-screen block bg-white border-r border-slate-200 z-10">
            <div class="w-full h-1 lg:hidden bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
            <div>
                <div class="my-4 flex justify-between w-full items-center">
                    <div>
                        <h2 class="text-slate-800 text-lg">{{ appName }}</h2>
                        <p class="my-0.5 text-slate-600 text-sm">Linking microbiome data</p>
                    </div>
                    <div 
                        class="w-8 h-10 rounded-md cursor-pointer flex items-center"
                        @click="toggleSidebar"
                    >
                        <img src="assets/cross-icon.svg">
                    </div>
                </div>
                <div class="my-10 mb-2 w-full relative">
                    <h3 class="mx-1 my-4 text-slate-600 text-lg">Dashboard</h3>
                    <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                        <NuxtLink to="/" class="flex gap-2" @click="toggleSidebar">
                            <p>
                                Main dashboard
                            </p>
                            <div class="h-2 w-2 bg-green-400 rounded-full"></div>
                        </NuxtLink>
                    </div>
                </div>
                <div class="my-10 w-full relative">
                    <h3 class="mx-1 my-4 text-slate-600 text-lg">Quick actions</h3>
                    <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                        <NuxtLink to="/sparql" @click="toggleSidebar">
                            <p>
                                Perform a query
                            </p>
                        </NuxtLink>
                    </div>
                    <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                        <NuxtLink to="/map" @click="toggleSidebar">
                            <p>
                                Map exploration
                            </p>
                        </NuxtLink>
                    </div>
                    <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                        <NuxtLink to="/submit" @click="toggleSidebar">
                            <p>
                                Submit my data
                            </p>
                        </NuxtLink>
                    </div>
                    <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                        <NuxtLink to="/integration" @click="toggleSidebar">
                            <p>
                                Integrate AbromicsKG
                            </p>
                        </NuxtLink>
                    </div>
                </div>
            </div>
            <div>

            </div>
            <div class="w-full relative">
                <h3 class="mx-1 my-4 text-slate-600 text-lg">Prewritten queries</h3>
                <SmallCard 
                    v-for="(query, index) in queries"
                    :title="query.name"
                    :description="query.title"
                    :link="query.link"
                />
                <div class="flex justify-center">
                    <ActionButton content="More queries"></ActionButton>
                </div>
            </div>
            <div v-show="isUserLoggedIn" class="w-full relative">
                <h3 class="mx-1 my-4 text-slate-600 text-lg">Admin actions</h3>
                <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                    <NuxtLink to="/admin/delete-all">
                        <p>
                            delete all graph nodes
                        </p>
                    </NuxtLink>
                </div>
                <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                    <NuxtLink to="/admin/recreate-graph">
                        <p>
                            recreate graph
                        </p>
                    </NuxtLink>
                </div>
                <div class="my-2 p-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-md hover:cursor-pointer">
                    <p>
                        delete graph content
                    </p>
                </div>
            </div>
            <div class="mx-12 px-6 pb-4 absolute bottom-0 left-0 border-t-2 border-slate-200">
                <div class="py-3 flex gap-2 text-slate-500">
                    <span>v0.0.2</span>
                    <span>ABRomicsKG</span>
                    <span>2025</span>
                </div>
            </div>
        </div>
</template>
