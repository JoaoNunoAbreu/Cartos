<template>
  <div class="home">
      <Navbar/>
      <!-- cena da imagem -->
      <PopupCartos />
      
      <div class="text-center"> 
        <!-- Para ficar igual ao login -->
        <h2 class="change-font black--text"> {{ $t('nav.tituloProjeto') }}</h2>  
        <h5 class="change-font black--text"> {{ $t('nav.sistemaPesquisa') }} </h5>
      </div>
      
      <!-- Só para afastar 2 centrimetro o titulo da pesquisa -->
       <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>
              </v-row>
            </v-col>
          </v-row>
       </v-container>


        <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>
              </v-row>
            </v-col>
          </v-row>
       </v-container>
        
      <!-- end -->

    <v-container>
      <div id="imprimeMain" class="text-center">
        <v-row>
          <v-col col="12">
            <div class="results" >

              <h3 class="font-weight-light change-font">
                {{ $t("nav.ResultadosAnalise") }}
              </h3>

              <h3 class="font-weight-light change-font">
                {{ $t("nav.resultadoPara") }}
                <span class="font-weight-black change-font">{{
                  this.pesquisa
                }}</span>
              </h3>

              <h3 class="font-weight-light change-font">
                {{ $t("nav.Parametros") }}
                <span class="font-weight-black change-font"
                  >{{ this.$route.params.selectedElemento }},
                  {{ this.$route.params.tipo }},
                  {{ this.$route.params.versao }},
                  {{ this.$route.params.resultado }}</span
                >
              </h3>

              <h5 class="change-font blue--text text--darken-4">
                {{ this.numResultados }} {{ $t("nav.resultadosEm") }}
                {{ this.tempoFinal }} {{ $t("nav.milisegundos") }}
              </h5>

              <v-container fluid>
                <v-row>
                  <v-row align="start" justify="end">
                    <v-col cols="12" md="1">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                          <v-btn
                            depressed
                            block
                            color="#29b89b"
                            class="white--text change-font"
                            @click="goHome"
                            v-on="on"
                          >
                            <v-icon>mdi-magnify</v-icon>
                          </v-btn>
                        </template>
                        <span>{{ $t("nav.buttonPesquisa") }}</span>
                      </v-tooltip>
                    </v-col>

                    <!-- Botão de ajuda -->
                    <v-col cols="12" md="1">
                      <v-dialog
                        @keydown.esc="dialog = false"
                        v-model="dialog"
                        scrollable
                        width="500"
                      >
                        <template #activator="{ on: dialog }">
                          <v-tooltip bottom>
                            <template #activator="{ on: tooltip }">
                              <v-btn
                                depressed
                                block
                                color="#327ab7"
                                class="white--text change-font"
                                v-on="{ ...tooltip, ...dialog }"
                                ><v-icon>mdi-information</v-icon>
                              </v-btn>
                            </template>
                            <span>{{ $t("nav.buttonAjuda") }}</span>
                          </v-tooltip>
                        </template>

                        <v-card>
                          <v-card-title class="headline change-font">{{
                            $t("nav.buttonAjuda")
                          }}</v-card-title>

                          <v-divider class="mx-4" horizontal></v-divider>

                          <v-card-text
                            class="change-font"
                            style="white-space: pre-line"
                            >{{ $t("nav.textoInstrucoes") }}</v-card-text
                          >
                          <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-tooltip bottom>
                              <template v-slot:activator="{ on }">
                                <v-btn
                                  depressed
                                  color="#26B99A"
                                  class="white--text mr-3"
                                  @click="dialog = false"
                                  v-on="on"
                                >
                                  <v-icon>mdi-door-open</v-icon>
                                </v-btn>
                              </template>
                              <span>{{ $t("nav.Sair") }}</span>
                            </v-tooltip>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </v-col>

                    <!-- Botão de imprimir -->
                    <v-col cols="12" md="1">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                          <v-btn
                            depressed
                            block
                            color="#29b89b"
                            class="white--text change-font"
                            @click="printSection"
                            v-on="on"
                          >
                            <v-icon>mdi-printer</v-icon>
                          </v-btn>
                        </template>
                        <span>{{ $t("nav.imprimir") }}</span>
                      </v-tooltip>
                    </v-col>

                    <!-- Para ficar em cima do painel -->
                    <v-col cols="12" md="1"> </v-col>
                  </v-row>
                </v-row>
              </v-container>
            </div>

            <!-- ...............Visualização dos Resultados.................. -->

            <v-card
              text
              class="pa-15 change-font; text-left ; mx-auto"
              max-width="600"
            >
              <div v-for="(item, index) in pageOfItems" v-bind:key="index">
                <h3 class="font-weight-black change-font">
                  <a class="change-font" @click="showElemento(index)">{{
                    item.id
                  }}</a>
                </h3>

                <p><b>Título:</b> {{ item.titulo }}</p>
                <p>{{ item.data_publicacao }}</p>
                <br />
              </div>

              <!-- Pagination -->
              <div class="card-footer text-center change-font">
                <jw-pagination
                  :items="resultados"
                  @changePage="onChangePage">
                </jw-pagination>
              </div>
            </v-card>
          </v-col>
        </v-row>
        <!-- tem de estar persistent para fazer clean do array conta -->
      </div>
      <v-dialog persistent v-model="dialogElemento" max-width="800px">
            <verElemento
              :passedData="elementoAtual"
              backTo="/resultados"
              :isDisabled="true"
              :isDeleting="false"
              @emiteFecho="emiteFecho($event)"
            ></verElemento>
      </v-dialog>
    </v-container>
    <Footer />
  </div>
</template>

<script>
import VerElemento from "../components/verElemento.vue";
import axios from "axios";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import PopupCartos from '../components/PopupCartos'

export default {
  data() {
    return {
      url: process.env.VUE_APP_URL,
      pesquisa: null,
      page: 1,
      resultados: [],
      dialog: false,
      dialogElemento: false,
      elementoAtual: null,
      textoAtual: null,
      pageOfItems: [],
      conta: [],
      tempoFinal: 0,
      numResultados: 0,
    };
  },
  components: {
    Navbar,
    Footer,
    PopupCartos,
    VerElemento,
  },
  created() {
    var tempo_inic = performance.now();

    this.pesquisa = this.$route.params.pesquisa;
    axios
      .get(this.url + `/analise/pesquisa?nome=${this.$store.state.user._id}`, { params: this.$route.params })
      .then((dados) => {
        var tempo_fin = performance.now();
        this.tempoFinal = tempo_fin - tempo_inic;
        this.numResultados = dados.data.length;

        for (let i = 0; i < dados.data.length; i++)
          this.resultados.push(dados.data[i]);
        
      })
      .catch((err) => {
        console.log(err.message);
        this.error = err.message;
      });
  },

  methods: {
    goHome() {
      this.$router.push({
        name: "home",
      });
    },
    onChangePage(pageOfItems) {
      // update page of items
      this.pageOfItems = pageOfItems;
    },
    printSection() {
      // Pass the element id here
      this.$htmlToPaper("imprimeMain");
    },
    showElemento(index) {
      this.elementoAtual = this.resultados[index];
      this.dialogElemento = true;
    },
    emiteFecho: function () {
      this.dialogElemento = false;
    },
  },
};
</script> 

<style scoped>
.keep-spaces {
  white-space: pre-wrap;
}
@media print {
  body {
    overflow: auto;
    height: auto;
  }
  .page-break {
    display: block;
    page-break-before: always;
  }
}

.col-md-1 {
  margin: 10px;
  max-width: 53px;
}

.v-application p {
  margin-bottom: 1px;
}
</style>

<style lang="stylus" scoped>
.change-font {
  font-family: 'Arial';
}
</style>

