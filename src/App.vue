<template>
  <v-app>
    <v-container>
      <div class="mt-5 mb-10 text-center">
        <v-img
          :src="require('@/assets/logo - mythosv1.png')"
          class="mx-auto"
          width="350"
        />
        <span
          class="text-h5 text-uppercase brown--text text--darken-1 font-weight-bold"
          >Lexical and Syntax Analyzer</span
        >
      </div>
      <v-row>
        <v-col cols="12" md="7" class="pr-10">
          <div>
            <div class="mb-5 d-flex">
              <v-spacer></v-spacer>
              <v-btn
                style="background-color: rgba(0,0,0,0.08)"
                @click="execute"
                icon
              >
                <v-icon v-text="'fa-play'" size="16" class="ml-1" />
              </v-btn>
            </div>
            <v-sheet color="#2d2d2d" class="py-3">
              <codemirror
                v-model="code"
                class="text-body-2"
                :options="cmOptions"
              />
            </v-sheet>
          </div>
        </v-col>
        <v-col cols="12" md="5">
          <v-simple-table height="400">
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
      <div>
        {{ lexicalErrors }}
      </div>
      <v-snackbar v-model="saved" timeout="3000" top right close
        >Saved</v-snackbar
      >
    </v-container>
  </v-app>
</template>

<script>
import { codemirror, CodeMirror } from "vue-codemirror";
require("codemirror/addon/mode/simple.js");

import "codemirror/lib/codemirror.css";
import "codemirror/theme/mbo.css";
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

CodeMirror.defineSimpleMode("mythos", {
  start: [
    { regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string" },
    { regex: /(QUEST)(\s+)([a-z\_0-9A-Z$][\w$]*)/, token: "variable-2" },
    {
      regex: /(?:AND|BESTOW|CHEST|CHOP|CHRONO|DAY|ECHO|FATE|FUTURE|GOLD|HEAD|HERMES|HYDRA|IN|NOT|OFFER|OLYMPUS|OR|PANDORA|PAST|PROPHECY|QUEST|RETRIAL|REWARD|SILVER|SKIP|SLAIN|SONG|STOP|TRIAL|VERDICT)\b/,
      token: "keyword"
    },
    { regex: /BLESSED|CURSED|NONE/, token: "atom" },
    {
      regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
      token: "number"
    },
    { regex: /\?\?.*/, token: "comment" },
    { regex: /[-+\/*%^=<>!]+/, token: "operator" },

    { regex: /[a-z\_0-9A-Z$]+[\w$]*/, token: "variable" }
  ],
  comment: [{ regex: /.*/, token: "comment" }],
  meta: { dontIndentStates: ["comment"], lineComment: "??" }
});

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
        theme: "mbo",
        mode: "mythos",
        lineNumbers: true,
        line: true,
        autofocus: true,
        lineWiseCopyCut: true,
        autoCloseBrackets: {
          pairs: '(){}[]||""',
          explode: "[]{}()"
        },
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
          "Ctrl-R": function() {
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
      const endpoint = "http://localhost:8000/lexxer/execute/";

      const response = await this.axios.post(endpoint, { raw_data });

      const { success, data = [], errors = [] } = response.data;
      const { lex_errors = [] } = errors;

      this.loading = false;

      if (success) {
        this.lexicalData = [...data];
        this.lexicalErrors = [];
      } else {
        this.lexicalData = [];
        this.lexicalErrors = [...lex_errors];
      }
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
