const { createApp, ref } = Vue

createApp({
    data() {
        return {
            message: "Hello world"
        }
    },
    delimiters: ['[[', ']]'],
}).mount('#app')