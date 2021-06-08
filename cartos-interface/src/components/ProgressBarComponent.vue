<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <p>Aguarde o processamento dos Elementos</p>
      <v-col cols="12">
        <div style="min-height: 500px;">
          <v-progress-linear indeterminate color="blue darken-2" ></v-progress-linear>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from 'axios'
export default {
  data(){
    return{
      url: process.env.VUE_APP_URL,
    }
  },
  mounted: async function () {
    try {
      var response = await axios.get(this.url + '/process', {headers: { 'Authorization': `Bearer: ${this.$store.state.jwt}`}})
      if(response.data.message){
        this.$router.push('/localidades')
      }
    } catch (e) {
      return e
    }
  }
}
</script>
