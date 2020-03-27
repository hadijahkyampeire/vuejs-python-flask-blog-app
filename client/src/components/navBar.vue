<template>
  <nav class="navbar navbar-expand-lg ">
    <a class="navbar-brand" href="#">My Vue Blog App</a>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <router-link class="nav-link" to="/">
            Home
            <span class="sr-only">(current)</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "navBar"
};
</script>

<style scoped>
nav {
  background-color: #57b847;
  color: #fff;
  margin-bottom: 2rem;
}

.navbar-nav .nav-link {
  color: #000;
}
.navbar-nav .active > .nav-link {
  color: #fff;
}

.navbar-brand {
  color: #3e5239;
  font-weight: bold;
}
</style>