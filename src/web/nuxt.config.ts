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
        sparqlEnpoint: "http://localhost:7200/repositories/abromics-kg"
    }
  }
})
