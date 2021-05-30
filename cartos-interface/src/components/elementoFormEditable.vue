<template>
  <div>
    <v-sheet color="grey lighten-4" tile>
      <v-row class="fill-height ml-10" align="center" justify="center">
        <v-col class="text-left">
          <v-form ref="form" method="post" enctype="multipart/form-data" v-model="valid" lazy-validation>
            <v-container>
              <div class="p-container">
                <div class="child-right">
                  <v-text-field
                    :label="$t('p1.id')"
                    :maxlength="maxId"
                    :counter="maxId"
                    :placeholder="$t('p1.string')"
                    v-model="id"
                    :disabled="true"
                  >
                  </v-text-field>
                  <v-text-field
                    :label="$t('p1.tit')"
                    :placeholder="$t('p1.string')"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    v-model="titulo"
                    required
                  >
                  </v-text-field>
                  <div class="p-container">
                    <div class="child">
                      <v-select
                        class="change-font"
                        v-if="
                          colecao !== 'Outra' &&
                          (counterCol == 0 || counterCol == 2)
                        "
                        required
                        v-model="colecao"
                        :items="colecaoSel"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        @input="disableDropdown('col')"
                        v-bind:label="$t('p1.col')"
                      >
                      </v-select>
                      <v-text-field
                        v-else
                        :label="$t('p1.col2')"
                        :placeholder="$t('p1.string')"
                        @input="handleInput('col')"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        v-model="colecao"
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.num')"
                        :placeholder="$t('p1.string')"
                        v-model="numero"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        required
                      ></v-text-field>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.serie')"
                        :placeholder="$t('p1.string')"
                        v-model="serie"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        required
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-select
                        class="change-font"
                        v-if="
                          lingua !== 'Outra' &&
                          (counterLingua == 0 || counterLingua == 2)
                        "
                        required
                        v-model="lingua"
                        :items="linguaSel"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        @input="disableDropdown('lingua')"
                        v-bind:label="$t('p1.lin')"
                      >
                      </v-select>
                      <v-text-field
                        v-else
                        :placeholder="$t('p1.string')"
                        :label="$t('p1.lin2')"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        @input="handleInput('lingua')"
                        v-model="lingua"
                      ></v-text-field>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.pag')"
                        :placeholder="$t('p1.inteiro')"
                        v-model="paginas"
                        :maxlength="maxNum"
                        :counter="maxNum"
                        :disabled="isDisabled"
                        required
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.size')"
                        :placeholder="$t('p1.string')"
                        v-model="size"
                        :maxlength="maxChars"
                        :counter="maxChars"
                        :disabled="isDisabled"
                        required
                      ></v-text-field>
                    </div>
                  </div>
                </div>
                <div class="child-left">
                  <label v-if="hasCapa===true" >{{ $t("p1.capa") }}:</label>
                  <!--
                  <v-file-input
                    :disabled="isDisabled"
                    show-size
                    accept="image/jpg, image/jpeg, image/png,video/*"
                    :label="$t('p1.file')"
                    v-model="capa"
                    @change="previewImage"
                  >
                  </v-file-input>
                  <v-img :src="this.url" contain></v-img>
                  -->
                  <v-img v-if="hasCapa===true" v-bind:src="capa" contain max-width="100" />
                  <label v-if="hasVideo===true">{{ $t("p1.Video") }}:</label>
                  <div>
                    <video v-if="hasVideo===true" width="200" :src="video" controls contain></video>
                  </div>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-text-field
                    :label="$t('p1.pers')"
                    :placeholder="$t('p1.string')"
                    v-model="personagens"
                    :maxlength="maxPersChars"
                    :counter="maxPersChars"
                    :disabled="isDisabled"
                    required
                  ></v-text-field>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.estado')"
                    :placeholder="$t('p1.string')"
                    v-model="estado"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    required
                  ></v-text-field>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-select
                    class="change-font"
                    v-if="
                      editora !== 'Outra' &&
                      (counterEditora == 0 || counterEditora == 2)
                    "
                    required
                    v-model="editora"
                    :items="editoraSel"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    @input="disableDropdown('editora')"
                    v-bind:label="$t('p1.edi')"
                  >
                  </v-select>
                  <v-text-field
                    v-else
                    :label="$t('p1.edi2')"
                    :placeholder="$t('p1.string')"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    @input="handleInput('editora')"
                    v-model="editora"
                  ></v-text-field>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.dataP')"
                    v-model="dataPub"
                    :placeholder="$t('p1.data')"
                    :maxlength="maxDate"
                    :counter="maxDate"
                    :disabled="isDisabled"
                    :rules="[rules.dataRule]"
                    required
                  ></v-text-field>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-row align="center">
                    <v-file-input
                      :disabled="isDisabled"
                      show-size
                      type="file"
                      :label="$t('p1.file')"
                      accept="application/pdf"
                      placeholder="pdf"
                      v-model="ficheiro"
                    ></v-file-input>
                  </v-row>
                </div>
                <div class="child">
                  <v-select
                    class="change-font"
                    v-if="
                      tipo !== 'Outra' && (counterTipo == 0 || counterTipo == 2)
                    "
                    required
                    v-model="tipo"
                    :items="tipoSel"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    @input="disableDropdown('tipo')"
                    v-bind:label="$t('p1.tipo')"
                  >
                  </v-select>
                  <v-text-field
                    v-else
                    :label="$t('p1.tipo2')"
                    :placeholder="$t('p1.string')"
                    @input="handleInput('tipo')"
                    :maxlength="maxChars"
                    :counter="maxChars"
                    :disabled="isDisabled"
                    v-model="tipo"
                  ></v-text-field>
                </div>
              </div>
            </v-container>
            <v-container style="width: 750px">
              <v-toolbar flat color="grey lighten-4">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      v-if="!isDisabled"
                      ref="submit"
                      class="orange white--text mr-3"
                      :disabled="disableButton"
                      @click="
                        save();
                        submitDialog = true;
                      "
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
                      v-if="!isDisabled"
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
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      v-if="!isDisabled"
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
                
                <!-- DELETE FROM DB -->

                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      v-if="isDeleting"
                      @click="deleteDialog = true;"
                      v-on="{ ...tooltip }"
                      color="#cc0000"
                      class="white--text mr-3" >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <span>
                    {{ $t("p1.apagar") }}
                  </span>
                </v-tooltip>

                <v-dialog
                  @keydown.esc="dialog = false"
                  v-model="dialog"
                  scrollable
                  width="500"
                >
                  <v-card>
                    <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
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
                      :to="backTo"
                      v-on="{ ...tooltip }"
                      color="#26B99A"
                      class="white--text mr-3"
                      @click="emiteFecho($event)"
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
    <v-dialog v-model="submitDialog" scrollable width="500">
      <infoPopup @emiteFecho="emiteFecho($event)"></infoPopup>
    </v-dialog>
    <v-dialog v-model="deleteDialog" scrollable width="500" persistent>
       <v-card>
        <v-toolbar style="background: linear-gradient(to top, #376a53 0%, #549d7c 100%);" dark>
          <h2>{{ $t("fol.conf") }}</h2>
        </v-toolbar>
        <v-row>
          <v-col
            style="
              margin-left: 1cm;
              margin-right: 1cm;
              max-width: 40px;
              margin-top: 20px;
            "
          >
            <v-icon x-large color="#3399ff" dark>mdi-help-circle</v-icon>
          </v-col>
          <v-col>
            <v-card-text>
              <h3>{{ $t("fol.elim") }}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                @click="
                  deleteItem();
                  deleteDialog = false;
                  emiteFecho($event);
                "
                v-on="{ ...tooltip }"
                color="#cc0000"
                class="white--text mr-3" >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("navd.confirm") }}
            </span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="deleteDialog = false" v-on="{ ...tooltip }" color="#26B99A"
                      class="white--text mr-3"  >
                <v-icon>mdi-door-open</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("navd.nao") }}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import axios from "axios";
import infoPopup from "../components/InfoPopup";
export default {
  data() {
    return {
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
      ficheiro: null,
      tipo: "",
      capa: null,
      video: null,
      url: process.env.VUE_APP_URL,
      dialog: false,
      counterCol: 0,
      counterEditora: 0,
      counterTipo: 0,
      counterLingua: 0,
      elemImport: [],
      valid: true,
      rules: {
        dataRule: (value) => {
          const pattern = /^((0)[1-9]|[1-2][0-9]|(3)[0-1])(\/)(((0)[1-9])|((1)[0-2]))(\/)\d{4}$/;
          return (
            pattern.test(value) || "A data deve ter o formato : DD/MM/AAAA"
          );
        },
      },
      colecaoSel: [],
      linguaSel: [],
      editoraSel: [],
      tipoSel: [],
      submitDialog: false,
      dialogImp: false,
      idImport: "",
      maxId: 6,
      maxChars: 20,
      maxDate: 10,
      maxNum: 3,
      maxPersChars: 100,
      deleteDialog: false,
      hasVideo: false,
      hasCapa: false
    };
  },
  props: {
    elemento: {
      type: Object,
    },
    isDisabled: {
      type: Boolean,
    },
    isDeleting: {
      type: Boolean,
    },
    backTo: {
      type: String,
    }
  },
  watch: {
    elemento: {
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    },
    isDisabled: {
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    },
    isDeleting: {
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    },
    backTo: {
      immediate: true,
      deep: true,
      handler() {
        this.onUpdate();
      },
    }
  },
  created() {
    
    axios
      .get(this.url + `/elementos/editoras`, {
        headers: {
          Authorization: `Bearer: ${this.$store.state.jwt}`,
        },
      })
      .then((response) => {
        for (let i = 0; i < response.data.length; i++)
          this.editoraSel.push(response.data[i].x.designacao);
        this.editoraSel.push("Outra");
      })
      .catch((e) => {
        this.errors.push(e);
      }),
      axios
        .get(this.url + `/elementos/colecoes`, {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          for (let i = 0; i < response.data.length; i++)
            this.colecaoSel.push(response.data[i].x.designacao);
          this.colecaoSel.push("Outra");
        })
        .catch((e) => {
          this.errors.push(e);
        }),
      axios
        .get(this.url + `/elementos/linguas`, {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          for (let i = 0; i < response.data.length; i++)
            this.linguaSel.push(response.data[i].x.designacao);
          this.linguaSel.push("Outra");
        })
        .catch((e) => {
          this.errors.push(e);
        }),
      axios
        .get(this.url + `/elementos/tipos`, {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          for (let i = 0; i < response.data.length; i++)
            this.tipoSel.push(response.data[i].x.designacao);
          this.tipoSel.push("Outra");
        })
        .catch((e) => {
          this.errors.push(e);
        })
  },
  methods: {
    onUpdate() {
      this.hasVideo=false;
      this.hasCapa=false;
      console.log("   UPDATE    ")
      this.video=null;
      this.id = this.elemento.id;
      this.titulo = this.elemento.titulo;
      this.colecao = this.elemento.colecao;
      this.numero = this.elemento.numero;
      this.serie = this.elemento.serie;
      this.lingua = this.elemento.lingua;
      this.paginas = this.elemento.nr_paginas;
      this.size = this.elemento.tamanho;
      this.personagens = this.elemento.personagens;
      this.estado = this.elemento.estado;
      this.editora = this.elemento.editora;
      this.dataPub = this.elemento.data_publicacao;
      this.tipo = this.elemento.tipo;
      this.getCapa(this.elemento.id);
      this.getVideo(this.elemento.id);
      
    },
    reset() {
      //needs work for more resets
      this.$refs.form.reset();
      (this.id = ""),
        (this.titulo = ""),
        (this.colecao = ""),
        (this.numero = ""),
        (this.serie = ""),
        (this.lingua = ""),
        (this.paginas = ""),
        (this.size = ""),
        (this.personagens = ""),
        (this.estado = ""),
        (this.editora = ""),
        (this.dataPub = ""),
        (this.ficheiro = null),
        (this.tipo = ""),
        (this.capa = null),
        (this.video = null);
    },
    save() {
      let formData = new FormData();
      formData.append("id", this.id);
      formData.append("titulo", this.titulo);
      formData.append("colecao", this.colecao);
      formData.append("numero", this.numero);
      formData.append("serie", this.serie);
      formData.append("lingua", this.lingua);
      formData.append("paginas", this.paginas);
      formData.append("size", this.size);
      formData.append("personagens", this.personagens);
      formData.append("estado", this.estado);
      formData.append("editora", this.editora);
      formData.append("dataPub", this.dataPub);
      formData.append("ficheiro", this.ficheiro);
      formData.append("capa", this.capa);
      formData.append("video", this.video);
      formData.append("tipo", this.tipo);

      axios
        .post(
          this.url + `/import/editElement/?nome=${this.$store.state.user._id}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then(() => {
          this.model = 0;
          this.$router.push({ path: this.backTo });
        })
        .catch((e) => {
          //console.log("ERRO = " + e);
          this.errors.push(e);
        });
    },
    disableDropdown(tipo) {
      if (tipo == "col") {
        if (this.colecao == "Outra") {
          this.counterCol = 1;
          this.colecao = "";
        }
      }
      
      if (tipo == "editora") {
        if (this.editora == "Outra") {
          this.counterEditora = 1;
          this.editora = "";
        }
      }

      if (tipo == "tipo") {
        if (this.tipo == "Outra") {
          this.counterTipo = 1;
          this.tipo = "";
        }
      }

      if (tipo == "lingua") {
        if (this.lingua == "Outra") {
          this.counterLingua = 1;
          this.lingua = "";
        }
      }
    },
    handleInput(tipo) {
      if (tipo == "col") {
        if (this.colecao.length == 0) {
          this.counterCol++;
        }
      }

      if (tipo == "editora") {
        if (this.editora.length == 0) {
          this.counterEditora++;
        }
      }

      if (tipo == "tipo") {
        if (this.tipo.length == 0) {
          this.counterTipo++;
        }
      }

      if (tipo == "lingua") {
        if (this.lingua.length == 0) {
          this.counterLingua++;
        }
      }
    },
    emiteFecho: function() {
      this.$emit("emiteFecho");
    },
    deleteItem() {
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/elementos/apagar/` +
            this.id +
            `?nome=${this.$store.state.user._id}`,
          {
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then(() => {
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    getCapa(id){
      console.log("hascapa :  "+ this.hasCapa)
      axios
        .get(this.url + `/elementos/ver/${id}/foto`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          this.hasCapa=true;
          var image = new Buffer(response.data, "binary").toString("base64");
          this.capa = `data:${response.headers[
            "content-type"
          ].toLowerCase()};base64,${image}`;
          //console.log("resoponse:" + image)
        })
        .catch((err) => {
          //console.log("resoponse:" + err)
          this.hasCapa=false;
          this.error = err.message;
        })
    },
    getVideo(id){
       console.log("video :"+this.hasVideo)
      axios
        .get(this.url + `/elementos/ver/${id}/video`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          this.hasVideo=true;
          var vi = new Buffer(response.data, "binary").toString("base64");
          this.video = `data:${response.headers[
            "content-type"
          ].toLowerCase()};base64,${vi}`;
        })
        .catch((err) => {
          this.hasVideo=false;
         
          this.error = err.message;
        });
    }
  },
  computed: {
    disableButton() {
      if (
        this.id.length > 1 &&
        this.titulo.length > 0 &&
        this.colecao &&
        this.numero.length > 0 &&
        this.serie.length > 0 &&
        this.lingua &&
        this.paginas.length > 0 &&
        this.size.length > 0 &&
        this.personagens.length > 0 &&
        this.estado.length > 0 &&
        this.editora &&
        this.dataPub.length > 0 &&
        this.ficheiro &&
        this.tipo &&
        this.valid
      )
        return false;
      else return true;
    },
  },
  components: {
    infoPopup: infoPopup,
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
.child-right {
  width: 1000px;
  float: right;
}
.child-left {
  width: 50%;
  margin-left: 50px;
  float: right;
}

.file-upload-form,
.image-preview {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  padding: 20px;
}
img.preview {
  width: 200px;
  background-color: white;
  border: 1px solid #ddd;
  padding: 5px;
}
</style>