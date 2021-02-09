<template>
  <v-app>
    <v-container>
      <div class="my-10">
        <v-img
          :src="require('@/assets/mythos.png')"
          class="mx-auto"
          width="300"
        />
      </div>
      <v-row>
        <v-col cols="7">
          <div>
            <div class="mt-10 mb-5">
              <span
                >Press <kbd dark>alt + ctrl + s</kbd> to save,
                <kbd dark>alt + ctrl + r</kbd> to run</span
              >
            </div>
            <v-sheet color="#2d2d2d" class="py-3">
              <codemirror
                v-model="code"
                @keydown.ctrl.83.prevent="saveChanges"
                @keydown.ctrl.82.prevent="execute"
                :options="cmOptions"
                placeholder="Write your own story ..."
              />
            </v-sheet>

            <v-btn @click="execute" class="success text-none mt-10" large>
              <v-icon
                v-text="'fa-cog'"
                size="20"
                :class="{ rotating: loading }"
                left
              />
              Execute
            </v-btn>
            <div v-if="stringifyCode" class="my-10 pa-5 rounded-lg">
              <p
                class="mb-0"
                v-text="stringifyCode"
                style="font-family: 'Fira Mono'"
              />
            </div>
          </div>
        </v-col>
        <v-col>
          <v-alert v-if="lexicalErrors.length" type="error">
            {{ lexicalErrors[0] }}
          </v-alert>
          <v-simple-table v-else height="500">
            <template v-slot:default>
              <thead>
                <tr>
                  <th
                    v-for="header in lexicalTableHeaders"
                    :key="header.value"
                    class="font-weight-bold text-body-1"
                  >
                    <span v-text="header.text" />
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in lexicalData" :key="item.name">
                  <td v-for="header in lexicalTableHeaders" :key="header.value">
                    <span v-text="item[header.value]" />
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
      <v-snackbar v-model="saved" timeout="3000" top right close
        >Saved</v-snackbar
      >
    </v-container>
  </v-app>
</template>

<script>
import { codemirror } from "vue-codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/monokai.css";
import "codemirror/addon/display/fullscreen.css";
import "codemirror/addon/scroll/simplescrollbars.css";

import "codemirror/addon/edit/matchbrackets";
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/selection/active-line";
import "codemirror/addon/display/fullscreen";
import "codemirror/addon/search/searchcursor";
import "codemirror/addon/search/search";
import "codemirror/addon/scroll/simplescrollbars";
import "codemirror/addon/display/placeholder";

// import "codemirror/addon/";

export default {
  components: {
    codemirror
  },
  data() {
    const self = this;
    return {
      code: "",
      stringifyCode: "",
      loading: false,
      saved: false,
      lexicalData: [],
      lexicalTableHeaders: [
        { text: "Lexeme", value: "value" },
        { text: "Token", value: "title" },
        { text: "Description", value: "description" },
        { text: "Ln", value: "line" }
      ],
      lexicalErrors: [],
      cmOptions: {
        tabSize: 2,
        theme: "monokai",
        lineNumbers: true,
        line: true,
        autofocus: true,
        lineWiseCopyCut: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        styleActiveLine: true,
        scrollbarStyle: "overlay",
        extraKeys: {
          F11: function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
          },
          Esc: function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
          },
          "Ctrl-S": function() {
            self.saveChanges();
          },
          "Ctrl-R": function(cm) {
            self.execute();
          }
        }
      }
    };
  },
  methods: {
    highlight(code) {
      return code;
    },
    saveChanges() {
      localStorage.setItem("code", this.code);
      this.saved = true;
    },
    async execute() {
      const raw_data = JSON.stringify([
        ...this.code.replaceAll("\n", " \n").split("\n")
      ]);

      this.loading = true;

      const response = await this.axios.post(
        "http://localhost:8000/lexxer/execute/",
        {
          raw_data
        }
      );

      const { success, data = [], errors = [] } = response["data"];

      this.loading = false;

      if (success) {
        this.stringifyCode = raw_data;
        this.lexicalData = [...data];
        this.lexicalErrors = [];
      } else this.lexicalErrors = [...errors];
    }
  },

  created() {
    this.code = localStorage.getItem("code") || "";
  }
};
</script>

<style>
@-webkit-keyframes rotating /* Safari and Chrome */ {
  from {
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes rotating {
  from {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  to {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
.rotating {
  -webkit-animation: rotating 2s linear infinite;
  -moz-animation: rotating 2s linear infinite;
  -ms-animation: rotating 2s linear infinite;
  -o-animation: rotating 2s linear infinite;
  animation: rotating 2s linear infinite;
}
</style>
