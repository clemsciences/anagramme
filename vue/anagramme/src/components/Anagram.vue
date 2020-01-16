<template>
    <v-container class="mx-6">
        <h1>Anagram solver</h1>
        <v-row>
            <v-textarea
            solo
            v-model="textToAnalyse"
            label="Text to decipher"
            name="textToDecipher">
            </v-textarea>
        </v-row>
        <v-row>
            <v-btn @click="tokenize">Tokenize</v-btn>
        </v-row>
        <v-row>
            <v-col>
                <v-checkbox
                v-model="loadFromCLTK"
                label="Load from CLTK">
                </v-checkbox>
            </v-col>
            <v-col>
                <v-checkbox
                v-model="loadFromUserInput"
                label="Load from your tokens">
                </v-checkbox>
            </v-col>
        </v-row>
        <div v-if="loadFromCLTK">
            <v-select
                :items="items"
                label="Available dictionaries"
                outlined
            ></v-select>
        </div>
        <v-row>
        <v-textarea
            v-if="loadFromUserInput"
            solo
            v-model="wordInput"
            label="Known tokens"
            name="lexicon">
            </v-textarea>
        </v-row>
        <ul id="results">
            <li v-for="result in results" :key="result">
                {{ result.word }}
            </li>
        </ul>

    </v-container>

</template>
<script>
import axios from 'axios';
export default {
    data: () => {
        return {
            loadFromCLTK: false,
            loadFromUserInput: false,
            textToAnalyse: "",
            wordInput: "",
            items: [],
            results: [],
            headers: { 'content-type': 'application/json' }
        }
    },
    mounted() {
        this.loadCltkLibraries();
    },
    methods: {
        tokenize() {
            axios.post("http://127.0.0.1:5000/tokenize",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    this.textToAnalyse = response.data.result;
                }
            });
        },
        getAllPossibleCombinaisons() {
            axios.post("http://127.0.0.1:5000/possible_words",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    this.results = response.data.result;
                }
            });
        },
        loadCltkLibraries() {
            let self = this;
            axios.get("http://127.0.0.1:5000/load_cltk_libraries",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    self.items = Object.values(response.data.result);
                }
            });
        }
    },

}
</script>

<style scoped>

</style>
