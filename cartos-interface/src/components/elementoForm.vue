<template>
  <div id="registar">
      <v-card height="100%" width="100%">
        <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
          <h1>{{$t('fol.title')}}</h1>
        </v-toolbar>
        <v-card-title>
          <h3>{{$t('elemForm.visFol')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left"><b>{{$t('elemForm.id')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.id}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('elemForm.colecao')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.colecao}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('elemForm.editora')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.editora}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('elemForm.dataPub')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.dataPub}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('elemForm.lingua')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.lingua}}
                                    </v-layout>
                                </td>
                            </tr>
                        </tbody>
                      </template>
                  </v-simple-table>
                  <p></p>
                  <v-dialog persistent v-model="dialog1" scrollable max-width="800px">
                    <template v-slot:activator="{ on }">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-btn v-on="{...on, ...tooltip}" class="mr-10 ml-5"><v-icon>mdi-text-box-search</v-icon></v-btn>
                        </template>
                        <span>
                            {{$t('elemForm.tComTags')}}
                        </span>
                      </v-tooltip>
                    </template>
                    <v-card height="100%" width="100%">
                        <v-card-title>
                            <h1>{{$t('elemForm.tComTags')}}</h1>
                            <div class="spacer"></div>
                            <v-btn @click="dialog1 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                        </v-card-title>
                        <v-card-text required>
                          {{this.elemento.textoCTags}}         
                        </v-card-text>
                        <v-btn @click="dialog1 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                    </v-card>
                  </v-dialog>
                  <v-dialog persistent v-model="dialog2" scrollable max-width="800px" >
                      <template v-slot:activator="{ on }">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on: tooltip }">
                              <v-btn v-on="{...on, ...tooltip}"><v-icon>mdi-text-box</v-icon></v-btn>
                          </template>
                          <span>
                              {{$t('elemForm.tSemTags')}}
                          </span>
                        </v-tooltip>
                      </template>
                      <v-card height="100%" width="100%">
                          <v-card-title>
                              <h1>{{$t('elemForm.tSemTags')}}</h1>
                              <div class="spacer"></div>
                              <v-btn @click="dialog2 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                          </v-card-title>
                          <v-card-text required>
                            {{this.elemento.textoSTags}}         
                          </v-card-text>
                          <v-btn @click="dialog2 = false" color="#c9302c" class="white--text">{{$t('indForm.close')}}</v-btn>
                      </v-card>
                  </v-dialog>
              </v-container>
          </v-form>
          </v-card-actions>
          <v-toolbar flat>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
              </template>
              <span>
                  {{$t('indForm.close')}}
              </span>
            </v-tooltip>
          </v-toolbar>
      </v-card>
  </div>
</template>

<script>

export default {
  data(){
    return{
      elemento:{
        id: "",
        titulo: "",
        colecao: "",
        numero: "",
        serie: "",
        lingua: "",
        paginas: "",
        size: "",
        personagens: "",
        estado: "",
        editora: "",
        dataPub: "",
        ficheiro: null,
        tipo: "",
        capa: null,
      },
      dialog1:false,
      dialog2:false
    }
  },
  props:{
    passedData:{
      type:Object
    }
  },
  methods: {
    onUpdate(){
      this.elemento.id = this.passedData.id;
      this.elemento.titulo = this.passedData.titulo;
      this.elemento.colecao = this.passedData.colecao;
      this.elemento.numero = this.passedData.numero;
      this.elemento.serie = this.passedData.serie;
      this.elemento.lingua = this.passedData.lingua;
      this.elemento.paginas = this.passedData.paginas;
      this.elemento.size = this.passedData.size;
      this.elemento.personagens = this.passedData.personagens;
      this.elemento.estado = this.passedData.estado;
      this.elemento.editora = this.passedData.editora;
      this.elemento.dataPub = this.passedData.data_publicacao;
      this.elemento.ficheiro = this.passedData.ficheiro;
      this.elemento.tipo = this.passedData.tipo;
      this.elemento.capa = this.passedData.capa;
    },
    emiteFecho(){
      this.$emit('emiteFecho')
    }
  },
  watch:{
    passedData: {
        immediate: true,
        deep: true,
        handler(){
            this.onUpdate()
        }
    }
  },
  created(){
    this.onUpdate()
  }
}
</script>
<style scoped>
  #registar *{
            box-sizing: border-box;
  }
  #registar{
            margin: 20px auto;
            max-width: 800px;
  }
  #checkboxes input{
            display: inline-block;
            margin-right: 10px;
  }
  #checkboxes label{
            display: inline-block;
  }
</style>
