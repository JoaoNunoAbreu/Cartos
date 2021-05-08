<template>
  <div id="myApplication">
    <h1>{{elemento.id}}</h1>
    <p>{{elemento.titulo}}</p>
    <v-card>
        <v-img v-bind:src="capa" contain  max-width="100" />
        <pdf :src="ficheiro"></pdf>
    </v-card>
    <v-toolbar flat>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="emiteFecho" color="#26B99A" class="white--text change-font" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
            </template>
        </v-tooltip>
    </v-toolbar>
  </div>
</template>

<script>
import axios from "axios";
import pdf from 'vue-pdf';
export default {
  name: 'app',
  data(){
        return{
            url: process.env.VUE_APP_URL,
            elemento:{
                id: "",
                titulo: ""
            },
            dialog: false,
            capa: "",
            ficheiro: "",
        }
    },
    props:{
        passedData:{
        type:Object
        }
    },
    components: {
        pdf
    },
    methods: {
        onUpdate(){
            this.elemento.id = this.passedData.id,
            this.elemento.titulo = this.passedData.titulo
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
        console.log("Elemento id: " + this.elemento.id),
        axios
            .get(this.url+`/elementos/ver/${this.elemento.id}/foto`,{
                responseType:'arraybuffer'
            })
            .then(response => {
                var image = new Buffer(response.data, 'binary').toString('base64')
                this.capa = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
                console.log(this.capa)
            })
            .catch(err => {
                console.log(err.message)
                this.error = err.message;
            }),
        axios
            .get(this.url+`/elementos/ver/${this.elemento.id}/ficheiro`,{
                responseType:'arraybuffer'
            })
            .then(response => {
                var pdf = new Buffer(response.data, 'binary').toString('base64')
                this.ficheiro = `data:${response.headers['content-type'].toLowerCase()};base64,${pdf}`
                
            })
            .catch(err => {
                console.log(err.message);
                this.error = err.message;
            })
            

    }
}
</script>

<style>
#app {
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>