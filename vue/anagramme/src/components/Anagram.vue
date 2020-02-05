<template>
    <v-container class="mx-6">
        <h1 class="text-center"><a href="https://en.wikipedia.org/wiki/Anagram">Anagram</a> solver</h1>

        <h2>Text to decipher</h2>
        <v-row>
            <v-col cols="12">
                <v-textarea
                    solo
                    v-model="textToAnalyse"
                    label="Text to decipher"
                    name="textToDecipher">
                </v-textarea>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="2">
            <v-btn @click="tokenize">Tokenize</v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="3">
                <v-checkbox
                v-model="loadFromCLTK"
                label="Load from CLTK">
                </v-checkbox>
            </v-col>
            <v-col cols="3">
                <v-checkbox
                v-model="loadFromUserInput"
                label="Load from your tokens">
                </v-checkbox>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="4" v-if="loadFromCLTK">
                <p>Available dictionaries</p>
                <v-select
                    :items="items"
                    label="Available dictionaries"
                    outlined
                    multiple
                    v-model="chosenLibrary"
                >

                </v-select>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" v-if="loadFromUserInput">
                <h2>User input</h2>
                <v-textarea
                    solo
                    v-model="wordInput"
                    label="Known tokens"
                    name="lexicon">
                </v-textarea>
            </v-col>
        </v-row>
        <v-btn @click="findWordAnagrams">Compute word anagrams</v-btn>
        <v-btn @click="findSentenceAnagrams">Compute sentence anagrams</v-btn>
        <span hidden><v-btn @click="exportResult">Copy</v-btn></span>
        <v-list id="results" class="my-auto">
            <v-list-item v-for="(result, i) in anagramsFound" :key="i">
                {{ result.token }} : {{ result.anagrams }}
            </v-list-item>
        </v-list>

    </v-container>

</template>
<script>
import axios from 'axios';
import dotenv from 'dotenv'
dotenv.config()
const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_SITE_API_URL,
  timeout: 0,
});

export default {
    data: () => {
        return {
            loadFromCLTK: false,
            loadFromUserInput: true,
            textToAnalyse: "bjoonur",
            wordInput: "bonjour",
            items: [],
            headers: { 'content-type': 'application/json' },
            anagramsFound: [],
            chosenLibrary: ""
        }
    },
    mounted() {
        this.loadCltkLibraries();
    },
    methods: {
        tokenize() {
            axiosInstance.post("/tokenize",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    this.textToAnalyse = response.data.result;
                }
            });
        },
        getAllPossibleCombinaisons() {
            axiosInstance.post("/anagramme/possible_words",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    this.results = response.data.result;
                }
            });
        },
        loadCltkLibraries() {
            axiosInstance.get("/load_cltk_libraries",
                {text: this.textToAnalyse}, this.headers).then(response => {
                if(response.data.success) {
                    this.items = Object.values(response.data.result);
                }
            });
        },
        findWordAnagrams() {
            let data = {text: this.textToAnalyse, scale: "word"};
            if(this.loadFromCLTK) {
                data.cltk_choice = this.chosenLibrary;
            } else {
                data.cltk_choice = "";
            }
            if (this.loadFromUserInput) {
                data.user_input = this.wordInput;
            } else {
                data.user_input = "";
            }
            this.findAnagrams(data);
        },
        findSentenceAnagrams() {
            let data = {text: this.textToAnalyse, scale: "sentence"};
            if(this.loadFromCLTK) {
                data.cltk_choice = this.chosenLibrary;
            } else {
                data.cltk_choice = "";
            }
            if (this.loadFromUserInput) {
                data.user_input = this.wordInput;
            } else {
                data.user_input = "";
            }
            this.findAnagrams(data);
        },
        findAnagrams(data) {
            axiosInstance.post("/find_anagrams",
            data, this.headers).then(response => {
                if(response.data.success) {
                    this.anagramsFound = response.data.result
                }
            });
        },
        exportResult() {
            return true;
        }
    },

}
</script>

<style scoped>

</style>
