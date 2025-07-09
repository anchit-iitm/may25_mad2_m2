<template>
  <div class="about">
    <h1><a v-if="this.message!==''">{{this.message}}, </a>This is an about page</h1>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'AboutView',
  data() {
    return {
      message: '',
      token: ''
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      alert('You are not logged in. Please log in first.');
      this.$router.push({ name: 'login' });
      return;
    }
    if (localStorage.getItem('userRole') !== 'admin') {
      alert('You do not have permission to access this page.');
      this.$router.push({ name: 'home' });
      return;
    }
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios
        .get('http://localhost:5000/helloWorld',
          { headers: 
            {'Authorization': this.token}
          }
        )
        .then(response => {
          this.message = response.data.message;
        })
        .catch(error => {
          alert('Error fetching data: ' + error.message);
        });
    }
  },
}
</script>
