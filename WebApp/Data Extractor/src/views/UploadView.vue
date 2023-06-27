<script>
import axios from 'axios'
import { AtomSpinner } from 'epic-spinners'

export default {
  components: {
    AtomSpinner
  },
  data() {
    return {
      selectedFile: "",
      isLoading: false,
    };
  },
  methods: {
    onFileSelected(event) {
      this.selectedFile = event.target.files[0]
    },
    onUpload() {
      this.isLoading = true
      const fd = new FormData()
      console.log("something is happening")
      fd.append('pdffile', this.selectedFile, this.selectedFile.name)
      axios.post('http://localhost:5000/upload', fd).then(res => {
        console.log(res)
        this.$store.commit('setCsvString', res['data'])
        this.isLoading = false
        this.$router.push('/tableview')
      })
    }
  },
}

</script>

<template>
  <div id="header-container">
    <h1>
      <p id="header-text">
        Drag and Drop files to upload
      </p>
    </h1>
  </div>
  <div id="container">
    <div id="loading-animation" v-if="isLoading">
      <atom-spinner :animation-duration="1000" :size="60" :color="'#181818'" />
    </div>
    <div id="button-container" v-if="!isLoading">
      <input type="file" @change="onFileSelected" id="upload-selector" accept="application/pdf">
      <button id="upload-button" @click="onUpload" v-if="selectedFile">Click to upload file</button>
    </div>
  </div>
</template>

<style>
#header-container {
  position: absolute;
  transform: translateX(-50%);
  left: 50%;
  top: 10%;
}

#header-text {
  font-weight: bolder;
  color: #fccb06;
}

#upload-selector {
  width: 100%;
  height: 100%;
  text-align: center;
  color: #181818;
  font-weight: bold;
  font-size: larger;
}

#container {
  position: absolute;
  transform: translateX(-50%);
  left: 50%;
  top: 20%;
  background-color: #fccb06;
  height: 50%;
  width: 60%;
  min-width: min-content;
  padding: 1.87em 1.87em;
  box-shadow: 0 1.25em 3.43em rgba(0, 0, 0, 0.08);
  border-radius: 0.5em;
  display: grid;
}

#button-container {
  display: grid;
  justify-content: center;
  align-content: center;
  height: 100%;
  width: 100%;
  column-gap: 2em;
  row-gap: 2em;
}

#loading-animation {
  height: 100%;
  width: 100%;
  display: grid;
  justify-content: center;
  align-content: center;
}

#upload-button {
  margin: auto;
  align-items: center;
  background-color: #181818;
  border-radius: 12px;
  box-shadow: transparent 0 0 0 3px, rgba(18, 18, 18, .1) 0 6px 20px;
  box-sizing: border-box;
  color: #fccb06;
  cursor: pointer;
  display: inline-flex;
  flex: 1 1 auto;
  font-family: Inter, sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  justify-content: center;
  line-height: 1;
  margin: 0;
  outline: none;
  padding: 1rem 1.2rem;
  text-align: center;
  text-decoration: none;
  transition: box-shadow .2s, -webkit-box-shadow .2s;
  white-space: nowrap;
  border: 0;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

#upload-button:hover {
  box-shadow: #121212 0 0 0 3px, transparent 0 0 0 0;
}
</style>