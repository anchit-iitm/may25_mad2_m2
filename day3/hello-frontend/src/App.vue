<template>
  <h2>app.vue start</h2>
  <nav>
    <router-link :to="{'name': 'home'}">Home</router-link> |
    <router-link :to="{'name': 'about'}">About</router-link> |
    <router-link :to="{'name': 'test'}">Test</router-link>
  </nav>
  <router-view/>
  <h2>app.vue end</h2>
</template>

<script>
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
