<template>
    <div id="homeAdmin" style="width:70%">
        <appHeader></appHeader>
        <navDraw></navDraw>
        <div >

            <!-- Counters -->
            <v-toolbar flat style="margin-top:2.5cm;margin-bottom:2.5cm">
                <v-row>
                    <v-col>
                        <v-card class="text-center ml-10 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-folder-open</v-icon>{{$t('hAdmin.f')}}</h4>
                                <h2 style="color:#549d7c"><b>{{nElementos}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-10 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-folder-open</v-icon>{{$t('hAdmin.col')}}</h4>
                                <h2 style="color:#549d7c"><b>{{nColecoes}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-divider vertical></v-divider>
                    <v-col>
                        <v-card class="text-center ml-10 mr-5">
                            <v-card-text>
                                <h4><v-icon class="mr-2">mdi-account-multiple</v-icon>{{$t('hAdmin.users')}}</h4>
                                <h2 style="color:#549d7c"><b>{{nUsers}}</b></h2>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-toolbar>
        </div>
        <v-divider horizontal class="mt-n7"></v-divider>
        <template>
            <h3 style="text-align: center" class="mx-auto mt-5">{{$t('hAdmin.ultimosInseridos')}}</h3>
      
            <v-card
                elevation="2"
                class="mx-auto mt-5"
            >
                <!-- Last 3 elements uploaded-->
                
                <v-carousel  cycle
                    height="350"
                    show-arrows-on-hover
                >
                    <v-carousel-item v-for="(i) in 2" :key="i">
                   
                        <!-- <v-card 
                            class="mx-auto"
                            max-width="400"
                            light    
                        > -->
                        <v-layout row>
                        <v-flex xs4  v-for="(elem,j) in ele[i-1]" :key="j" >
                         
                            <v-img v-if="i===1"
                                class="white--text align-end"
                                height="150px"
                                :src="capas[j]"
                            ></v-img>
                            <v-img v-else
                                class="white--text align-end"
                                height="150px"
                                :src="capas[3+j]"
                            ></v-img>
                             <!-- <v-expand-transition>
                            <div v-if="hover" class="d-flex transition-fast-in-fast-out teal darken-1 v-reveal display-3 white--text"
                                style="height: 100%;">
                                <v-spacer></v-spacer>
                                <v-btn icon  color="white" ><v-icon  @click="viewItem(elem)">mdi-eye</v-icon></v-btn>
                                <v-spacer></v-spacer>
                            </div>
                            
                            </v-expand-transition> -->
                            
                            <div class=text-center>
                                <v-card-title style="color:black;" cprimary-title class="justify-center">
                                    {{elem.id}} 
                                </v-card-title>
                                <v-card-subtitle class="pb-0">
                                {{elem.data_publicacao}}
                                </v-card-subtitle>
                                <v-card-text class="text--primary">
                            
                                <div><b>{{$t('fol.col')}}:</b> {{elem.colecao}}</div>
                                <div><b>{{$t('fol.edi')}}:</b> {{elem.editora}}</div>
                                <div><b>{{$t('fol.lin')}}:</b> {{elem.lingua}}</div>
                                </v-card-text>
                            </div>
                        <!-- </v-card> -->
                        </v-flex>
                        </v-layout>

                    </v-carousel-item>
                </v-carousel>
            </v-card>

            <v-divider horizontal class="mt-8"></v-divider>

            <!-- Colecoções Graph -->

            <div class="mt-5">
                <h3 style="text-align: center">{{$t('hAdmin.nElemCol')}}</h3>
                <div class="small">
                    <line-chart :passedData="colecoes"></line-chart>
                </div>
            </div>

            <!-- Editoras Graph -->

            <div class="mt-5">
                <h3 style="text-align: center">{{$t('hAdmin.nElemEdi')}}</h3>
                <div class="small">
                    <line-chart :passedData="editoras"></line-chart>
                </div>
            </div>
        </template>
        <v-dialog persistent v-model="dialog" max-width="800px">
            <elementoFormEditable
              :elemento="item"
              :isDisabled="true"
              :isDeleting="false"
              @emiteFecho="emiteFecho($event)"
            ></elementoFormEditable>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import LineChart from '@/components/LineChart'
import ElementoFormEditable from "../components/elementoFormEditable.vue";

export default {
    data(){
        return{
            nElementos:0,
            nColecoes:0,
            nUsers:0,
            colecoes:{},
            ele:[],
            editoras:{},
            value:[],
            number:[],
            capas:[],
            percent:0,
            last6Elements: [],
            condition:false,
            item: null,
            dialog: false,
            url: process.env.VUE_APP_URL,
            headers: [{
                text: this.$t("fol.id"),
                align: "start",
                value: "id",
                },
                {
                text: `${this.$t("fol.col")}`,
                value: "colecao",
                },
                {
                text: this.$t("fol.edi"),
                value: "editora",
                },
                {
                text: `${this.$t("fol.data")}`,
                value: "data_publicacao",
                },
                {
                text: `${this.$t("fol.lin")}`,
                value: "lingua",
                },
                {
                text: `${this.$t("fol.opt")}`,
                value: "options",
                sortable: false,
                
                },
        ],
        }
    },
    components:{
            'appHeader': Header,
            'navDraw':NavDraw,
            LineChart,
            elementoFormEditable: ElementoFormEditable,
    },
    watch: {
        dialog(val) {
            val || this.close();
        }
    },
    created: async function() {

        axios.get(this.url + `/home/index`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            this.last6Elements = response.data.lastElementos;
            let firstHalf = this.last6Elements.slice(0, this.last6Elements.length/2)
            let secondHalf = this.last6Elements.slice(-this.last6Elements.length/2)
            this.ele = [firstHalf,secondHalf]
            this.nUsers = response.data.n_users;
            this.nElementos = response.data.n_elementos;
            this.nColecoes= response.data.n_colecoes;
            this.colecoes = response.data.colecoesContadas;
            this.editoras = response.data.editorasContadas;

            for(let i = 0; i < this.last6Elements.length; i++){

                var idd = this.last6Elements[i].id;
                axios.get(this.url + `/elementos/ver/${idd}/foto`, {
                    responseType: "arraybuffer",
                })
                .then((response) => {
                    var image = new Buffer(response.data, "binary").toString("base64");
                    this.capas.push(`data:${response.headers[
                        "content-type"
                    ].toLowerCase()};base64,${image}`);
                  
                })
                .catch((err) => {
                    console.log(err.message);
                    this.error = err.message;
                })
                
            }
            

        }).catch(e => {
            console.log(e);
            alert("Não foi possível estabelecer conexão com a base de dados. Por favor dar refresh da página.")
        })
        
     
       
     
    },
    methods:{
        getOccurrence: function(array, value) {
            var count = 0;
            array.forEach((v) => (v === value && count++));
            return count;
        },
         printSection() {
            this.$htmlToPaper("tabelaElementos");
        },
        viewItem(item) {
            this.item = item;
            this.dialog = true;
        },
        close() {
            this.dialog = false;
            this.item = {};
        },
        emiteFecho: function () {
            this.dialog = false;
            /* this.getElementos(); */
        },
    }
}
</script>
<style scoped>
    .v-data-table /deep/ th {
        background: linear-gradient(to top, #376a53 0%, #549d7c 100%);
        }
    .v-data-table /deep/ tr {
        color: black;
        font-size: 13px;
        }
    .v-data-table /deep/ tr:nth-child(even) {
        background-color: rgb(245, 245, 245);
    }
    label {
        color: white;
        padding: 8px;
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }
    #homeAdmin *{
            box-sizing: border-box;
    }
    #homeAdmin{
                margin: 20px auto;
                margin-bottom: 80px;
    }
    
</style>

<style>
.v-carousel__controls{
    background:  linear-gradient(to top, #376a53 0%, #549d7c 100%);
}
.v-expansion-panel {
  box-shadow: none;
}
.v-reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .9;
  position: absolute;
  width: 100%;
}

.small {
  transform: scale(0.9, 0.9);
  -ms-transform: scale(0.9, 0.9); /* IE 9 */
  -webkit-transform: scale(0.9, 0.9); /* Safari and Chrome */
  -o-transform: scale(0.9, 0.9); /* Opera */
  -moz-transform: scale(0.9, 0.9); /* Firefox */
}

</style>