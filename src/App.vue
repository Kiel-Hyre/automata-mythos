<template>
  <v-app>
    <input
      type="file"
      accept=".myth, .txt"
      ref="fileUpload"
      class="d-none"
      @change="uploadFile"
    />
    <v-container>
      <div class="mt-5 mb-10 text-center">
        <v-img
          :src="require('@/assets/logo - mythosv1.png')"
          class="mx-auto"
          width="300"
        />
        <span
          class="text-h6 text-uppercase brown--text text--darken-1 font-weight-bold"
          >Lexical and Syntax Analyzer</span
        >
      </div>
      <v-row>
        <v-col>
          <div>
            <v-sheet
              color="rgb(78,78,78)"
              class="d-flex align-center px-5 py-2 rounded-t-lg"
            >
              <v-tooltip top>
                <template #activator="{attrs, on}">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    style="background-color: rgba(0,0,0,0.08)"
                    @click="newCode"
                    class="text-none font-weight-bold mr-5"
                    color="white"
                    icon
                    small
                  >
                    <v-icon v-text="'far fa-file'" size="16" />
                  </v-btn>
                </template>
                New Code <kbd>[Ctrl + N]</kbd>
              </v-tooltip>

              <v-tooltip top>
                <template #activator="{attrs, on}">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    style="background-color: rgba(0,0,0,0.08)"
                    @click="open"
                    class="text-none font-weight-bold mr-5"
                    color="white"
                    icon
                    small
                  >
                    <v-icon v-text="'fa-file-import'" size="16" />
                  </v-btn>
                </template>
                Import .myth file <kbd>[Ctrl + O]</kbd>
              </v-tooltip>

              <v-tooltip top>
                <template #activator="{attrs, on}">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    style="background-color: rgba(0,0,0,0.08)"
                    @click="saveChanges"
                    class="text-none font-weight-bold mr-5"
                    color="white"
                    icon
                  >
                    <v-icon v-text="'fa-save'" size="16" />
                  </v-btn>
                </template>
                Save <kbd>[Ctrl + S]</kbd>
              </v-tooltip>

              <v-tooltip top>
                <template #activator="{attrs, on}">
                  <v-btn
                    v-on="on"
                    v-bind="attrs"
                    style="background-color: rgba(0,0,0,0.08)"
                    @click="showDownload = true"
                    class="text-none font-weight-bold mr-5"
                    color="white"
                    icon
                  >
                    <v-icon v-text="'fa-arrow-alt-circle-down'" size="16" />
                  </v-btn>
                </template>
                Download
              </v-tooltip>

              <v-tooltip top>
                <template #activator="{attrs, on}">
                  <v-btn
                    @click="showLexical = !showLexical"
                    v-on="on"
                    v-bind="attrs"
                    style="background-color: rgba(0,0,0,0.08)"
                    class="text-none font-weight-bold mr-5"
                    color="white"
                    icon
                  >
                    <v-icon v-text="'fa-table'" size="16" />
                  </v-btn>
                </template>
                Show Lexical
              </v-tooltip>
              <v-spacer></v-spacer>
              <v-btn
                @click="execute"
                class="text-none white--text font-weight-bold"
                color="orange darken-1"
                :loading="loading"
                small
              >
                Run (Ctrl + R)
              </v-btn>
            </v-sheet>
            <codemirror
              @cursorActivity="highlight"
              v-model="code"
              :options="cmOptions"
              ref="codemirror"
              class="text-body-2"
            />
            <v-sheet
              class="d-flex white--text px-3 py-1 text-body-2 rounded-b-lg"
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
        <v-col v-if="showLexical" cols="12" md="5">
          <v-simple-table height="480">
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
      <v-snackbar v-model="saved" timeout="1000" top close>
        <v-icon v-text="'fa-save'" size="18" left />
        Saved
      </v-snackbar>
      <v-dialog :value="showDownload" width="500" persistent>
        <v-card class="pa-8">
          <div>
            <span class="text-h5 font-weight-bold">
              Download Code
            </span>
            <p class="text-body-1 mt-3">
              Enter the filename below:
            </p>
            <v-text-field
              filled
              hide-details
              dense
              suffix=".myth"
              color="amber darken-2"
              v-model="downloadFileName"
              placeholder="Untitled"
            ></v-text-field>
            <div class="mt-5">
              <v-btn @click="download" color="success">
                <v-icon v-text="'fa-download'" size="14" left />
                Download
              </v-btn>
              <v-btn @click="closeDownloadModal" class="ml-3" text outlined>
                Cancel
              </v-btn>
            </div>
          </div>
        </v-card>
      </v-dialog>
    </v-container>
  </v-app>
</template>

<script>
import { codemirror, CodeMirror } from "vue-codemirror";
import { saveAs } from "file-saver";

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
      mythosFiles: null,
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
        tabSize: 2,
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
          "Ctrl-O": function() {
            self.open();
          },
          "Ctrl-R": function() {
            self.execute();
          },
          "Ctrl+N": function() {
            self.newCode;
          },
          Tab: function(cm) {
            cm.replaceSelection("  ", "end");
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
      tabs: ["lexical", "syntax"],
      showLexical: false,
      editName: false,
      showDownload: false,
      downloadFileName: ""
    };
  },
  computed: {
    errorCount() {
      const { lexical, syntax } = this.errors;
      return lexical.length + syntax.length;
    }
  },
  methods: {
    newCode() {
      this.code = "";
      this.saveChanges(false);
    },
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
    saveChanges(notif = true) {
      localStorage.setItem("code", this.code);
      if (notif) this.saved = true;
    },
    download() {
      const file = new File(
        [this.code],
        `${this.downloadFileName.trim() || "Untitled"}.myth`,
        {
          type: "text/plain;charset=utf-8"
        }
      );
      saveAs(file);
      this.saveChanges(false);
      this.closeDownloadModal();
    },
    closeDownloadModal() {
      this.showDownload = false;
      this.downloadFileName = "";
    },
    open() {
      this.$refs.fileUpload.click();
    },
    execute() {
      this.loading = true;
      this.lexicalData = [];
      setTimeout(async () => {
        const raw_data = this.code;
        const splittedData = raw_data
          .replaceAll("\n", " \n")
          .split("\n")
          .map(line => line.trim());
        const lines = splittedData.indexOf(splittedData.find(Boolean));

        const start_line = lines > 0 ? lines + 1 : 1;

        const endpoint = "http://localhost:8000/lexxer/execute/";

        const response = await this.axios.post(endpoint, {
          raw_data,
          start_line
        });

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
    },
    uploadFile() {
      this.lexicalData = [];
      this.tabs.forEach(tab => {
        this.errors[tab] = [];
      });
      this.executedOnce = false;
      const self = this;
      const fr = new FileReader();
      fr.onload = function() {
        self.code = fr.result;
        self.saveChanges(false);
      };
      fr.readAsText(self.$refs.fileUpload.files[0]);
    }
  },
  watch: {
    downloadFileName(val) {
      const patt = new RegExp(/[~"#%&*:<>?/\\{|}]+/g);
      const res = patt.test(val);
      this.$nextTick(() => {
        if (res)
          this.downloadFileName = this.downloadFileName.substring(
            0,
            val.length - 1
          );
      });
    }
  },
  filters: {
    truncate: function(value) {
      const [name, type] = value.split(".");
      if (name.length <= 24) return value;

      return `${name.substring(0, 24)}....${type}`;
    }
  },
  created() {
    this.code = localStorage.getItem("code") || "";
  }
};
</script>

<style>
.CodeMirror {
  height: 400px;
}
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
