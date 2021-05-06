<template>
  <div>
    <v-sheet color="grey lighten-4" tile>
      <v-row class="fill-height ml-10" align="center" justify="center">
        <v-col class="text-left">
          <v-form
            ref="form"
            method="post"
            enctype="multipart/form-data">
            <v-container>
              <div class="p-container">
                <div class="child-right">
                  <v-text-field
                    :label="$t('p1.id')"
                    v-model="id"
                    :rules="[rules.inicioNome, rules.tresDigitos, rules.seiscar]"
                    required>
                  </v-text-field>
                  <v-text-field
                    :label="$t('p1.tit')"
                    v-model="titulo"
                    required>
                  </v-text-field>
                  <div class="p-container">
                    <div class="child">
                      <v-select
                        class="change-font"
                        required
                        v-model="colecao"
                        :items="colecaoSel"
                        v-bind:label="$t('p1.col')">
                      </v-select>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.num')"
                        v-model="numero"
                        required
                      ></v-text-field>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.serie')"
                        v-model="serie"
                        required
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-select
                        class="change-font"
                        required
                        v-model="lingua"
                        :items="linguaSel"
                        v-bind:label="$t('p1.lin')"
                      ></v-select>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.pag')"
                        v-model="paginas"
                        required
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.size')"
                        v-model="size"
                        required
                      ></v-text-field>
                    </div>
                  </div>
                </div>
                <div class="child-left">
                  <label>{{ $t("p1.foto") }}:</label>
                  <v-file-input
                    show-size
                    accept="image/jpg, image/jpeg, image/png"
                    :label="$t('p1.file')"
                    v-model="capa"
                    @change="previewImage">
                  </v-file-input>
                  <v-img :src="this.url" contain></v-img>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-text-field
                    :label="$t('p1.pers')"
                    v-model="personagens"
                    required
                  ></v-text-field>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.estado')"
                    v-model="estado"
                    required
                  ></v-text-field>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-select
                    class="change-font"
                    required
                    v-model="editora"
                    :items="editoraSel"
                    v-bind:label="$t('p1.edi')"
                  ></v-select>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.dataP')"
                    v-model="dataPub"
                    :rules="[rules.dataRule]"
                    required
                  ></v-text-field>
                </div>
              </div>
              <div class="p-container">
                <div class="child" >
                  <v-row align="center">
                  <v-file-input
                    show-size
                    type="file"
                    :label="$t('p1.tfile')"
                    v-model="ficheiro"
                  ></v-file-input>
                  </v-row>
                </div>
                <div class="child">
                  <v-select
                    class="change-font"
                    required
                    v-model="tipo"
                    :items="tipoSel"
                    v-bind:label="$t('p1.tipo')"
                  ></v-select>
                </div>
              </div>
            </v-container>
            <v-container style="width: 750px">
              <v-toolbar flat color="grey lighten-4">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      ref="submit"
                      class="orange white--text mr-3"
                      @click="save()"
                      v-on="{ ...tooltip }"
                      ><v-icon>mdi-checkbox-marked-outline</v-icon></v-btn
                    >
                  </template>
                  <span>
                    {{ $t("p1.save") }}
                  </span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      @click.prevent="reset"
                      v-on="{ ...tooltip }"
                      color="#26B99A"
                      class="white--text mr-3"
                      ><v-icon>mdi-broom</v-icon></v-btn
                    >
                  </template>
                  <span>
                    {{ $t("p1.reset") }}
                  </span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      ref="submit"
                      @click="submeter()"
                      :disabled="disableButton"
                      class="mr-5"
                      v-on="{ ...tooltip }"
                      ><v-icon>mdi-exit-to-app</v-icon></v-btn
                    >
                  </template>
                  <span>
                    {{ $t("p1.sub") }}
                  </span>
                </v-tooltip>
                <v-spacer></v-spacer>
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
                    {{ $t("p1.ajuda") }}
                  </span>
                </v-tooltip>
                <v-dialog
                  @keydown.esc="dialog = false"
                  v-model="dialog"
                  scrollable
                  width="500"
                >
                  <v-card>
                    <v-toolbar color="#2A3F54" dark>
                      <h3>{{ $t("navd.importAjuda") }}</h3>
                    </v-toolbar>
                    <v-divider class="mx-4" horizontal></v-divider>

                    <v-card-text
                      class="change-font mt-6"
                      style="white-space: pre-line"
                      >{{ $t("navd.textoImportAjuda") }}</v-card-text
                    >
                    <v-card-actions>
                      <v-spacer></v-spacer>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                          <v-btn
                            depressed
                            color="white"
                            @click="dialog = false"
                            v-on="on"
                          >
                            <v-icon large>mdi-exit-to-app</v-icon>
                          </v-btn>
                        </template>
                        <span>{{ $t("nav.Sair") }}</span>
                      </v-tooltip>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      link
                      to="/admin/elementos"
                      v-on="{ ...tooltip }"
                      color="#26B99A"
                      class="white--text mr-3"   
                      ><v-icon>mdi-door-open</v-icon></v-btn
                    >
                  </template>
                  <span>
                    {{ $t("p1.leave") }}
                  </span>
                </v-tooltip>
              </v-toolbar>
            </v-container>
          </v-form>
        </v-col>
      </v-row>
    </v-sheet>
  </div>
</template>
<script>
//depois usar para estabelecer as rules dos campos do form
//import { required, email, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data() {
    return {
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
      tipo: "",
      capa: null,
      url:"",
      saveClick: false,
      dialog:false, 
      rules: {
        inicioNome: (value) =>
          value.startsWith("RPT") ||
          "O nome do Elemento necessita de começar com RPT",
        tresDigitos: (value) =>
          value.replace(/[^0-9]/g,"").length == 3||
          "O nome do Elemento tem de ter 3 dígitos",
        seiscar: (value) =>
          value.length == 6||
          "O nome do Elemento tem de ter 6 caracteres",
        dataRule: (value) =>{
          const pattern = /^((0)[1-9]|[1-2][0-9]|(3)[0-1])(\/)(((0)[1-9])|((1)[0-2]))(\/)\d{4}$/
          return pattern.test(value) || 'A data deve ter o formato : DD/MM/AAAA'
        }
      },
      colecaoSel: ["C1", "C2","C3"],
      linguaSel: ["Português", "Inglês", "Espanhol"],
      editoraSel:["Porto Editora","Porto Editora 2","Porto Editora 3"],
      tipoSel:["Tipo1","Tipo2","Tipo3"]
    };
  },
  props: {
    elemento: {
      type: Object,
    },
  },
  created() {
    this.id = this.elemento.id;
    this.titulo = this.elemento.titulo;
    this.colecao = this.elemento.colecao;
    this.numero = this.elemento.numero;
    this.serie = this.elemento.serie;
    this.lingua = this.elemento.lingua;
    this.paginas = this.elemento.paginas;
    this.size = this.elemento.size;
    this.personagens = this.elemento.personagens;
    this.estado = this.elemento.estado;
    this.editora = this.elemento.editora;
    this.dataPub = this.elemento.dataPub;
    this.ficheiro = this.elemento.ficheiro;
    this.tipo = this.elemento.tipo;
    this.capa= this.elemento.capa;
  },
  methods: {
    reset() {
      //needs work for more resets
      this.$refs.form.reset();
      (this.id =""),
      (this.titulo = ""),
      (this.colecao = ""),
      (this.numero = ""),
      (this.serie= ""),
      (this.lingua= ""),
      (this.paginas= ""),
      (this.size= ""),
      (this.personagens= ""),
      (this.estado= ""),
      (this.editora= ""),
      (this.dataPub= ""),
      (this.ficheiro= null),
      (this.tipo= ""),
      (this.capa=null)
      },
    save() {
      this.saveClick=true;
      this.$emit("atualizaElemento", this);
    },
    submeter() {
      this.skip = 1;
      //console.log(this.skip)
      this.$emit("submeterElemento", this);
    },
    previewImage: function() {
      this.url= URL.createObjectURL(this.capa)
    }

    /*
    atualizarInfo(){
      this.$emit('atualizarInfoPasso1','skip')
    }*/
  },
  computed: {
    disableButton() {
      if (
        this.id.length > 1 &&
        this.titulo.length > 0 &&
        this.colecao &&
        this.numero.length >0 &&
        this.serie.length > 0 &&
        this.lingua &&
        this.paginas.length > 0 &&
        this.size.length > 0 &&
        this.personagens.length > 0 &&
        this.estado.length > 0 &&
        this.editora &&
        this.dataPub.length > 0 &&
        this.ficheiro  &&
        this.tipo &&
        this.saveClick
      )
        return false;
      else return true;
    },
  },
};
</script>
<style scoped>
.v-text-field label {
  font-size: 20px;
}

.p-container {        
    display: flex;
    align-items: center;
}
.child {
  width: 80%;
}
.child-right{
  width: 1000px;
  float: right;
}
.child-left{
  width:50% ;
  margin-left: 50px;
  float: right;
}

.file-upload-form, .image-preview {
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    padding: 20px;
}
img.preview {
    width: 200px;
    background-color: white;
    border: 1px solid #DDD;
    padding: 5px;
}
</style>