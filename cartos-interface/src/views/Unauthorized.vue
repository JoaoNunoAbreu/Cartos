<template>
  <div class="NotFound" >
    <nav>
        <v-toolbar flat style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%)">
        </v-toolbar>
    </nav>
    <PopupCartos />
    <v-container>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card height="400" color="transparent" flat>
            <div class="display-3 mt-5">(401) Not Enough Permissions.</div>
            <div class="paragraph-text mt-2">
              <br />
              <br />
              <a href="/">Home</a>
              <a class="ml-7" href="/login">Login</a>
            </div>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import PopupCartos from '../components/PopupCartos'
export default {
  components: { PopupCartos}
}
</script>

<style>
  .paragraph-text {
    font-size: 18px;
  }
  .NotFound {
    text-align: center;
  }
</style>
