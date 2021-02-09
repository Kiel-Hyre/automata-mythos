<template>
  <div>
    <v-app>
      <v-container>
        <div class="my-10">
          <v-img
            :src="require('@/assets/mythos.png')"
            class="mx-auto"
            width="300"
          />
        </div>
        <div>
          <div>
            <div class="mt-10 mb-5">
              <span
                >Press <kbd dark>alt + ctrl + s</kbd> to save,
                <kbd dark>alt + ctrl + r</kbd> to run</span
              >
            </div>
            <v-sheet color="#2d2d2d" class="py-3">
              <prism-editor
                v-model="code"
                cols="5"
                :highlight="highlight"
                class="my-editor px-3"
                line-numbers
                @keyup.alt.83="saveChanges"
                @keyup.alt.82="execute"
                @keydown="smartTyper"
              ></prism-editor>
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

          <v-simple-table height="500">
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
        </div>
        <v-snackbar v-model="saved" timeout="3000" top right close
          >Saved</v-snackbar
        >
      </v-container>
    </v-app>
  </div>
</template>

<script>
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css"; // import the styles somewhere

export default {
  components: {
    PrismEditor
  },
  data() {
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
      ]
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

      const { data = [] } = await this.axios.post(
        "http://localhost:8000/lexxer/execute/",
        {
          raw_data
        }
      );

      console.log(data);

      this.lexicalData = [...data.lexxer];

      this.stringifyCode = raw_data;
      this.loading = false;
    },
    smartTyper(event) {
      const pairs = {
        '"': '"',
        "(": ")",
        "{": "}",
        "|": "|>|"
      };

      const keyTyped = event.key;
      const inputElement = event.target;

      if (
        !Object.keys(pairs).includes(keyTyped) ||
        document.getSelection().toString()
      ) {
        return;
      }

      let cursorPos = inputElement.selectionStart;
      let closingChar = pairs[keyTyped];

      if (
        (keyTyped === "|" && this.code[cursorPos - 1] === "<") ||
        keyTyped !== "|"
      ) {
        inputElement.value =
          inputElement.value.substr(0, cursorPos) +
          closingChar +
          inputElement.value.substr(cursorPos);

        inputElement.setSelectionRange(cursorPos, cursorPos);
      }
    }
  },
  created() {
    this.code = localStorage.getItem("code");
  }
};
</script>

<style>
.my-editor {
  background: #2d2d2d;
  color: #fff;
  font-family: Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 16px;
  line-height: 1.6;
}
.prism-editor__textarea:focus {
  outline: none;
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
</style>
