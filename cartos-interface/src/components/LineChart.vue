<script>
  import { Line } from 'vue-chartjs'

  export default {
    extends: Line,
    props: {
      passedData: {
        type: Object,
      }
    },
    data () {
      return {
        chartData: {
          labels: [],
          datasets: [
            {
              label: 'Line Chart',
              data: [],
              fill: false,
              borderColor: '#376a53',
              backgroundColor: '#376a53',
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }],
            xAxes: [ {
              gridLines: {
                display: false
              }
            }]
          },
          legend: {
            display: true
          },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    mounted () {
      this.onUpdate()
    },
    methods: {
      onUpdate() {
        this.chartData.labels = [...Object.keys(this.passedData)];
        this.chartData.datasets[0].data = [...Object.values(this.passedData)];
        this.renderChart(this.chartData, this.options)
      }
    },
    watch: {
      passedData: {
        handler() {
          this.onUpdate()
        }
      },
    }
  }
</script>