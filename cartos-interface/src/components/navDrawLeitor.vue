<template>
    <v-card>
        <v-navigation-drawer app
          clipped
          v-if="true"
          v-model="drawer"
          style="background: linear-gradient(to bottom, #376a53 50%, #549d7c 100%);"
        >

          <v-list
            nav
            dense
            dark
          >
            <v-list-item link to="/leitor/elementos">
              <v-list-item-icon>
                <v-icon>mdi-folder-open</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.documents')}}</v-list-item-title>
            </v-list-item>
              
            <v-list-item link to="/leitor/analise">
              <v-list-item-icon>
                <v-icon>mdi-magnify</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('nav.barraPesquisa')}}</v-list-item-title>
            </v-list-item>
         
            <v-list-item link @click="about = true">
              <v-list-item-icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.about')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="about = false" v-model="about" scrollable width="500">
              <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                  <h2>{{ $t('nav.sabermais') }}</h2>
                </v-toolbar>
                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoSaberMais') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="about=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="credits = true">
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.credits')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="credits = false"  v-model="credits" scrollable width="500">
              <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                  <h2>{{ $t('nav.creditos') }}</h2>
                  
                </v-toolbar>
                
                <v-divider
                class="mx-4"
                horizontal
                ></v-divider>
                
                <v-card-text class="change-font mt-6" style="white-space: pre-line">
                  <h2> {{ $t('nav.textoCreditos') }} </h2>
                  <p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/Catarinacg16" target="blank_">Catarina Gil</a><p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/goncalo-f" target="blank_">Gonçalo Ferreira</a><p/>
                  <v-icon>mdi-github</v-icon> <a href="https://github.com/JoaoNunoAbreu" target="blank_">João Nuno Abreu</a>

                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="credits=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="terms = true">
              <v-list-item-icon>
                <v-icon>mdi-book-multiple</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Termos de Utilização</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="terms = false" v-model="terms" scrollable  width="500">
              <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                  <h2>{{ $t('nav.termos') }}</h2>
                </v-toolbar>

                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoTermos') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="terms=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-list-item link @click="priv = true">
              <v-list-item-icon>
                <v-icon>mdi-incognito</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Privacidade</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="priv = false" v-model="priv" scrollable width="500">
              <v-card>
                <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
                  <h2>{{ $t('nav.privacidade') }}</h2>
                </v-toolbar>
                
                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoPriv') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="priv=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-list>
          <template v-slot:append>
            <div class="pa-2">
              <v-tooltip top> 
                <template v-slot:activator="{ on }">
                  <v-btn dark depressed min-width="60px" @click="goHome();" v-on="on">
                    <v-icon>mdi-home</v-icon>
                  </v-btn>
                </template>
                <span>{{$t('navd.home')}}</span>
              </v-tooltip>
              <v-tooltip top> 
                <template v-slot:activator="{ on }">
                  <v-btn dark depressed min-width="60px" @click="logout();" v-on="on">
                    <v-icon>mdi-power</v-icon>
                  </v-btn>
                </template>
                <span>{{$t('navd.exit')}}</span>
              </v-tooltip>
            </div>
          </template>

        </v-navigation-drawer>
    </v-card>
</template>

<script>
import axios from 'axios'
import { eventBus } from '../main'
export default {
    data() {
        return{
            title: 'Vue',
            userPic: '',
            nome: this.$store.state.user._id,
            miniVariant: true,
            expandOnHover: true,
            priv:false,
            terms:false,
            credits:false,
            about:false,
            drawerOn: true,
            url: process.env.VUE_APP_URL,
            drawer:true
        }
    },
    created(){
      eventBus.$on('updateDrawer', a => {
        this.drawer = !this.drawer
        console.log(a)
      })
      axios.get(this.url + `/users/foto/${this.$store.state.user._id}`, {
        responseType:'arraybuffer',
        headers: {
            'Authorization': `Bearer: ${this.$store.state.jwt}`
        }
      })
      .then(response => {
        var image = new Buffer(response.data, 'binary').toString('base64')
        this.userPic = `data:${response.headers['content-type'].toLowerCase()};base64,${image}`
      }).catch(e => {
        console.log(e)
      })
    },
    methods:{
      logout: function(){
        //console.log("destroy token here")
        this.$store.commit("guardaTokenUtilizador", "")
        this.$store.commit("guardaNomeUtilizador", "")
        this.$router.push( {path:`/login`})
      },
      
      goHome: function(){
        this.$router.push( {path:`/home`})
      }
    }
};
</script>

<style scoped>

header{
    background: linear-gradient(to top, #376a53 0%, #549d7c 100%);
    padding: 10px;
}

h1{
    color:white;
    text-align:center;
}
.navBar{
  text-align: left;
}
h3{
    color:white;
}
.ava{
  margin-top: 50px;
}
</style>
