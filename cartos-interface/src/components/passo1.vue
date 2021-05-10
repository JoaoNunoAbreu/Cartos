<template>
  <div>
    <v-sheet color="grey lighten-4" tile>
      <v-row class="fill-height ml-10" align="center" justify="center">
        <v-col class="text-left">
          <v-form ref="form" method="post" enctype="multipart/form-data">
            <v-container>
              <div class="p-container">
                <div class="child-right">
                  <v-text-field
                    :label="$t('p1.id')"
                    :maxlength="maxId"
                    :placeholder="$t('p1.string')"
                    v-model="id"
                    :rules="[
                      rules.inicioNome,
                      rules.tresDigitos,
                      rules.seiscar,
                      rules.idRepetidos,
                    ]"
                    required
                  >
                  </v-text-field>
                  <v-text-field
                        :label="$t('p1.tit')"
                        :placeholder="$t('p1.string')"
                        :maxlength="maxChars"
                        v-model="titulo"
                        @focus="show_titulo = 'block'; disableOthers('show_titulo')"
                        required
                  >
                  </v-text-field>
                  <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_titulo" class="inputChar" v-text="(maxChars - titulo.length)"></div>
                  
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
                        v-model="colecao"
                        @focus="show_colecao = 'block'; disableOthers('show_colecao')"
                      ></v-text-field>
                      <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_colecao"  class="inputChar" v-text="(maxChars - colecao.length)"></div>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.num')"
                        :placeholder="$t('p1.string')"
                        v-model="numero"
                        :maxlength="maxChars"
                        required
                        @focus="show_numero = 'block'; disableOthers('show_numero')"
                      ></v-text-field>
                      <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_numero"  class="inputChar" v-text="(maxChars - numero.length)"></div>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.serie')"
                        :placeholder="$t('p1.string')"
                        v-model="serie"
                        :maxlength="maxChars"
                        required
                        @focus="show_serie = 'block'; disableOthers('show_serie')"
                      ></v-text-field>
                      <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_serie"  class="inputChar" v-text="(maxChars - serie.length)"></div>
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
                        @input="disableDropdown('lingua')"
                        v-bind:label="$t('p1.lin')"
                      >
                      </v-select>
                      <v-text-field
                        v-else
                        :placeholder="$t('p1.string')"
                        :label="$t('p1.lin2')"
                        :maxlength="maxChars"
                        @input="handleInput('lingua')"
                        v-model="lingua"
                        @focus="show_lingua = 'block'; disableOthers('show_lingua')"
                      ></v-text-field>
                      <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_lingua"  class="inputChar" v-text="(maxChars - lingua.length)"></div>
                    </div>
                  </div>
                  <div class="p-container">
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.pag')"
                        :placeholder="$t('p1.inteiro')"
                        v-model="paginas"
                        :maxlength="maxNum"
                        required
                      ></v-text-field>
                    </div>
                    <div class="child">
                      <v-text-field
                        :label="$t('p1.size')"
                        :placeholder="$t('p1.string')"
                        v-model="size"
                        :maxlength="maxChars"
                        required
                        @focus="show_size = 'block'; disableOthers('show_size')"
                      ></v-text-field>
                      <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_size"  class="inputChar" v-text="(maxChars - size.length)"></div>
                    </div>
                  </div>
                </div>
                <div class="child-left">
                  <label>{{ $t("p1.foto") }}:</label>
                  <v-file-input
                    show-size
                    accept="image/jpg, image/jpeg, image/png,video/*"
                    :label="$t('p1.file')"
                    v-model="capa"
                    @change="previewImage"
                  >
                  </v-file-input>
                  <v-img :src="this.url" contain></v-img>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-text-field
                    :label="$t('p1.pers')"
                    :placeholder="$t('p1.string')"
                    v-model="personagens"
                    :maxlength="maxPersChars"
                    required
                    @focus="show_personagens = 'block'; disableOthers('show_personagens')"
                  ></v-text-field>
                  <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_personagens"  class="inputChar" v-text="(maxPersChars - personagens.length)"></div>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.estado')"
                    :placeholder="$t('p1.string')"
                    v-model="estado"
                    :maxlength="maxChars"
                    required
                    @focus="show_estado = 'block'; disableOthers('show_estado')"
                  ></v-text-field>
                  <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_estado"  class="inputChar" v-text="(maxChars - estado.length)"></div>
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
                    @input="disableDropdown('editora')"
                    v-bind:label="$t('p1.edi')"
                  >
                  </v-select>
                  <v-text-field
                    v-else
                    :label="$t('p1.edi2')"
                    :placeholder="$t('p1.string')"
                    :maxlength="maxChars"
                    @input="handleInput('editora')"
                    v-model="editora"
                    @focus="show_editora = 'block'; disableOthers('show_editora')"
                  ></v-text-field>
                  <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_editora"  class="inputChar" v-text="(maxChars - editora.length)"></div>
                </div>
                <div class="child">
                  <v-text-field
                    :label="$t('p1.dataP')"
                    v-model="dataPub"
                    :placeholder="$t('p1.data')"
                    :maxlength="maxChars"
                    :rules="[rules.dataRule]"
                    required
                  ></v-text-field>
                </div>
              </div>
              <div class="p-container">
                <div class="child">
                  <v-row align="center">
                    <v-file-input
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
                    v-model="tipo"
                    @focus="show_tipo = 'block'; disableOthers('show_tipo')"
                  ></v-text-field>
                  <div :style="'padding-top: -22px; margin-top: -22px; display: ' + show_tipo" class="inputChar" v-text="(maxChars - tipo.length)"></div>
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
                    <v-btn @click="bimport()" class="mr-5" v-on="{ ...tooltip }"
                      ><v-icon>mdi-exit-to-app</v-icon></v-btn
                    >
                  </template>
                  <span>
                    {{ $t("p1.imp") }}
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
    <v-dialog v-model="submitDialog" scrollable width="500">
      <infoPopup @emiteFecho="emiteFecho($event)"></infoPopup>
    </v-dialog>
    <v-dialog
      persistent
      v-model="dialogImp"
      @keydown.esc="dialogImp = false"
      scrollable
      width="500"
    >
      <v-card class="mx-auto">
        <v-toolbar color="#2A3F54" dark>
          <h3 class="mx-auto">{{ $t("navd.importAjuda") }}</h3>
        </v-toolbar>
        <v-divider class="mx-4" horizontal></v-divider>
        <div class="mx-auto" style="width: 200px">
          <v-select
            class="change-font"
            required
            v-model="idImport"
            :items="elemImport"
            v-bind:label="$t('p1.id')"
          >
          </v-select>
        </div>
        <v-card class="mx-auto" outlined color="transparent">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                ref="submit"
                class="orange white--text mr-4 mb-3"
                @click="saveImp()"
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
                class="white--text mb-3"
                color="#26B99A"
                @click="dialogImp = false"
                v-on="{ ...tooltip }"
              >
                <v-icon>mdi-door-open</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("nav.Sair") }}</span>
          </v-tooltip>
        </v-card>
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
      url: process.env.VUE_APP_URL,
      dialog: false,
      counterCol: 0,
      counterEditora: 0,
      counterTipo: 0,
      counterLingua: 0,
      elemImport: [],
      show_titulo: "none",
      show_colecao: "none",
      show_numero: "none",
      show_serie: "none",
      show_lingua: "none",
      show_size: "none",
      show_personagens: "none",
      show_estado: "none",
      show_editora: "none",
      show_tipo: "none",
      rules: {
        inicioNome: (value) =>
          value.startsWith("RPT") ||
          "O nome do Elemento necessita de começar com RPT",
        tresDigitos: (value) =>
          value.replace(/[^0-9]/g, "").length == 3 ||
          "O nome do Elemento tem de ter 3 dígitos",
        idRepetidos: (value) =>
          !this.elemImport.includes(value) || "Identificador já está a ser utilizado",
        seiscar: (value) =>
          value.length == 6 || "O nome do Elemento tem de ter 6 caracteres",
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
      maxNum: 3,
      maxPersChars: 100
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
    this.capa = this.elemento.capa;

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
        }),
      //Elementos
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/elementos/elementos?nome=${this.$store.state.user._id}`,
          {
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          for (let i = 0; i < response.data.length; i++)
            this.elemImport.push(response.data[i].id);

          console.log(this.elemImport);
        })
        .catch((e) => {
          this.errors.push(e);
        });
  },
  methods: {
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
        (this.capa = null);
    },
    save() {
      this.$emit("atualizaElemento", this);
    },
    bimport() {
      this.dialogImp = true;
    },
    submeter() {
      this.skip = 1;
      this.$emit("submeterElemento", this);
    },
    previewImage: function () {
      this.url = URL.createObjectURL(this.capa);
    },
    disableOthers(show){
      if(show != "show_titulo") this.show_titulo = "none";
      if(show != "show_colecao") this.show_colecao = "none"
      if(show != "show_numero") this.show_numero = "none"
      if(show != "show_serie") this.show_serie = "none"
      if(show != "show_lingua") this.show_lingua = "none"
      if(show != "show_size") this.show_size = "none"
      if(show != "show_personagens") this.show_personagens = "none"
      if(show != "show_estado") this.show_estado = "none"
      if(show != "show_editora") this.show_editora = "none"
      if(show != "show_tipo") this.show_tipo = "none"
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
    emiteFecho: function () {
      this.submitDialog = false;
    },
    saveImp() {
      axios
        .get(this.url + "/elementos/" + this.idImport, {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          let elementoImportado = response.data[0];
          this.id = elementoImportado.id;
          this.titulo = elementoImportado.titulo;
          this.colecao = elementoImportado.colecao;
          this.numero = elementoImportado.numero;
          this.serie = elementoImportado.serie;
          this.lingua = elementoImportado.lingua;
          this.paginas = elementoImportado.nr_paginas;
          this.size = elementoImportado.tamanho;
          this.personagens = elementoImportado.personagens;
          this.estado = elementoImportado.estado;
          this.editora = elementoImportado.editora;
          this.dataPub = elementoImportado.data_publicacao;
          this.ficheiro = elementoImportado.ficheiro;
          this.tipo = elementoImportado.tipo;
          this.capa = elementoImportado.capa;

          this.dialogImp = false;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
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
        this.tipo
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