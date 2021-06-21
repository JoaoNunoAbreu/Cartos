<template>
  <nav>
    <v-toolbar flat style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);">
      <v-spacer></v-spacer>
      <v-btn
        dark
        color="#29b89b"
        to="/login"
      >
        Log In
      </v-btn>

      <v-btn
        dark
        class="mr-10 ml-3"
        color= "#2C6FAE"
        to="/registo"
      >
        {{ $t('nav.registo') }}
      </v-btn>

      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font" v-bind:class="{active: activeBtn === 'btn1' }" @click="setLocale('pt'); activeBtn = 'btn1'" v-on="on">PT</v-btn>
        </template>
        <span>{{ $t('nav.LinguaPT') }}</span>
      </v-tooltip>

      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font" v-bind:class="{active: activeBtn === 'btn2' }" @click="setLocale('es'); activeBtn = 'btn2'" v-on="on">ES</v-btn>
        </template>
        <span>{{ $t('nav.LinguaES') }}</span>
      </v-tooltip>
      
      <v-tooltip bottom> 
        <template v-slot:activator="{ on }">
        <v-btn text small class="white--text change-font"  v-bind:class="{active: activeBtn === 'btn3' }" @click="setLocale('en'); activeBtn = 'btn3'" v-on="on">UK</v-btn>
        </template>
        <span>{{ $t('nav.LinguaEN') }}</span>
      </v-tooltip>

    </v-toolbar>
  </nav>
</template>

<script>

export default {
  components: {},
  data() {
    return {
      closeOnContentClick: true, 
      filterBtnTTip: false,  
      activeBtn: 'btn1'
    };
  }, 
  methods:{ 
    setLocale(locale){ 
      this.$i18n.locale = locale
      this.$router.push({
        params: { lang: locale }
      })
    }
  } 
};
</script>

<style>
.flag:hover {
  cursor: pointer;
} 
.active{
  background-color:#29b89b;
}
</style>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style>