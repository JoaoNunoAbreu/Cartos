<template>
    <div id="import">
        <appHeader :ajuda='ajuda'></appHeader>
        <navDraw></navDraw>
        <v-sheet
            class="mx-auto"
            elevation="8"
            max-width="800"
        >   
            <div class="import"></div>
            <v-card>
                <v-window v-model="model">
                    <v-window-item v-for="n in 1" :key="n">
                        <v-toolbar dark flat style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);">
                            <h3 class="ml-5"> {{$t('imp.passo')}}</h3>
                        </v-toolbar>
                        <passo1 v-if="n == 1 && renderComponent" :elemento="info" :cancelado="cancelado" @atualizaElemento=atualizaElemento($event) @submeterElemento=submeterElemento() ></passo1>

                        <v-toolbar flat color="white" v-if="n!=1 && n!=6">
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="prev" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-arrow-left</v-icon></v-btn>
                                </template>
                                <span>
                                    {{$t('imp.back')}}
                                </span>
                            </v-tooltip>
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on: tooltip }">
                                    <v-btn ref="submit" color="#26B99A" class="white--text mr-5" @click="next();" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                                </template>
                                <span>
                                    {{$t('p1.sub')}}
                                </span>
                            </v-tooltip>
                        </v-toolbar>
                        <v-dialog
                            v-model="fotoErro"
                            scrollable 
                            width="500"
                            persistent
                        >
                            <v-card>
                                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                                    <h2>{{$t('reg.pag')}}</h2>
                                </v-toolbar>
                                <v-row>
                                <v-col style="margin-left:1cm;margin-right:1cm;max-width:20px; margin-top:15px" >
                                    <v-icon x-large color="#c9302c" dark>mdi-close</v-icon>
                                </v-col>
                                <v-col>
                                    <v-card-text>
                                        <h3>{{$t('imp.seq')}}</h3>
                                    </v-card-text>
                                </v-col>
                                </v-row>

                                <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on: tooltip }">
                                    <v-btn @click="fotoErro = false" v-on="{ ...tooltip}">
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
                    </v-window-item>
                </v-window>
                
            </v-card>
        </v-sheet>
        <v-dialog @keydown.esc="failureDialog = false" v-model="failureDialog" scrollable width="500"> 
            <v-card>
                <v-toolbar cstyle="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                <h2>{{$t('reg.pag')}}</h2>
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
                        {{$t('imp.new')}}
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
    </div>
</template>

<script>
    import Header from '../components/header.vue'
    import NavDraw from '../components/navDraw.vue'
    import Passo1 from '../components/passo1.vue'
    import axios from 'axios'
    export default {
        data: () => ({
            value: null,
            model: null,
            ajuda:'imports',
            info:{
                id: "",
                titulo: "",
                colecao: "",
                numero: "",
                serie: "",
                lingua: "",
                páginas: "",
                size: "",
                personagens: "",
                estado: "",
                editora: "",
                dataPub: "",
                ficheiro: null,
                capa: null,
                video:null,
                tipo: "",
            },
            passo6info: {},
            cancelado: 0,
            renderComponent: true,
            fotoErro:false,
            failureDialog:false,
            url: process.env.VUE_APP_URL,
        }),
        components:{
            'appHeader': Header,
            'navDraw':NavDraw,
            'passo1':Passo1,
        },
        methods:{
            prev(){
                this.model -= 1
            },
            next(){
                this.model += 1
            },
            cancela(){
                // ----------------------------
                this.id = ""
                this.titulo = ""
                this.colecao = ""
                this.numero = ""
                this.serie = ""
                this.lingua = ""
                this.páginas = ""
                this.size = ""
                this.personagens = ""
                this.estado = ""
                this.editora = ""
                this.dataPub = ""
                this.ficheiro = null
                this.capa = null
                this.video = null
                this.tipo = ""
                // ----------------------------
                this.model = 0
                this.renderComponent = false
                this.$nextTick (() => {
                    this.renderComponent = true;
                });
            },
            atualizaElemento(elemento){
                this.info.id = elemento.id
                this.info.titulo = elemento.titulo
                this.info.colecao = elemento.colecao
                this.info.numero = elemento.numero
                this.info.serie = elemento.serie
                this.info.lingua = elemento.lingua
                this.info.paginas = elemento.paginas
                this.info.size = elemento.size
                this.info.personagens = elemento.personagens
                this.info.estado = elemento.estado
                this.info.editora = elemento.editora
                this.info.dataPub = elemento.dataPub
                this.info.ficheiro = elemento.ficheiro
                this.info.capa = elemento.capa
                this.info.video = elemento.video
                this.info.tipo = elemento.tipo
                this.submeterElemento();
            },
            submeterElemento(){
                let formData = new FormData()
                formData.append('id',this.info.id)
                formData.append('titulo',this.info.titulo)
                formData.append('colecao',this.info.colecao)
                formData.append('numero',this.info.numero)
                formData.append('serie',this.info.serie)
                formData.append('lingua',this.info.lingua)
                formData.append('paginas',this.info.paginas)
                formData.append('size',this.info.size)
                formData.append('personagens',this.info.personagens)
                formData.append('estado',this.info.estado)
                formData.append('editora',this.info.editora)
                formData.append('dataPub',this.info.dataPub)
                formData.append('ficheiro',this.info.ficheiro)
                formData.append('capa',this.info.capa)
                formData.append('video',this.info.video)
                formData.append('tipo',this.info.tipo)

                axios.post(this.url+`/import/passo6/?nome=${this.$store.state.user._id}`,formData,{headers:{
                    'Content-Type': 'multipart/form-data',
                    Authorization:`Bearer: ${this.$store.state.jwt}`
                }})
                .then(() => {
                    this.model = 0
                    
                }).catch(e => {
                    console.log("ERRO = " + e)
                    this.errors.push(e)
                })
            }
        },
        updated () {
            if(this.model == null){
                this.value = 0
            }
            this.value = parseInt(100/6 * this.model,10)
        }
    }
</script>

<style scoped>
    #import{
        margin-bottom: 50px;
    }
.mx-auto .import{
            margin: 20px auto;
            max-width: 800px;
  }
</style>