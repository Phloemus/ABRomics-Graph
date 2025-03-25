<script setup>


</script>

<template>
    <div v-show="true" class="w-full h-full">
        <div class=" w-full h-full fixed top-0 left-0 bg-opacity-70 bg-slate-800 z-20">
            <div class="mx-auto my-14 p-4 bg-white rounded-md max-w-screen-sm">
                <h2 class="text-slate-900 text-2xl font-bold flex justify-center">Login</h2>
                <div class="my-10 px-4 w-full">
                    <div class="w-full">
                        <h3 class="text-lg text-slate-900">Username</h3>
                        <div class="my-2">
                            <input 
                                class="w-full px-3 py-1 bg-slate-200 placeholder:italic placeholder:text-slate-400 border focus:outline-none focus:ring-1 focus:ring-slate-900 focus:border-slate-900 focus:bg-white text-slate-800 rounded-sm"
                                placeholder="username"
                                value=""
                                name="username"
                            />
                        </div>
                    </div>
                    <div class="w-full">
                        <h3 class="text-lg text-slate-900">Password</h3>
                        <div class="my-2">
                            <input 
                                class="w-full px-3 py-1 bg-slate-200 placeholder:italic placeholder:text-slate-400 border focus:outline-none focus:ring-1 focus:ring-slate-900 focus:border-slate-900 focus:bg-white text-slate-800 rounded-sm"
                                type="password"
                                placeholder="password"
                                value=""
                                name="password"
                            />
                        </div>
                    </div>

                </div>
                <div class="pr-4 flex justify-end">
                    <ActionButton content="Login" />
                </div>
            </div>
        </div>
    </div>
</template>
