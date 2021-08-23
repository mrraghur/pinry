<template>
  <div class="home">
    <PHeader></PHeader>
    <Trends></Trends>
    <Pins></Pins>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import Pins from '../components/Pins.vue';
import Trends from '../components/Trends.vue';

export default {
  name: 'Home',
  components: {
    PHeader,
    Trends,
    Pins,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
