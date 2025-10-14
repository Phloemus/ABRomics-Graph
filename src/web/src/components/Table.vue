<script setup>

    const props = defineProps({
        data: Array,
    })
    console.log(props.data)

    const columns = Object.keys(props.data[0])
    console.log(columns)

</script>


<template>

        <table class="my-4 w-full">
            <tbody class="w-full bg-slate-50 border border-slate-100 rounded-md">
                <tr class="bg-white border border-slate-100 font-medium text-slate-900 text-lg rounded-t-md">
                    <th v-for="(key, index) in columns" class="p-2 border border-slate-100">{{ key }}</th>
                </tr>
                <tr v-for="(row, index) in data">
                    <td v-for="(value, index) in row" class="p-2 border border-slate-100">{{ value.value }}</td>
                </tr>
            </tbody>
        </table>

</template>
