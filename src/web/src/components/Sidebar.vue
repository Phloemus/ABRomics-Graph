<template>
    <div class="px-4 w-96 h-full bg-white border-r border-slate-200 z-20">
            <div>

            </div>
            <div class="w-full relative">
                <h3 class="mx-1 my-4 text-slate-600 text-lg">Queries</h3>
                <div class="my-3 p-2 w-full bg-slate-50 rounded-md hover:bg-slate-100 hover:cursor-pointer">
                    <NuxtLink 
                        to="/about"
                    >
                        <h4 class="text-slate-800 text-md">
                            <span class="font-medium text-slate-900">Competency Question 1:</span> 
                            What are the most common antibiotic resistance genes present in all samples
                        </h4>
                    </NuxtLink>
                </div>
                <div class="my-3 p-2 w-full bg-slate-50 rounded-md hover:bg-slate-100 hover:cursor-pointer">
                    <NuxtLink 
                        to="/about"
                    >
                        <h4 class="text-slate-800 text-md">
                            <span class="font-medium text-slate-900">Competency Question 1:</span> 
                            What are the most common antibiotic resistance genes present in all samples
                        </h4>
                    </NuxtLink>
                </div>
                <div class="flex justify-center">
                    <ActionButton content="More queries"></ActionButton>
                </div>
            </div>
            <div class="mx-12 px-6 pb-4 absolute bottom-0 left-0 border-t-2 border-slate-200">
                <div class="py-3 flex gap-2 text-slate-500">
                    <span>v0.0.1</span>
                    <span>ABRomicsKG</span>
                    <span>2025</span>
                </div>
            </div>
        </div>
</template>
