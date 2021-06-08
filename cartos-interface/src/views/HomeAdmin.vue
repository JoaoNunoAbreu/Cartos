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
            <h3 style="text-align: center" class="mx-auto mt-5">Últimos Elementos Inseridos</h3>
            <v-card
                elevation="2"
                max-width="400"
                class="mx-auto mt-5"
            >
                <!-- Last 3 elements uploaded-->
                
                <v-carousel  cycle
                    height="350"
                    show-arrows-on-hover
                >
                    <v-carousel-item
                        v-for="(elem,idx) in last3Elements"
                        :key="idx"
                    >
                   
                        <v-card 
                            class="mx-auto"
                            max-width="400"
                            light    
                        >
                         <v-hover v-slot="{ hover }">
                            <v-img
                                class="white--text align-end"
                                height="150px"
                                :src="capas[idx]"
                            >
                            
                             <v-expand-transition>
                            <div v-if="hover" class="d-flex transition-fast-in-fast-out teal darken-1 v-reveal display-3 white--text"
                                style="height: 100%;">
                                <v-spacer></v-spacer>
                                <v-btn icon  color="white" ><v-icon  @click="viewItem(item)">mdi-eye</v-icon></v-btn>
                                <v-spacer></v-spacer>
                            </div>
                            
                            </v-expand-transition>
                            </v-img>
                            </v-hover>
                            <div class=text-center>
                                <v-card-title cprimary-title class="justify-center">
                                    {{elem.id}} 
                                </v-card-title>
                                <v-card-subtitle class="pb-0">
                                {{elem.data_publicacao}}
                                </v-card-subtitle>
                                <v-card-text class="text--primary">
                            
                                <div><b>Coleção:</b> {{elem.colecao}}</div>
                                <div><b>Editora:</b> {{elem.editora}}</div>
                                <div><b>Língua:</b> {{elem.lingua}}</div>
                                </v-card-text>
                            </div>
                        </v-card>
                   
                    </v-carousel-item>
                </v-carousel>
            </v-card>

            <v-divider horizontal class="mt-8"></v-divider>

            <!-- Colecoções Graph -->

            <div class="mt-5">
                <h3 style="text-align: center">Nº Elementos por Coleção</h3>
                <line-chart :passedData="colecoes"></line-chart>
            </div>

            <!-- Editoras Graph -->

            <div class="mt-5">
                <h3 style="text-align: center">Nº Elementos por Editora</h3>
                <line-chart :passedData="editoras"></line-chart>
            </div>
            
        </template>
    </div>
</template>
<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import LineChart from '@/components/LineChart'

export default {
    data(){
        return{
            nElementos:0,
            nColecoes:0,
            nUsers:0,
            colecoes:{},
            editoras:{},
            value:[],
            number:[],
            capas:[],
            percent:0,
            last3Elements: [],
            condition:false,
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
            LineChart
    },
    created: async function() {

        axios.get(this.url + `/home/index`, { headers: { Authorization: `Bearer: ${this.$store.state.jwt}` } })
        .then(response => {
            this.last3Elements = response.data.lastElementos;
            this.nUsers = response.data.n_users;
            this.nElementos = response.data.n_elementos;
            this.nColecoes= response.data.n_colecoes;
            this.colecoes = response.data.colecoesContadas;
            this.editoras = response.data.editorasContadas;
            console.log("editoras = " + this.editoras)

            for(let i = 0;i<response.data.lastElementos.length;i++){

                var idd = this.last3Elements[i].id;
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
            alert("Não foi possível estabelecer conexão com a base de dados.")
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

</style>