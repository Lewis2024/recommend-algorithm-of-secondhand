<template>
  <div>
    <button @click="getRecommendations">获取推荐</button>
    <div v-for="(recommendation, index) in recommendations" :key="index">
      {{ recommendation }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      recommendations: []
    };
  },
  methods: {
    getRecommendations() {
      axios.get('http://localhost:8080/recommendations?userId=i')
        .then(response => {
          this.recommendations = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
