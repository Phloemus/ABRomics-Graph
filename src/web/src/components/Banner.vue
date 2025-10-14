<script setup>
    import { XMarkIcon } from '@heroicons/vue/24/solid'

    // replace by the false by true to display the banner by default instead of not showing the 
    // banner. The goal of the banner is to display relevant info like an outage, some sort of maintenance
    // or a event that is being annonced
    const isBannerDisplayed = useState('isBannerDisplayed', () => false)

    function toggleBanner() {
        isBannerDisplayed.value = !isBannerDisplayed.value
    }

</script>

<template>
    <div v-show="isBannerDisplayed" class="w-full h-14 flex justify-center items-center bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
        <div class="flex gap-4">
            <p class="text-xl text-white font-semibold">
                Get yourself a seat at the 3rd Microbiograph consortium ! 
                <NuxtLink class="hover:underline" to="events/consortium-3">Get my ticket</NuxtLink>
                - <NuxtLink class="hover:underline" to="events/consortium-3/program">The program</NuxtLink>
            </p>
            <XMarkIcon class="w-8 h-8 text-slate-700 cursor-pointer" @click="toggleBanner" />
        </div>
    </div>
</template>
