<template>
      <v-card>
        <v-toolbar color="#2A3F54" dark>
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
              <h3>{{ $t("fol.imp") }}</h3>
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
    return {}
  },
  methods: {
        emiteFecho(){
            this.$emit('emiteFecho')
            }
    },
}
</script>

<style scoped>

</style>

