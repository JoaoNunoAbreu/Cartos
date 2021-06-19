<template>

    <div class="home">
      <Navbar/>
      <!-- cena da imagem -->
      <PopupCartos />
      
      <div class="text-center"> 
        <!-- Para ficar igual ao login -->
        <h2 class="change-font black--text"> {{ $t('nav.tituloProjeto') }}</h2>  
        <h5 class="change-font black--text mt-5"> {{ $t('nav.sistemaPesquisa') }} </h5>
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


      <v-container style="padding:0">
        <v-form ref="form" lazy-validation>
        
        <v-container fluid>
            <v-row>
              <v-col cols="12">
                <v-row
                  align="start"
                  justify="center"
                >
            <v-col cols="12" md="2"> </v-col>

            <v-col cols="12" md="6"> 
              <v-combobox
                outlined
                dense 
                class="change-font"
                clearable  
                :items="pesquisas"
                v-bind:label="$t('nav.barraPesquisa')"
                v-model="pesquisa" 
                hide-no-data
                :rules="rulesRequired($t('nav.pesquisaNaoVazia'))"
                required
              > 
              </v-combobox>          
            </v-col>

            <v-col cols="12" md="1">
              
              <v-tooltip bottom> 
                <template v-slot:activator="{ on }">
                <v-btn width=20 depressed block color="#29b89b" class="white--text change-font" @click="pesquisar" v-on="on">
                  <v-icon>mdi-magnify</v-icon>
                </v-btn>
                </template>
                <span>{{ $t('nav.buttonPesquisa') }}</span>
              </v-tooltip>
           
            </v-col> 
            <div>
            <!-- Botão de ajuda -->
            <v-col cols="12" md="1">
              <v-dialog @keydown.esc="dialog = false" v-model="dialog" scrollable width="500">
                 <template #activator="{ on: dialog }">
                  
                    <v-tooltip bottom>
                      <template #activator="{ on: tooltip }">
                        <v-btn width=43 depressed block color="#327ab7" class="white--text change-font" v-on="{ ...tooltip, ...dialog }"><v-icon>mdi-information</v-icon> </v-btn>
                      </template>
                      <span>{{$t('nav.buttonAjuda')}}</span>
                    </v-tooltip>
                
                </template>  
                
                <v-card>
                    <v-card-title class="headline change-font">{{ $t('nav.buttonAjuda') }}</v-card-title>

                     <v-divider
                      class="mx-4"
                      horizontal
                     ></v-divider>

                    <v-card-text class="change-font" style="white-space: pre-line"
                        >{{ $t('nav.textoInstrucoes') }}</v-card-text
                      >
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
            </v-col>
            </div>
                  
            <v-col cols="12" md="2"> </v-col>

              </v-row>
            </v-col>
          </v-row>
        </v-container>

        <!-- Filtros -->
            
          <v-container fluid>
            <v-row align="start" justify="center">
              <v-col cols="12" md="3"> 
                <v-select
                  class="change-font"
                  required
                  v-model="colecao"
                  :items="colecaoSel"
                  v-bind:label="$t('p1.col')">
                </v-select>
              </v-col>
            </v-row>
            <v-row align="start" justify="center">
              <v-col cols="12" md="3"> 
                <v-select
                  class="change-font"
                  required
                  v-model="editora"
                  :items="editoraSel"
                  v-bind:label="$t('p1.edi')"
                ></v-select>
              </v-col>
            </v-row>
            <v-row align="start" justify="center" class="mb-3 mt-n1">
              <v-col cols="12" md="3"> 
                <v-menu
                  ref="menu"
                  v-model="menu"
                  :close-on-content-click="false"
                  :return-value.sync="date"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="date"
                      label="Picker in menu"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="date"
                    no-title
                    scrollable
                  >
                    <v-spacer></v-spacer>
                    <v-btn
                      text
                      color="primary"
                      @click="menu = false"
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      text
                      color="primary"
                      @click="$refs.menu.save(date)"
                    >
                      OK
                    </v-btn>
                  </v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-container> 

            <!-- o v-bind:label, tive de fazer assim para conseguir traduzir o interior do campo -->
            <!--  <v-btn @click="reset">clear</v-btn> /-->
        </v-form>
      </v-container>
      <Footer class="footer" />
    </div>
</template>

<script>
import axios from "axios"; 
import Navbar from '../components/Navbar';
import PopupCartos from '../components/PopupCartos'
import Footer from '../components/Footer'

export default {
  name: "Home",
  components: { PopupCartos, Navbar, Footer },
  data() {
    return {
      pesquisa: "", 
      dialog: false,
      colecao: "Todas",
      colecaoSel: [],
      editora: "Todas", 
      editoraSel: [],
      menu: false,
      date: null,
      pesquisas:[],
      url: process.env.VUE_APP_URL,
    };
  }, 

  created() {
      axios.get(this.url+`/elementos/editoras`,
        {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        }
      )
      .then((response) => {
        for (let i = 0; i < response.data.length; i++)
          this.editoraSel.push(response.data[i].x.designacao)
        this.editoraSel.push("Todas")
      })
      .catch((e) => {
        //console.log(e)
        this.errors.push(e);
      }),
      axios.get(this.url+`/elementos/colecoes`,
        {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        }
      )
      .then((response) => {
        for (let i = 0; i < response.data.length; i++)
          this.colecaoSel.push(response.data[i].x.designacao)

        this.colecaoSel.push("Todas")
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
  
  methods: { 
    
    pesquisar() {
      
      let params = {
                pesquisa: this.pesquisa,
                colecao: this.colecao, 
                editora: this.editora,
                date: this.date
            }
      this.$router.push({
            name: 'resultados',
            params: params,
            
        });      
    }, 
    reset() {
      this.$refs.form.reset();
    }, 
     
    // função auxiliar que permite a tradução da obrigatoriedade dos campos
    rulesRequired(role) {
      return [value => !!value || role];
    }, 
    
    rulePalavras(role){ 
      if(this.resultado == "npalavras"){ return  [v => v > 0 || role];}
    }
    }  
};
</script>

<style lang="stylus" scoped>
.change-font {
    font-family: "Arial"; 
}
</style> 

<!-- Este CSS muda globalmente o tamanho da fonte da letra -->
<style>
.v-input .v-label {
    font-size: 0.9em;
}
</style>

<!-- CSS para questões de paddings, etc -->

<style scoped> 

.container{ 
  padding: 0px;
} 
.col-xl, .col-xl-auto, .col-xl-12, .col-xl-11, .col-xl-10, .col-xl-9, .col-xl-8, .col-xl-7, .col-xl-6, .col-xl-5, .col-xl-4, .col-xl-3, .col-xl-2, .col-xl-1, .col-lg, .col-lg-auto, .col-lg-12, .col-lg-11, .col-lg-10, .col-lg-9, .col-lg-8, .col-lg-7, .col-lg-6, .col-lg-5, .col-lg-4, .col-lg-3, .col-lg-2, .col-lg-1, .col-md, .col-md-auto, .col-md-12, .col-md-11, .col-md-10, .col-md-9, .col-md-8, .col-md-7, .col-md-6, .col-md-5, .col-md-4, .col-md-3, .col-md-2, .col-md-1, .col-sm, .col-sm-auto, .col-sm-12, .col-sm-11, .col-sm-10, .col-sm-9, .col-sm-8, .col-sm-7, .col-sm-6, .col-sm-5, .col-sm-4, .col-sm-3, .col-sm-2, .col-sm-1, .col, .col-auto, .col-12, .col-11, .col-10, .col-9, .col-8, .col-7, .col-6, .col-5, .col-4, .col-3, .col-2, .col-1{ 
  padding: 5px;
} 

.col-md-1 { 
  max-width: 53px;
}
.footer {
  width: 100%;
  height: 40px;
  position: absolute;
  bottom: 25px;
  left: 0;
}
</style>