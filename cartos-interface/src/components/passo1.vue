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
                    :rules="[rules.inicioNome, rules.umHifen]"
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
                  <div class="image-preview" v-if="imageData.length > 0">
                      <img class="preview" :src="imageData">
                  </div>
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
                      to="/admin/folios"
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
      imageData: "" ,
      capa: null,
      rules: {
        /*inicioNome: (value) =>
          value.startsWith("TM-F") ||
          "O nome do Fólio necessita de começar com TM-F",
        umHifen: (value) =>
          value.split("-").length - 1 == 1 ||
          "O nome do Fólio não pode ter mais hífens",
      */},
      colecaoSel: ["C1", "C2","C3"],
      linguaSel: ["Português", "Inglês", "Espanhol"],
      editoraSel:["Porto Editora","Porto Editora 2","Porto Editora 3"],
      tipoSel:["Tipo1","Tipo2","Tipo3"]
    };
  },
  props: {
    folio: {
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
      (this.imageData= ""),
      (this.capa=null)
      },
    save() {
      this.$emit("atualizaElemento", this);
    },
    submeter() {
      this.skip = 1;
      //console.log(this.skip)
      this.$emit("submeterElemento", this);
    },
    previewImage: function(event) {
            // Reference to the DOM input element
            var input = event.target;
            // Ensure that you have a file before attempting to read it
            if (input.files && input.files[0]) {
                // create a new FileReader to read this image and convert to base64 format
                var reader = new FileReader();
                // Define a callback function to run, when FileReader finishes its job
                reader.onload = (e) => {
                    // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
                    // Read image as base64 and set to imageData
                    this.imageData = e.target.result;
                }
                // Start the reader job - read file as a data url (base64 format)
                reader.readAsDataURL(input.files[0]);
            }
        }

    /*
    atualizarInfo(){
      this.$emit('atualizarInfoPasso1','skip')
    }*/
  },
  computed: {
   /* disableButton() {
      if (
        this.idFolio.length > 1 &&
        this.versao &&
        this.tipo &&
        this.descricao.length > 0 &&
        this.sumario &&
        this.ficheiro
      )
        return false;
      else return true;
    },
  */},
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