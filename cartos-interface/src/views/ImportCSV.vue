<template>
  <div id="elementos">
    <appHeader></appHeader>
    <div v-if="this.$store.state.user.tipo === 'Admin'">
      <navDraw></navDraw>
    </div>
    <div v-else>
      <navDrawLeitor></navDrawLeitor>
    </div>
    <div class="ml-16 mt-16">
      <h1><b>{{ $t("navd.import") }}</b></h1>
      <v-file-input
          style="width:40%"
          show-size
          type="file"
          :label="$t('p1.file')"
          accept="text/csv"
          placeholder="csv"
          v-model="ficheiro"
          ref="inputFile"
      ></v-file-input>
      <v-tooltip bottom>
      <template v-slot:activator="{ on: tooltip }">
      <v-btn
        ref="submit"
        class="orange white--text mr-3"
        :disabled="disableButton"
        @click="save"
        v-on="{ ...tooltip }"
        ><v-icon>mdi-checkbox-marked-outline</v-icon></v-btn
      >
      </template>
      <span>
        {{ $t("p1.sub") }}
      </span>
      </v-tooltip>
      <v-tooltip bottom>
      <template v-slot:activator="{ on: tooltip }">
        <v-btn
          @click="ficheiro = null;"
          v-on="{ ...tooltip }"
          color="#26B99A"
          class="white--text mr-3"
          ><v-icon>mdi-broom</v-icon></v-btn
        >
      </template>
      <span>
        {{ $t("p1.clean") }}
      </span>
      </v-tooltip>
       <v-tooltip bottom>
      <template v-slot:activator="{ on: tooltip }">
      <v-btn  
        @click="dialog = true"
        v-on="{ ...tooltip }"
        color="#00004d"
        class="white--text mr-3"
        ><v-icon>mdi-help</v-icon></v-btn
      >
       </template>
      <span>
        {{ $t("navd.help") }}
      </span>
      </v-tooltip>
      
      <!-- Dialog do texto de ajuda -->

      <v-dialog
        @keydown.esc="dialog = false"
        v-model="dialog"
        scrollable
        width="850"
      >
        <v-card>
          <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
            <h3>{{ $t("navd.importAjuda") }}</h3>
          </v-toolbar>
          <v-divider class="mx-4" horizontal></v-divider>

          <v-card-text
            class="change-font mt-6"
            style="white-space: pre-line"
            >
            {{ $t("navd.textoImportAjuda") }}<v-icon small >mdi-checkbox-marked-outline</v-icon>
            <p>{{ $t("navd.textoImportAjuda2") }}</p>
            <pre><code>Identificador,Titulo,Numero,Colecao,Série,Editora,Língua,NrPaginas,Tamanho,DtPublicacao,Personagens,Tipo,Estado
RPT007,Batman: The Dark Knight,1,Batman,Batman,DC,Inglês,22,A4,01/01/2011,Batman,Ação,Bom</code></pre>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  depressed
                  color="#26B99A"
                  @click="dialog = false"
                  class="white--text"
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

      <v-dialog v-model="confirmDialog" scrollable width="500">
        <InfoPopup 
          :nSucesso="nSucesso"
          :nInsucesso="nInsucesso"
           @emiteFecho="emiteFecho($event)">
        </InfoPopup>
      </v-dialog>

    </div>
  </div>
</template>
<script>

import CSVFileValidator from 'csv-file-validator';
import InfoPopup from "../components/InfoPopup.vue";
import Header from "../components/header.vue";
import NavDraw from "../components/navDraw.vue";
import navDrawLeitor from "../components/navDrawLeitor.vue";
import axios from "axios"; 
export default {
  data() {
    return {
        url: process.env.VUE_APP_URL,
        ficheiro: null,
        dialog:false,
        confirmDialog:false,
        elemImport:[],
        nSucesso: 0,
        nInsucesso: 0,
        csvFields : [
          {name: 'Identificador',inputName: 'Identificador',required: true},
          {name: 'Titulo',inputName: 'Titulo',required: true},
          {name: 'Numero', inputName: 'Numero',required: true},
          {name: 'Colecao',inputName: 'Colecao',required: true},
          {name: 'Série',inputName: 'Série',required: true},
          {name: 'Editora',inputName: 'Editora',required: true },
          {name: 'Língua',inputName: 'Língua',required: true},
          {name: 'NrPaginas',inputName: 'NrPaginas',required: true},
          {name: 'Tamanho',inputName: 'Tamanho',required: true},
          {name: 'DtPublicacao',inputName: 'DtPublicacao',required: true},
          {name: 'Personagens',inputName: 'Personagens',required: true,isArray: true},
          {name: 'Tipo',inputName: 'Tipo',required: true},
          {name: 'Estado',inputName: 'Estado',required: true}
        ]
    };
  },
  components: {
    appHeader: Header,
    navDraw: NavDraw,
    navDrawLeitor: navDrawLeitor,
    InfoPopup
  },
  created() {
    axios.get(this.url + `/elementos/elementos?nome=${this.$store.state.user._id}`,{
        headers: {
          Authorization: `Bearer: ${this.$store.state.jwt}`,
        },
      }
    )
    .then((response) => {
      for (let i = 0; i < response.data.length; i++)
        this.elemImport.push(response.data[i].id);
    })
    .catch((e) => {
      this.errors.push(e);
    });
  },
  methods: {
    save(){
      const config = {
        headers: this.csvFields, // required
      }
      CSVFileValidator(this.ficheiro, config)
        .then(csvData => {
          csvData.data // Array of objects from file
          csvData.inValidMessages // Array of error messages

        let seenIDS = []
        for(let i = 0; i < csvData.data.length; i++){
          if(seenIDS.includes(csvData.data[i].Identificador)){
            this.nInsucesso++;
            csvData.data.splice(i,1)
          }
          else{
            seenIDS.push(csvData.data[i].Identificador)
          }
        }

        if(csvData.inValidMessages.length == 0){
          this.doPostsSync(csvData);
        }
        this.confirmDialog = true
      })
      .catch(err => {
        console.log(err)
      })
    },
    async doPosts(formData){
      try{
        await axios.post(this.url+`/import/passo6/?nome=${this.$store.state.user._id}`,formData,{
          headers:{
            'Content-Type': 'multipart/form-data',
            Authorization:`Bearer: ${this.$store.state.jwt}`
          }
        })
        .then(() => {
          this.nSucesso+=1;
        })
      }
      catch(e){
        console.log("ERRO = " + e)
        this.errors.push(e)
      }
    },
    async doPostsSync(csvData) {
      for(let i = 0; i < csvData.data.length; i++){
        if(this.idRules(csvData.data[i].Identificador) && this.anotherRules(csvData.data[i])){
          let formData = new FormData()
          let personagens = String(csvData.data[i].Personagens).replace(/;/g, ",")
          formData.append('id',csvData.data[i].Identificador)
          formData.append('titulo',csvData.data[i].Titulo)
          formData.append('colecao',csvData.data[i].Colecao)
          formData.append('numero',csvData.data[i].Numero)
          formData.append('serie',csvData.data[i].Série)
          formData.append('lingua',csvData.data[i].Língua)
          formData.append('paginas',csvData.data[i].NrPaginas)
          formData.append('size',csvData.data[i].Tamanho)
          formData.append('personagens',personagens)
          formData.append('estado',csvData.data[i].Estado)
          formData.append('editora',csvData.data[i].Editora)
          formData.append('dataPub',csvData.data[i].DtPublicacao)
          formData.append('tipo',csvData.data[i].Tipo)

          await this.doPosts(formData)
          console.log("making post request " + i)
        }
        else { 
          this.nInsucesso+=1;
        }
      }
    },
    idRules(elemId){
       return ( !this.elemImport.includes(elemId) && 
                elemId.substring(0,3)=="RPT" && 
                elemId.length==6 &&
                elemId.replace(/[^0-9]/g, "").length == 3)
    },
    anotherRules(elem){
      let pattern = /^((0)[1-9]|[1-2][0-9]|(3)[0-1])(\/)(((0)[1-9])|((1)[0-2]))(\/)\d{4}$/;
      return ( pattern.test(elem.DtPublicacao) &&  
               elem.Titulo.length <= 100 && elem.Colecao.length <= 100 && 
               elem.Numero.length <= 100 && elem.Série.length <= 100 && 
               elem.Língua.length <= 100 && elem.NrPaginas.length <= 3 && 
               elem.Tamanho.length <= 100 && elem.Estado.length <= 100 && 
               elem.Editora.length <= 100 && elem.DtPublicacao.length <= 100 &&
               elem.Personagens.length <= 200)
          
    },
    emiteFecho: function () {
      this.confirmDialog=false;
      this.nSucesso=0;
      this.nInsucesso=0;
      this.$router.push( {path:`/admin/elementos`})
    },

  },
  computed:{
    disableButton() {
      return !this.ficheiro
    },
  }
};
</script>
<style scoped>
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
label {
  color: white;
  padding: 8px;
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 15px;
}
b {
  font-size: 20px;
}
</style>
