// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  srcDir: "src",
  pages: true,
  ssr: true,
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss", "@nuxt/icon", "nuxt-shiki"],
  shiki: {
    bundleThemes: ["ayu-dark"]
  },
  runtimeConfig: {
    public: {
        appName: "ABRomicsKG",
        graphServerUrl: typeof process.env.NUXT_PUBLIC_GRAPH_SERVER_HOST === "undefined" ? "http://localhost:7200/" : process.env.NUXT_PUBLIC_GRAPH_SERVER_HOST,
        apiUrl: typeof process.env.NUXT_PUBLIC_API_HOST === "undefined" ? "http://localhost:5000/graph-api/" : "http://" + process.env.NUXT_PUBLIC_API_HOST + ":5000/" + process.env.NUXT_PUBLIC_API_HOST + "/"
    }
  }
})
