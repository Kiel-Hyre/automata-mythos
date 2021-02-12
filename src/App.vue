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
              <v-btn
                style="background-color: rgba(0,0,0,0.08)"
                @click="execute"
                icon
              >
                <v-icon v-text="'fa-play'" size="16" class="ml-1" />
              </v-btn>
              <v-spacer></v-spacer>
            </div>
            <span class="text-body-2">Untitled.myth</span>
            <codemirror
              @cursorActivity="highlight"
              v-model="code"
              :options="cmOptions"
              ref="codemirror"
              class="text-body-2"
            />
            <v-sheet
              class="d-flex white--text px-3 py-1 text-body-2"
              color="rgb(78,78,78)"
            >
              <v-spacer></v-spacer>
              <span v-text="`Ln ${cmCursorPos.line}, Col ${cmCursorPos.ch}`" />

              <v-icon
                v-if="!executedOnce || loading"
                v-text="'fa-cog'"
                dark
                size="16"
                class="ml-3"
                :class="{ rotating: loading }"
              />

              <v-icon
                v-if="!loading && executedOnce && !errorCount"
                color="success"
                dark
                size="16"
                v-text="'fa-check-circle'"
                class="ml-3"
              />

              <span v-if="!loading && executedOnce && errorCount">
                <v-icon
                  color="error"
                  dark
                  size="16"
                  v-text="'fa-times-circle'"
                  class="ml-3"
                />
                <span
                  v-text="errorCount"
                  class="text-body-2 ml-1 red--text text--lighten-3"
                />
              </span>
            </v-sheet>
          </div>
        </v-col>
        <v-col cols="12" md="5">
          <v-simple-table height="400">
            <template #default>
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
              <tbody v-if="lexicalData.length">
                <tr
                  @click="showErrorLine(item.lineno, item.char_line)"
                  v-for="item in lexicalData"
                  :key="item.name"
                  class=" no-select"
                >
                  <td v-for="header in lexicalTableHeaders" :key="header.value">
                    <span
                      v-text="item[header.value]"
                      :class="{
                        'font-weight-bold': header.value === 'lineno'
                      }"
                    />
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <td :colspan="lexicalTableHeaders.length">
                  <div class="pa-5 text-body-1">
                    <div v-if="loading" class="d-flex justify-center">
                      Building ...
                    </div>
                    <div v-else class="d-flex justify-center">
                      <div v-if="!executedOnce">
                        <v-btn @click="execute" class="text-none">
                          <v-icon v-text="'fa-play'" size="12" class="mr-4" />
                          Run the analyzer
                        </v-btn>
                      </div>
                    </div>
                  </div>
                </td>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
      <div class="mt-5">
        <v-tabs
          v-model="selectedTab"
          background-color="grey lighten-4"
          active-class="elevation-3"
          class="rounded-t-lg"
          color="brown--text text--darken-1"
          hide-slider
        >
          <v-tab v-for="tab in tabs" :key="tab">
            <span v-text="tab" />
            <span v-if="errors[tab].length">
              <v-icon
                v-text="'fa-exclamation-triangle'"
                color="red"
                class="mx-3"
                size="16"
              />
              <span
                v-text="errors[tab].length"
                class="text-body-2 red--text text--lighten-3"
              />
            </span>
          </v-tab>
        </v-tabs>
        <v-card>
          <v-simple-table height="400">
            <template #default>
              <thead>
                <tr>
                  <th
                    v-for="header in analyzerTableHeaders"
                    :key="header.value"
                    class="font-weight-bold text-body-1 text--center"
                    :width="header.width"
                  >
                    <v-icon
                      v-if="header.value === 'icon'"
                      v-text="'fa-caret-down'"
                      class="mt-n1"
                    />
                    <span v-else v-text="header.text" />
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  @click="showErrorLine(item.line, item.char_line)"
                  v-for="item in errors[tabs[selectedTab]]"
                  :key="item.name"
                  class="no-select"
                >
                  <td
                    v-for="header in analyzerTableHeaders"
                    :key="header.value"
                    class="text-body-1 text--center"
                  >
                    <v-icon
                      v-if="header.value === 'icon'"
                      v-text="'fa-exclamation-triangle'"
                      color="red"
                      class="mt-n1"
                      size="16"
                    />

                    <span v-else v-text="item[header.value]" />
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
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
import "codemirror/addon/lint/lint";
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
      regex: /[-]?(?:\d+\.?\d*)/i,
      token: "number"
    },
    { regex: /\?\?.*/, token: "comment" },
    { regex: /[-+\/*%^=<>!]+/, token: "operator" },

    { regex: /[a-z\_0-9A-Z$]+[\w$]*/, token: "variable" }
  ],
  comment: [{ regex: /.*/, token: "comment" }],
  meta: { dontIndentStates: ["comment"], lineComment: "??" }
});

// ^(0$|[1-9][0-9]{0,8})(\.\d{1,5})?$
// ^(?=.{1,23}$)[_a-zA-Z][A-Za-z0-9_]*

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
        { text: "Ln", value: "lineno" },
        { text: "Lexeme", value: "value" },
        { text: "Token", value: "type" },
        { text: "Description", value: "description" }
      ],
      lexicalErrors: [],
      syntaxErrors: [],
      analyzerTableHeaders: [
        { text: "", value: "icon" },
        { text: "Ln", value: "line" },
        { text: "Col", value: "char_line" },
        {
          text: "Messages",
          value: "message",
          width: "80%",
          align: "center"
        }
      ],
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
        lint: true,
        extraKeys: {
          "Ctrl-S": function() {
            self.saveChanges();
          },
          "Ctrl-R": function() {
            self.execute();
          }
        }
      },
      cmCursorPos: {
        line: 1,
        ch: 0
      },
      executedOnce: false,
      errors: {
        lexical: [],
        syntax: []
      },
      tableData: {
        lexical: [],
        syntax: []
      },
      selectedTab: 0,
      tabs: ["lexical", "syntax"]
    };
  },
  computed: {
    errorCount() {
      const { lexical, syntax } = this.errors;
      return lexical.length + syntax.length;
    }
  },
  methods: {
    showErrorLine(line, ch) {
      this.$refs.codemirror.codemirror.focus();
      this.$refs.codemirror.codemirror.setCursor({
        line: line - 1,
        ch: ch - 1
      });
    },
    highlight(cursor) {
      const { ch, line } = cursor.getCursor();
      this.cmCursorPos = Object.assign({}, this.cmCursorPos, {
        ch,
        line: line + 1
      });
    },
    saveChanges() {
      localStorage.setItem("code", this.code);
      this.saved = true;
    },
    execute() {
      this.loading = true;
      this.lexicalData = [];
      setTimeout(async () => {
        const raw_data = this.code;
        const endpoint = "http://localhost:8000/lexxer/execute/";

        const response = await this.axios.post(endpoint, { raw_data });

        const { success, data = [], errors = [] } = response.data;

        this.loading = false;

        if (success) {
          this.lexicalData = [...data["lexical"]];
          this.tabs.forEach(tab => {
            this.errors[tab] = [];
          });
        } else {
          this.tabs.forEach(tab => {
            this.lexicalData = [];
            this.errors[tab] = errors.filter(error => error.code === tab);
          });
        }

        if (!this.executedOnce) this.executedOnce = true;
      }, 500);
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

.no-select {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  cursor: pointer;
}
</style>
