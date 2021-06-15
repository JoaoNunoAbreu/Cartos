<template>
      <v-card>
        <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
          <h2>{{ $t("fol.info") }}</h2>
        </v-toolbar>
        <v-row>
          <v-col
            style="
              margin-left: 1cm;
              margin-right: 1cm;
              max-width: 40px;
              margin-top: 20px;
            "
          >
            <v-icon x-large color="#003399" dark>mdi-information</v-icon>
          </v-col>
          <v-col style="margin-top: 20px;">
            <v-card-text>
              <h3>{{ $t("navd.textoImportCSV") }}</h3>
              <h3> {{nSucesso}} {{ $t("navd.sucessoCSV") }}</h3>
              <h3> {{nInsucesso}}{{ $t("navd.insucessoCSV") }}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="emiteFecho" v-on="{ ...tooltip }" color="#26B99A"
                      class="white--text mr-3"  >
                <v-icon>mdi-door-open</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("navd.leave") }}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
</template>

<script>
export default {
  data() {
    return {
    }
  },
  props: {
    nSucesso: {
      type: Number,
    },
    nInsucesso: {
      type: Number,
    },
  },
  watch: {
    nSucesso: {
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    },
    nInsucesso:{
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    }
  },
  methods: {
    emiteFecho(){
      this.$emit('emiteFecho')
    },
    onUpdate() {
    }
    },
}
</script>

<style scoped>

</style>

