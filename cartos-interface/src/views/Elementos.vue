<template>
  <div id="elementos">
    <appHeader :ajuda="ajuda"></appHeader>
    <div v-if="this.$store.state.user.tipo === 'Admin'">
      <navDraw></navDraw>
    </div>
    <div v-else>
      <navDrawLeitor></navDrawLeitor>
    </div>
    <v-data-table
      id="tabelaElementos"
      :headers="headers"
      :items="elementos"
      :items-per-page="15"
      :sort-by="['id']"
      :search="search"
      multi-sort
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title
            ><b>{{ $t("fol.title") }}</b></v-toolbar-title
          >
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            :label="`${$t('navd.se')}`"
            single-line
            hide-details
            class="mr-5"
          ></v-text-field>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                v-if="$store.state.user.tipo === 'Admin'"
                link
                to="/admin/import"
                color="#2A3F54"
                dark
                v-on="{ ...tooltip }"
                class="mr-5"
              >
                <v-icon>mdi-text-box-plus</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("fol.insert") }}
            </span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                link
                color="#2A3F54"
                dark
                v-on="{ ...tooltip }"
                @click="printSection"
              >
                <v-icon>mdi-printer</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("fol.print") }}
            </span>
          </v-tooltip>

          <v-dialog persistent v-model="dialog" max-width="500px">
            <elementoForm
              :passedData="item"
              @emiteFecho="emiteFecho($event)"
            ></elementoForm>
          </v-dialog>

          <v-dialog persistent v-model="dialogEdit" max-width="800px">
            <elementoFormEditable
              :elemento="item"
              @emiteFecho="emiteFecho($event)"
            ></elementoFormEditable>
          </v-dialog>

        </v-toolbar>
      </template>
      <template v-slot:header.id="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.colecao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.editora="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.data_publicacao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.lingua="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.options="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.options="{ item }">
        <v-icon small class="mr-2" @click="viewItem(item)"> mdi-eye </v-icon>
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon
          v-if="$store.state.user.tipo === 'Admin'"
          small
          @click="
            deleteDialog = true;
            tempValue = item;
          "
        >
          mdi-trash-can
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="picDialog" width="800px">
      <v-card>
        <v-img v-bind:src="elementoPic" contain aspect-ratio="1.5" />
      </v-card>
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltip }">
          <v-btn
            color="#c9302c"
            dark
            @click="picDialog = false"
            v-on="{ ...tooltip }"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </template>
        <span>
          {{ $t("indForm.close") }}
        </span>
      </v-tooltip>
    </v-dialog>
    <v-dialog v-model="noPicDialog" width="500px">
      <v-card>
        <v-toolbar color="#2A3F54" dark>
          <h2>{{ $t("fol.title") }}</h2>
        </v-toolbar>
        <v-row>
          <v-col
            style="
              margin-left: 1cm;
              margin-right: 1cm;
              max-width: 20px;
              margin-top: 15px;
            "
          >
            <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
          </v-col>
          <v-col>
            <v-card-text>
              <h3>{{ $t("fol.noPicText") }}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="noPicDialog = false" v-on="{ ...tooltip }">
                <v-icon>mdi-exit-to-app</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("indForm.close") }}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialog" scrollable width="500" persistent>
       <v-card>
        <v-toolbar color="#2A3F54" dark>
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
                  deleteDialog = false;
                  deleteItem(tempValue);
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
import Header from "../components/header.vue";
import NavDraw from "../components/navDraw.vue";
import navDrawLeitor from "../components/navDrawLeitor.vue";
import ElementoForm from "../components/elementoForm.vue";
import ElementoFormEditable from "../components/elementoFormEditable.vue";

export default {
  data() {
    return {
      url: process.env.VUE_APP_URL,
      headers: [
       {
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
      search: "",
      ajuda: "elementos",
      ver: "ver",
      elementos: [],
      errors: [],
      elementoPic: "",
      dialog: false,
      dialogEdit: false,
      picDialog: false,
      noPicDialog: false,
      deleteDialog: false,
      tempValue: "",
      item: {},
    };
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogEdit(val) {
      val || this.closeEdit();
    }
  },
  components: {
    appHeader: Header,
    navDraw: NavDraw,
    navDrawLeitor: navDrawLeitor,
    elementoForm: ElementoForm,
    elementoFormEditable: ElementoFormEditable,
  },
  created() {
    this.getElementos();
  },
  methods: {
    getElementos(){
      axios
        .get(
          this.url+`/elementos/elementos?nome=${this.$store.state.user._id}`,
          {
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          console.log(response.data)
          this.elementos = response.data;
        })
        .catch((e) => {
          //console.log(e)
          this.errors.push(e);
        });
    },
    printSection() {
      this.$htmlToPaper("tabelaElementos");
    },
    viewItem(item) {
      this.item = item;
      this.dialog = true;
    },
    editItem(item) {
      this.item = item;
      this.dialogEdit = true;
    },
    close() {
      this.dialog = false;
      this.item = {};
    },
    closeEdit() {
      this.dialogEdit = false;
      this.item = {};
    },
    deleteItem(item) {
      const index = this.elementos.indexOf(item);
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/elementos/apagar/` +
            this.elementos[index].id +
            `?nome=${this.$store.state.user._id}`,
          {
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          this.elementos = response.data;
          this.tempValue = {};
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    emiteFecho: function () {
      this.dialog = false;
      this.dialogEdit = false;
      this.getElementos();
    },
    verElementoFoto: function (item) {
      const index = this.elementos.indexOf(item);
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/elementos/ver/${this.elementos[index].id}/foto`,
          {
            responseType: "arraybuffer",
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          var image = new Buffer(response.data, "binary").toString("base64");
          this.elementoPic = `data:${response.headers[
            "content-type"
          ].toLowerCase()};base64,${image}`;
          this.picDialog = true;
        })
        .catch((e) => {
          this.noPicDialog = true;
          this.errors.push(e);
        });
    },
  },
};
</script>
<style scoped>
@media print {
  body {
    overflow: auto;
    height: auto;
  }
  .page-break {
    display: block;
    page-break-before: always;
  }
}
/* .tommitable .v-data-table .table{ */
.v-data-table /deep/ th {
  background-color: #4b779e;
}
.v-data-table /deep/ tr {
  color: #73879C;
  font-size: 13px;
}
.v-data-table /deep/ tr:nth-child(even) {
  background-color: rgb(245, 245, 245);
}
#elementos * {
  box-sizing: border-box;
}
#elementos {
  margin: 20px auto;
  max-width: 1100px;
  margin-bottom: 80px;
}
label {
  color: white;
  padding: 8px;
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 15px;
}
b {
  font-size: 20px;
}
</style>
