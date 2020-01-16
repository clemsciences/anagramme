<template>
  <v-app>
    <v-content>
      <Anagram></Anagram>
    </v-content>
  </v-app>
</template>

<script>
import Anagram from './components/Anagram';

export default {
  name: 'App',

  components: {
    Anagram
  },

  data: () => ({
    //
  }),
};
</script>
