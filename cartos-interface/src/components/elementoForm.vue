<template>
  <div id="registar">
      <v-card height="100%" width="100%">
        <v-toolbar color="#2A3F54" dark>
          <h1>{{$t('fol.title')}}</h1>
        </v-toolbar>
        <v-card-title>
          <h3>{{$t('folForm.visFol')}}</h3>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.id')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.idElemento}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.ver')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.versao}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.tipo')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.tipo}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.desc')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.descricao}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('folForm.sum')}}</b></td>
                                <td>
                                    <v-layout class="ml-12">
                                        {{elemento.sumario}}
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
                            {{$t('folForm.tComTags')}}
                        </span>
                      </v-tooltip>
                    </template>
                    <v-card height="100%" width="100%">
                        <v-card-title>
                            <h1>{{$t('folForm.tComTags')}}</h1>
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
                              {{$t('folForm.tSemTags')}}
                          </span>
                        </v-tooltip>
                      </template>
                      <v-card height="100%" width="100%">
                          <v-card-title>
                              <h1>{{$t('folForm.tSemTags')}}</h1>
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
        idElemento:"",
        versao:"",
        textoCTags:"",
        textoSTags:"",
        tipo:"",
        data:"",
        descricao:"",
        sumario:""
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
      this.elemento.idElemento = this.passedData._id
      this.elemento.versao = this.passedData.versao
      this.elemento.textoCTags = this.passedData.textoCTags
      this.elemento.textoSTags = this.passedData.textoSTags
      this.elemento.tipo = this.passedData.tipo
      this.elemento.data = this.passedData.data
      this.elemento.descricao = this.passedData.descricao
      this.elemento.sumario = this.passedData.sumario
    },
    atualizarInfo(){
      this.$emit('atualizarInfo')
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
