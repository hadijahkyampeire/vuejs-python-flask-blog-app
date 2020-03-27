<template>
  <div class="login">
    <h2>Login</h2>
    <form>
      <div class="form-group">
        <input
          type="email"
          class="form-control"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
          placeholder="Enter email"
        />
      </div>
      <div class="form-group">
        <input
          type="password"
          class="form-control"
          id="exampleInputPassword1"
          placeholder="Password"
        />
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-login">Login</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "login"
};
</script>

<style >
.login {
  margin: auto;
  width: 60%;
  border-radius: 1rem;
  display: block;
  box-shadow: 1px 1px 1px 1px grey;
  border: solid 1px #fff;
}

.btn-login {
  background-color: #fff;
  text-align: center;
  color: #57b847;
  text-transform: uppercase;
  width: 30%;
  border-radius: 10rem;
  border: solid 1px #57b847;
}
</style>
