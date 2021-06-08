<template>
  <v-app>
    <v-main>      
      <router-view></router-view>
      <!--<appFooter></appFooter>-->
    </v-main>
  </v-app>
</template>

<script>
//import Footer from './components/Footer.vue'
export default {
  name: 'App',

  /*components: {
    'appFooter':Footer
  },*/

  data: () => ({
    //
  }),
};
</script>

<style scoped>

</style>
