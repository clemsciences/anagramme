<template>
    <v-container class="mx-6">
        <h1>Anagram solver</h1>
        <v-row>
            <v-textarea solo name="textToDecipher" hint="Text to decipher"></v-textarea>
        </v-row>
        <v-row>
            <v-btn @click="tokenize">Tokenize</v-btn>
        </v-row>
        <v-row>
            <v-col>
                <v-checkbox v-model="loadFromCLTK" label="Load from CLTK"></v-checkbox>
            </v-col>
            <v-col>
                <v-checkbox v-model="loadFromUserInput" label="Load from your tokens"></v-checkbox>
            </v-col>
        </v-row>
        <v-row>
        <v-textarea solo name="lexicon" hint="Known tokens"></v-textarea>
        </v-row>
        <v-text></v-text>
        
    </v-container>

</template>
<script>
export default {
    data: () => {
        return {
            loadFromCLTK: false,
            loadFromUserInput: false
        }
    },
    methods: {
        tokenize: function() {

        },
    },

}
</script>

<style scoped>

</style>