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

export default {
  components: {
    codemirror
  },
  data() {
    const self = this;
    return {
      toolbarItems: {
        file: {
          items: [
            { name: "New myth", action: this.newCode },
            {
              name: "Open myth",
              shortcut: "Ctrl + O",
              action: this.open
            },
            { name: "Save", shortcut: "Ctrl + S", action: this.saveChanges },
            { name: "Download", action: this.askFileName }
          ]
        },
        run: {
          items: [
            { name: "Run", shortcut: "Ctrl + R", action: this.execute },
            { name: "Toggle Lexical Table", action: this.toggleLexical }
          ]
        }
      },
      code: localStorage.getItem("code") || "",
      loading: false,
      saved: false,
      lexicalData: [],
      lexicalTableHeaders: [
        { text: "Ln", value: "lineno" },
        { text: "Lexeme", value: "value" },
        { text: "Token", value: "type" },
        { text: "Description", value: "description" }
      ],
      analyzerTableHeaders: [
        { text: "", value: "icon" },
        { text: "Ln", value: "line" },
        { text: "Col", value: "char_line" },
        { text: "Code", value: "code" },
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

      showLexical: localStorage.getItem("showLexical") === "true",
      showDownload: false,
      downloadFileName: "",
      filename: localStorage.getItem("name") || "Untitled",
      errors: [],
      cacheCode: localStorage.getItem("code")
    };
  },
  computed: {
    errorCount() {
      return this.errors.length;
    },
    filenameWithType() {
      return `${this.filename}.myth`;
    },
    hasChanges() {
      return this.cacheCode !== this.code;
    }
  },
  methods: {
    toggleLexical() {
      this.showLexical = !this.showLexical;
      localStorage.setItem("showLexical", this.showLexical);
    },
    resetTables() {
      this.errors = [];
      this.lexical = [];
      this.executedOnce = false;
      this.$refs.codemirror.codemirror.clearHistory();
    },
    newCode() {
      this.$refs.codemirror.codemirror.setValue("");
      this.resetTables();
      this.filename = "Untitled";
      localStorage.setItem("name", this.filename);
      this.cacheCode = "";
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
      this.cacheCode = this.code;
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
    askFileName() {
      this.downloadFileName = this.filename;
      this.showDownload = true;
    },
    closeDownloadModal() {
      this.showDownload = false;
      this.downloadFileName = this.filename;
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
          this.errors = [];
        } else {
          this.lexicalData = [];
          this.errors = [...errors];
        }

        if (!this.executedOnce) this.executedOnce = true;
      }, 500);
    },
    uploadFile() {
      const files = this.$refs.fileUpload.files[0];
      const splitFileName = files.name.split(".");
      const name = splitFileName.slice(0, splitFileName.length - 1).join(".");
      const type = splitFileName[splitFileName.length - 1];

      if (type !== "myth") return;

      this.filename = name;
      localStorage.setItem("name", name);

      const self = this;
      const fr = new FileReader();
      fr.onload = function() {
        self.$refs.codemirror.codemirror.setValue(fr.result);
        self.cacheCode = fr.result;
        self.resetTables();
        self.saveChanges(false);
      };
      fr.readAsText(self.$refs.fileUpload.files[0]);
    },
    _keyListener(e) {
      if (e.key === "s" && (e.ctrlKey || e.metaKey)) {
        this.saveChanges();
        e.preventDefault();
      }
      if (e.key === "o" && (e.ctrlKey || e.metaKey)) {
        this.open();
        e.preventDefault();
      }
      if (e.key === "r" && (e.ctrlKey || e.metaKey)) {
        this.execute();
        e.preventDefault();
      }
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
  mounted() {
    window.addEventListener("keydown", this._keyListener);
    this.$refs.codemirror.codemirror.clearHistory();
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this._keyListener);
  }
};
