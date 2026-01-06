<script setup>

    import { useRoute } from 'vue-router'

    import ActionButton from "../../components/ActionButton.vue"
    import Table from "../../components/Table.vue"

    import { onMounted, ref } from 'vue'
    import { init } from 'modern-monaco'
    import { createHighlighter } from 'shiki'
    import { shikiToMonaco } from '@shikijs/monaco'

    const config = useRuntimeConfig()
    
    const editor = ref(null)
    let monacoInstance = null
    let editorInstance = null

    var queryResponse = ref([])
    var isQueryPerformed = ref(false)
    var isQueryError = ref(false)
    var queryError = ref("")

    onMounted(async () => {
        monacoInstance = await init()

        const highlighter = await createHighlighter({
          themes: ['vitesse-dark', 'catppuccin-mocha'],
          langs: ['sparql']
        })

        shikiToMonaco(highlighter, monacoInstance)

        monacoInstance.editor.defineTheme('catppuccin-mocha', {
          base: 'vs-dark',
          inherit: true,
          rules: [],
          colors: {
            'editor.background': '#1e293b',
            'editor.selectionBackground': '#585b70',
            'editorCursor.foreground': '#f5e0dc'
          }
        })

        editorInstance = monacoInstance.editor.create(editor.value, {
          value: "SELECT (COUNT(*) AS ?count) WHERE {\n\t?s ?p ?o .\n}",
          language: 'javascript',
          theme: 'catppuccin-mocha',
          automaticLayout: true,
          minimap: { enabled: false },
          fontSize: 15
        })
    })

    function fetchQueryResult(id) {
        // Don't forget to change the port or the host in prod ;)
        const uri = encodeURI(config.public.graphServerUrl + "repositories/abromics-kg?query=" + editorInstance.getValue())
        fetch(uri,
            {
                method: "GET",
                headers: {
                    'Content-Type': 'application/sparql-query',
                    'Accept': 'application/sparql-results+json'
                }
            }
        ).then((response) => {
            console.log(response)
            if(response.status != 200) {
                isQueryError.value = true
                queryError.value = response.json()
                return
            } else {
                isQueryError.value = false
            }
            return response.json()
        }).then((data) => {
            queryResponse.value = data.results.bindings
            isQueryPerformed.value = true
            console.log(data)
        }).catch(err => {
            console.error("Error while processing response: ", err)
            isQueryError.value = true
            queryError.value = err
        })
    }

</script>

<template>
    <div class="flex justify-between items-start">
                <div class="w-full">
                    <h2 class="text-xl text-slate-900 font-bold">Query</h2>
                    <div class="my-4 w-full bg-slate-800 rounded-md">
                        <div class="py-2 px-4 flex items-center justify-between border-b border-slate-700">
                            <span class="text-white">sparql</span>
                            <div class="flex items-center gap-2">
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                                <div class="h-4 w-4 rounded-full bg-slate-700"></div>
                            </div>
                        </div>
                        <div class="py-4 w-full bg-slate-800 rounded-b-md">
                            <code class="w-full h-full relative">
                                <div ref="editor" class="w-full min-h-80"></div>
                            </code>
                        </div>
                    </div>
                </div>
                <div>
            </div>
    </div>
    <div class="w-full flex gap-4">
        <ActionButton
            content="Execute query"
            @click="fetchQueryResult"
        >
        </ActionButton>
        <div v-if="isQueryError" class="py-2 px-4 bg-red-200 text-red-500 rounded-md">
            Error: {{ queryError }}
        </div>
    </div>
    <div v-if="isQueryPerformed" class="my-6">
        <div class="flex justify-between items-center">
            <h2 class="text-xl text-slate-900 font-bold">Query result</h2>
        </div>
        <Table :data="queryResponse"/>
    </div>
</template>
