<template>
  <v-container>
    <div class="mt-10">
      <input
        type="file"
        accept=".myth"
        ref="fileUpload"
        class="d-none"
        @change="uploadFile"
      />
      <v-row>
        <v-col cols="12" md="7">
          <v-sheet
            color="rgb(51,51,51)"
            class="rounded-t-lg d-flex align-center py-1"
            dark
          >
            <div>
              <v-img
                :src="require('@/assets/logo - mythosv2.png')"
                class="mx-3"
                width="120"
              />
            </div>
            <v-menu
              v-for="(toolbar, key) in toolbarItems"
              :key="key"
              bottom
              offset-y
              color="rgb(66,66,66)"
              dark
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn class="text-none" text v-bind="attrs" v-on="on">
                  <span v-text="key" class="text-capitalize" />
                </v-btn>
              </template>

              <v-list width="300">
                <v-list-item
                  @click="item.action"
                  v-for="(item, index) in toolbar.items"
                  :key="index"
                  link
                >
                  <span v-text="item.name"></span>
                  <v-spacer></v-spacer>
                  <kbd v-if="item.shortcut" v-text="item.shortcut" />
                </v-list-item>
              </v-list>
            </v-menu>
          </v-sheet>
          <v-divider></v-divider>
          <div>
            <v-sheet color="rgb(78,78,78)" class="d-flex align-center">
              <v-sheet color="rgb(66,66,66)" class="px-3 py-3 d-flex">
                <v-sheet
                  max-width="600px"
                  color="transparent"
                  class="d-flex align-center white--text text-body-2"
                >
                  <v-img
                    :src="require('@/assets/pillar.svg')"
                    width="20"
                    class="mr-3"
                  />
                  <span
                    class="text-truncate d-block"
                    v-text="filenameWithType"
                  />
                </v-sheet>
                <v-icon
                  v-if="hasChanges"
                  v-text="'fa-asterisk'"
                  size="10"
                  class="ml-2"
                  color="red"
                />
              </v-sheet>
              <v-spacer></v-spacer>
              <v-btn
                @click="execute"
                class="text-none white--text font-weight-bold"
                color="orange darken-1 mr-3"
                :loading="loading"
                small
              >
                Run
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
              class="d-flex white--text align-center px-3 py-2 text-body-2 rounded-b-lg"
              color="rgb(78,78,78)"
            >
              <v-spacer></v-spacer>
              <span v-text="`Ln ${cmCursorPos.line}, Col ${cmCursorPos.ch}`" />
              <v-badge
                :value="executedOnce && !loading"
                :color="lexicalData.length ? 'green' : 'red'"
                offset-x="3"
                offset-y="5"
                dot
              >
                <v-icon v-text="'fa-table'" size="16" class="ml-3" dark />
              </v-badge>
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
          <v-simple-table height="420">
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
          background-color="grey lighten-4"
          active-class="elevation-3"
          class="rounded-t-lg"
          color="brown--text text--darken-1"
          hide-slider
        >
          <v-tab>
            <span>
              Messages
            </span>
            <span v-if="errorCount">
              <v-icon
                v-text="'fa-exclamation-triangle'"
                color="red"
                class="mx-3"
                size="16"
              />
              <span
                v-text="errorCount"
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
                    class="font-weight-bold text-body-1"
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
              <tbody v-if="errorCount">
                <tr
                  @click="showErrorLine(item.line, item.char_line)"
                  v-for="item in errors"
                  :key="item.name"

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
                    <span
                      v-else-if="header.value === 'code'"
                      v-text="
                        (item[header.value] && item[header.value][0]) || ''
                      "
                      class="font-weight-bold text-uppercase d-block text-center"
                    />
                    <span v-else v-text="item[header.value]" />
                  </td>
                </tr>
              </tbody>

              <tbody v-else>
                <tr  v-if="executedOnce">
                  <td class="text-body-1 text--center">
                    <v-icon
                      v-text="'fa-check-circle'"
                      color="success"
                      class="mt-n1"
                      size="16"
                    />
                  </td>
                  <td v-for="i in 3" :key="i">-</td>
                  <td class="text-body-1">Run Successfully</td>
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
              Enter a filename below:
            </p>
            <v-text-field
              autofocus
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
    </div>
  </v-container>
</template>

<script src="./Mythos.js" />

<style scoped>
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
