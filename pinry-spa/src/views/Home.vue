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
<style>
.home{
background: hsla(53, 84%, 74%, 1);

background: linear-gradient(90deg, hsla(53, 84%, 74%, 1) 0%, hsla(336, 87%, 61%, 1) 50%, hsla(262, 81%, 71%, 1) 100%);

background: -moz-linear-gradient(90deg, hsla(53, 84%, 74%, 1) 0%, hsla(336, 87%, 61%, 1) 50%, hsla(262, 81%, 71%, 1) 100%);

background: -webkit-linear-gradient(90deg, hsla(53, 84%, 74%, 1) 0%, hsla(336, 87%, 61%, 1) 50%, hsla(262, 81%, 71%, 1) 100%);

filter: progid: DXImageTransform.Microsoft.gradient( startColorstr="#F4E784", endColorstr="#F24389", GradientType=1 );
}
</style>
