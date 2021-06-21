<template>
  <div class="text-center">
    <v-dialog @keydown.esc="dialog = false"  v-model="dialog" scrollable width="500">
      <template v-slot:activator="{ on }">
        <v-btn depressed text class="grey--text change-font text-none" v-on="on">
          <span>{{ $t('nav.creditos') }}</span>
        </v-btn>
      </template>
      <v-card>
        <v-card-text class="change-font mt-6" style="white-space: pre-line">
                  <h2> {{ $t('nav.textoCreditos') }} </h2>
                  <p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/Catarinacg16" target="blank_">Catarina Gil</a><p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/goncalo-f" target="blank_">Gonçalo Ferreira</a><p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/JoaoNunoAbreu" target="blank_">João Nuno Abreu</a>

                </v-card-text>
           <v-card-actions>
          <v-spacer></v-spacer>
           
           <v-tooltip bottom> 
            <template v-slot:activator="{ on }">
                <v-btn depressed color="#26B99A" class="white--text mr-3" @click="dialog=false" v-on="on">
                  <v-icon>mdi-door-open</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('nav.Sair') }}</span>
            </v-tooltip>

        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false
    };
  }
};
</script> 

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial";
}
</style>
