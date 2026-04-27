<template>
  <div class="container">
    <Bar v-if="loaded" :data="chartData" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  props: {
    chartData: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    loaded: false
  }),
  async mounted () {
    this.loaded = false

    try {
      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  }
}
</script>