export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    result: null,
  }),
  actions: {
    setResult(data) {
      this.result = data
    },
  },
})
