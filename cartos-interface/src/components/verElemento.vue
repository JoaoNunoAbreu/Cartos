<template>
  <div id="registar">
    <v-toolbar class="mt-n5" style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
      <h1>{{elemento.id}}</h1>
    </v-toolbar>
    <v-card class="mb-n5">
        <v-container>
            <v-simple-table class="table mr-10 ml-10">
            <template v-slot:default>
                <tbody>
                    <tr>
                        <td class="text-left"><b>{{$t('fol.titulo')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.titulo}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('elemForm.colecao')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.colecao}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.num')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.numero}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.serie')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.serie}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('elemForm.lingua')}}</b></td>
                        <td >
                            <v-layout>
                                {{elemento.lingua}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.nrPaginas')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.paginas}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.size')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.size}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.pers')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.personagens}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.estado')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.estado}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.edi')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.editora}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.dataP')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.dataPub}}
                            </v-layout>
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left"><b>{{$t('p1.tipo')}}</b></td>
                        <td>
                            <v-layout>
                                {{elemento.tipo}}
                            </v-layout>
                        </td>
                    </tr>
                </tbody>
            </template>
            </v-simple-table>
            <v-row class="mt-5 mb-1">
                <v-spacer></v-spacer>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                            <v-btn
                        @click="openImg = true;"
                        v-on="{ ...tooltip }"
                        class="grey--text mr-3" 
                        :disabled="!hasCapa">
                        <v-icon>mdi-image</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{ $t("p1.verCapa") }}
                    </span>
                </v-tooltip>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                            <v-btn
                        @click="openVideo = true;"
                        v-on="{ ...tooltip }"
                        class="grey--text mr-3" 
                        :disabled="!hasVideo">
                        <v-icon>mdi-movie</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{ $t("p1.verVideo") }}
                    </span>
                </v-tooltip>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                            <v-btn
                        @click="pdfDialog = true;"
                        v-on="{ ...tooltip }"
                        class="grey--text mr-3" >
                        <v-icon>mdi-eye</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{ $t("p1.pdf") }}
                    </span>
                </v-tooltip>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn color="#26B99A" class="white--text mr-4" @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-door-open</v-icon></v-btn>
                    </template>
                    <span>
                        {{$t('indForm.close')}}
                    </span>
                </v-tooltip>
            </v-row>
    
    </v-container>
    </v-card>

    <!-- Dialog do PDF -->

    <v-dialog @keydown.esc="failureDialog = false" v-model="failureDialog" scrollable width="500"> 
        <v-card>
          <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
            <h2>{{$t('navd.guser')}}</h2>
          </v-toolbar>
          <v-divider
          class="mx-4"
          horizontal
        ></v-divider>

          <v-row>
            <v-col style="margin-left:1cm;max-width:20px; margin-top:15px" >
              <v-icon x-large color="#c9302c" dark>mdi-close</v-icon>
            </v-col>
            <v-col>
              <v-card-text class="mt-2">
                {{$t('uF.badChoice')}}
              </v-card-text>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            
            <v-tooltip bottom> 
              <template v-slot:activator="{ on }">
                  <v-btn depressed color="white" @click="failureDialog=false" v-on="on">
                    <v-icon large>mdi-exit-to-app</v-icon>
                  </v-btn>
                </template>
                <span>{{ $t('nav.Sair') }}</span>
              </v-tooltip>

          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="pdfDialog" width="800px">
      <v-card>
          <template>
            <v-row>
                <v-col style=" text-align: right;">
              {{page}}/{{pageCount}}
               </v-col>
              <v-col style=" text-align: right;">
                <v-tooltip >
                    <template  v-slot:activator="{ on: tooltip }">
                    <v-btn color="#c9302c" dark @click="pdfDialog = false; page=1;" v-on="{ ...tooltip}">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('indForm.close')}}
                    </span>
                </v-tooltip>
              </v-col>
              </v-row>
               <v-row>
                <v-col>
                  <v-btn style="top:400px" color="#286090" dark @click="pageshift(-1)">
                      <v-icon>mdi-arrow-collapse-left</v-icon>
                  </v-btn>
                </v-col>
                <v-col>
                  <pdf 
                      :src="pdf"
                      :page="page"
                      @num-pages="pageCount = $event"	
                      @page-loaded="currentPage = $event"
                      style="width:620px"
                  ></pdf>
                </v-col>
              <v-col>
              <v-btn style="top:400px" color="#286090" dark @click="pageshift(1)">
              <v-icon>mdi-arrow-collapse-right</v-icon>
          </v-btn>
          </v-col>
              </v-row>
          </template>
      </v-card>
      
    </v-dialog>
    <v-dialog v-model="openImg" max-width="400px" >
        <img :src="elemento.capa" width="100%" @click.stop="openImg=false; hasCapa=false">
    </v-dialog>
    <v-dialog v-model="openVideo" max-width="400px" >
        <video width="100%" :src="elemento.video" controls contain></video>
        <v-btn @click="openVideo=false;">Sair</v-btn>
    </v-dialog>
  </div>
</template>

<script>

import axios from "axios";
import pdf from 'vue-pdf'

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
        tipo: "",
        capa: null,
        video: null,
      },
      url: process.env.VUE_APP_URL,
      dialog:false,
      dialogHelp:false,
      failureDialog:false,
      pageCount:0,
      currentPage:0,
      page:1,
      openImg: false,
      openVideo: false,
      pdfDialog:false,
      pdf:null,
      hasVideo:false,
      hasCapa:false,
    }
  },
  props:{
    passedData:{
      type:Object
    },
    value:{
      type:String
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
  },methods:{
    onUpdate(){
        if(this.elemento !== undefined && Object.keys(this.elemento).length != 0){
            this.elemento.id = this.passedData.id
            this.elemento.titulo = this.passedData.titulo
            this.elemento.colecao = this.passedData.colecao
            this.elemento.numero = this.passedData.numero
            this.elemento.serie = this.passedData.serie
            this.elemento.lingua = this.passedData.lingua
            this.elemento.paginas = this.passedData.nr_paginas
            this.elemento.size = this.passedData.tamanho
            this.elemento.personagens = this.passedData.personagens
            this.elemento.estado = this.passedData.estado
            this.elemento.editora = this.passedData.editora
            this.elemento.dataPub = this.passedData.data_publicacao
            this.elemento.tipo = this.passedData.tipo
            this.elemento.capa = this.passedData.capa
            this.elemento.video = this.passedData.video
            this.getPdf(this.elemento.id);
            this.getCapa(this.elemento.id);
            this.getVideo(this.elemento.id);
        }
    },
    reset () {
        this.elemento.id = "";
        this.elemento.titulo = "";
        this.elemento.colecao = "";
        this.elemento.numero = "";
        this.elemento.serie = "";
        this.elemento.lingua = "";
        this.elemento.paginas = "";
        this.elemento.size = "";
        this.elemento.personagens = "";
        this.elemento.estado = "";
        this.elemento.editora = "";
        this.elemento.dataPub = "";
        this.elemento.tipo = "";
        this.elemento.capa = null;
        this.elemento.video = null;
    },
    emiteFecho(){
        this.hasCapa=false
        this.hasVideo=false
        this.$emit('emiteFecho')
    },
    getPdf(id){
      axios.get(this.url + `/elementos/ver/${id}/ficheiro`, {
          responseType:'arraybuffer',
          headers: {
              'Authorization': `Bearer: ${this.$store.state.jwt}`
          }
      })
      .then(response => {
          var pdf = new Buffer(response.data, 'binary').toString('base64')
          this.pdf = `data:${response.headers['content-type'].toLowerCase()};base64,${pdf}`
      }).catch(e => {
          console.log(e)
      })
    },
    getCapa(id){
      axios
        .get(this.url + `/elementos/ver/${id}/foto`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          this.hasCapa=true;
          var image = new Buffer(response.data, "binary").toString("base64");
          this.elemento.capa = `data:${response.headers[
            "content-type"
          ].toLowerCase()};base64,${image}`;
        })
        .catch((err) => {
          this.hasCapa=false;
          this.error = err.message;
        })
    },
    getVideo(id){
      axios
        .get(this.url + `/elementos/ver/${id}/video`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          if(response.headers["content-type"]=="video/mp4"){
            this.hasVideo=true;
            var vi = new Buffer(response.data, "binary").toString("base64");
            this.elemento.video = `data:${response.headers[
              "content-type"
            ].toLowerCase()};base64,${vi}`;
          }
          
        })
        .catch((err) => {
          this.hasVideo=false;
          this.error = err.message;
        });
    },
    pageshift(shift){
        var temp = this.page + shift
        if (temp > 0 && temp <= this.pageCount){
            this.page=temp
        }
    }
  },
  created(){
    this.onUpdate()
  },
  components: {
    'pdf':pdf
  },
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
