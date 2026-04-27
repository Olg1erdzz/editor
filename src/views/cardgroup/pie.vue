<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'
import * as chartConfig from './chartConfig.js'
ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  name: 'App',
  components: {
    Pie
  },
  props: {
    chartData: {
      type: Object as () => ChartData<"line", (number | Point | null)[], unknown>,
      required: true
    }
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
</script>
