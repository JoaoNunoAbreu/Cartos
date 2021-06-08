<template>
    <div>
        <appHeader></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else >
            <navDrawLeitor></navDrawLeitor>
        </div>
        <div style="width:800px">
            <v-container class="ml-5">
                <h2>{{ $t('navd.cf') }}</h2>
                <v-divider></v-divider>
                <v-toolbar flat>
                    <v-text-field 
                        label="Indique que elementos quer (separados por vírgulas)"
                        v-model="chosenElementos"
                        class="mr-5 mt-10"
                    ></v-text-field>
                    <v-tooltip bottom> 
                        <template v-slot:activator="{ on }">
                        <v-btn max-width=20px class="change-font mr-5" v-on="on" @click="pesquisa">
                            <v-icon>mdi-magnify</v-icon>
                        </v-btn>
                        </template>
                        <span>{{ $t('nav.buttonPesquisa') }}</span>
                    </v-tooltip>
                    <v-tooltip bottom>
                        <template #activator="{ on: tooltip }">
                            <v-btn @click="helpCF = true" class="change-font mr-5" v-on="{ ...tooltip}"><v-icon>mdi-information</v-icon> </v-btn>
                        </template>
                        <span>{{$t('nav.buttonAjuda')}}</span>
                    </v-tooltip>
                    <v-tooltip bottom>
                        <template #activator="{ on: tooltip }">
                            <v-btn @click="dialogPesquisas = true" class="change-font" v-on="{ ...tooltip}"><v-icon>mdi-history</v-icon> </v-btn>
                        </template>
                        <span>{{$t('cf.seeHist')}}</span>
                    </v-tooltip>
                </v-toolbar>
            </v-container>
        </div>
        <v-dialog
            v-model="helpCF"
            scrollable 
            width="500"
            persistent
        >
            <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                    <h2>{{ $t('navd.cf') }}</h2>
                </v-toolbar>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                    <h3>{{ $t('cf.help') }}</h3>
                    </v-card-text>
                </v-col>
                </v-row>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click="helpCF = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('indForm.close')}}
                    </span>
                </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <div>
            <v-carousel
                v-model="activeSearch"
                height="900"
                hide-delimiter-background
                show-arrows-on-hover
            >
                <v-carousel-item
                v-for="(texto, i) in textoElementos"
                :key="i"
                >
                <v-sheet
                    color="lightgray"
                    height="100%"
                >
                    <v-row
                        class="fill-height scroll"
                        align="center"
                        justify="center"
                    >
                        <v-container persistent >
                            <h3>{{ $t('cf.f') }}: {{Object.keys(texto)[0]}} </h3>
                            <v-card width="100%" class="mb-12">
                                <v-card-text>
                                    {{Object.values(texto)[0]}}         
                                </v-card-text>
                            </v-card>
                        </v-container>
                    </v-row>
                </v-sheet>
                </v-carousel-item>
            </v-carousel>
        </div>
        <v-dialog
            v-model="dialog"
            scrollable 
            width="500"
            persistent
        >
            <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                <h2>{{ $t('navd.cf') }}</h2>
            </v-toolbar>
            <v-card>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                    <h3>{{ $t('cf.of') }} {{unexistentElemento}} {{ $t('cf.nArmaz') }}</h3>
                    </v-card-text>
                </v-col>
                </v-row>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                    <v-btn color="#c9302c" dark @click="dialog = false;chosenElementos=''" v-on="{ ...tooltip}">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('indForm.close')}}
                    </span>
                </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog
            v-model="dialogPesquisas"
            scrollable 
            width="40%"
            persistent
        >
            <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                  <h1>{{ $t('navd.cf') }}</h1>
                </v-toolbar>
                <v-row>
                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                    <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
                </v-col>
                <v-col>
                    <v-card-text>
                        <h2 class="mb-5">{{ $t('cf.hp') }}:</h2>
                        <h4 v-for="pesquisa in pesquisas.slice().reverse()" :key="pesquisa">
                            {{ $t('cf.p') }}:{{pesquisa.pesquisa}}, {{ $t('cf.feita') }}:{{pesquisa.data}}
                        </h4>
                    </v-card-text>
                </v-col>
                </v-row>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click="dialogPesquisas = false" v-on="{ ...tooltip}">
                        <v-icon>mdi-exit-to-app</v-icon>
                    </v-btn>
                    </template>
                    <span>
                    {{$t('indForm.close')}}
                    </span>
                </v-tooltip>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from "axios"
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
import Header from '../components/header.vue'
export default {
    data(){
        return{
            elementos:{},
            chosenElementos:"",
            textoElementos:[],
            activeSearch:false,
            unexistentElemento:"",
            dialog:false,
            helpCF:false,
            dialogPesquisas:false,
            pesquisas:[],
            url: process.env.VUE_APP_URL,
        }
    },
    components: {
        'navDraw':NavDraw,
        'appHeader': Header,
        'navDrawLeitor':navDrawLeitor,
    },
    created: function(){
        axios.get(this.url + `/elementos/elementos?nome=${this.$store.state.user._id}`,{headers:{
                Authorization:`Bearer: ${this.$store.state.jwt}`
        }})
        .then(response => {
            for(let i = 0;i<response.data.elementos.length;i++){
                this.elementos[`${response.data.elementos[i]._id}`] = response.data.elementos[i].textoSTags
            }
        }).catch(e => {
            this.errors.push(e)
        })
        axios.get(this.url + `/elementos/compElementos/pesquisas?nome=${this.$store.state.user._id}`,{
            headers: {
                Authorization: `Bearer: ${this.$store.state.jwt}`       
            }
        }).then(data => {
            this.pesquisas = data.data.pesquisas.slice(data.data.pesquisas.length - 11, data.data.pesquisas.length - 1)
        }).catch(e => {
            this.errors.push(e)
        })
    },
    methods:{
        sortOnKeys:function(dict) {
            var sorted = [];
            for(var key in dict) {
                sorted[sorted.length] = key;
            }
            sorted.sort();
            var tempDict = {};
            for(var i = 0; i < sorted.length; i++) {
                tempDict[sorted[i]] = dict[sorted[i]];
            }

            return tempDict;
        },
        pesquisa:function(){
            let formData = new FormData()
            formData.append('username',this.$store.state.user._id)
            if(this.chosenElementos != ""){
                formData.append('pesquisa',this.chosenElementos)
            }
            else{
                formData.append('pesquisa',"todos os elementos")
            }
            axios.post(this.url + `/elementos/compElementos/post?nome=${this.$store.state.user._id}`,formData,{
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer: ${this.$store.state.jwt}`       
                }
            }).then(data => {
                this.pesquisas = data.data.pesquisas.slice(data.data.pesquisas.length - 10, data.data.pesquisas.length)
            }).catch(e => {
                this.errors.push(e)
            })
            this.textoElementos = []
            let obj = {}
            var elems = this.chosenElementos.split(',')
            elems = elems.map(function (el) {
                return el.trim();
            });
            if(elems.length == 1 && elems[0] == ""){
                //this.pesquisas.push("tudo")
                var chaves = Object.keys(this.elementos)
                for(let j = 0; j<chaves.length;j++){
                    obj[chaves[j]] = this.elementos[chaves[j]]
                    this.textoElementos.push(obj)
                    this.activeSearch = true
                    obj = {}
                }
            }
            else{
                //this.pesquisas.push(this.chosenElementos)
                for(let i = 0;i<elems.length;i++){
                    if(elems[i].split('-').length > 2){
                        let array = elems[i].split('-')
                        let firstValue = array[0] + '-' + array[1]
                        let secondValue = array[2] + '-' + array[3]
                        if(firstValue in this.elementos && secondValue in this.elementos){
                            for(let unit in this.elementos){
                                if(firstValue <= unit && secondValue >= unit){
                                    obj[unit]=this.elementos[unit]
                                    this.textoElementos.push(obj)
                                    this.activeSearch = true
                                    obj = {}
                                }
                            }
                        }
                        else if(!(firstValue in this.elementos)){
                            this.unexistentElemento = firstValue
                            this.dialog = true
                        }
                        else if(!(secondValue in this.elementos)){
                            this.unexistentElemento = secondValue
                            this.dialog = true
                        }
                    }
                    else if(elems[i] in this.elementos){
                        obj[elems[i]]=this.elementos[elems[i]]
                        this.textoElementos.push(obj)
                        this.activeSearch = true
                        obj = {}
                    }
                    else{
                        this.unexistentElemento = elems[i]
                        this.dialog = true
                    }
                }
            }
        }
    }
}
</script>
<style scoped>
    .scroll{
        overflow-y:scroll
    }
</style>