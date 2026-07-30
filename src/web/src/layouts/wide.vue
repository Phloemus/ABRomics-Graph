<script setup>

    import Banner from "../components/Banner.vue"
    import Sidebar from "../components/Sidebar.vue"
    import Navbar from "../components/Navbar.vue"


</script>


<template>
    <div class="min-h-screen">
        <Banner />
        <div class="w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
        <div class="w-full bg-slate-50 flex">
            <Sidebar />
            <div class="w-full">
                <Navbar />
                <div class="px-2 py-10">
                    <slot />
                </div>
            </div>
        </div>
    </div>
</template>