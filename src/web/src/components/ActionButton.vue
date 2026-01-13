<script setup>
    const props = defineProps({
        content: {
            default: ""
        }, 
        isLoading: {
            default: false
        }
    })
</script>

<template>
    <button class="px-8 py-2 bg-slate-900 hover:bg-slate-800 text-white text-md flex gap-4 items-center rounded-md">
        <span>{{ props.content }}</span>
        <div v-if="props.isLoading == true" class="w-5 h-5 relative">
            <div class="absolute top-0 left-0 w-full h-full border-2 border-slate-300 border-opacity-75 rounded-full"></div>
            <div class="absolute top-0 left-0 w-full h-full border-2 border-transparent border-t-white rounded-full animate-spin z-2"></div>
        </div>
    </button>
</template>
