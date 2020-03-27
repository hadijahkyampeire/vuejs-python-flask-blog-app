<template>
  <div class="register">
    <h2>Register</h2>
    <form>
      <div class="form-group">
        <input type="text" class="form-control" id="username" placeholder="Enter username" />
      </div>
      <div class="form-group">
        <input
          type="email"
          class="form-control"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
          placeholder="Enter email"
        />
        <small
          id="emailHelp"
          class="form-text text-muted"
        >We'll never share your email with anyone else.</small>
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
      <button type="submit" class="btn btn-register">Register</button>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  name: "register"
};
</script>

<style >
.register {
  margin: auto;
  width: 60%;
  border-radius: 1rem;
  display: block;
  box-shadow: 1px 1px 1px 1px grey;
  border: solid 1px #fff;
}
h2 {
  background-color: #57b847;
  text-align: center;
  padding: 1.5rem;
  border-top-left-radius: 0.75rem;
  border-top-right-radius: 0.75rem;
  color: #fff;
}

form {
  margin: 2rem;
}

.btn-register {
  background-color: #57b847;
  text-align: center;
  color: #fff;
  text-transform: uppercase;
  width: 30%;
  border-radius: 10rem;
}

input.form-control {
    border-radius: 10rem;
    background-color: #ebebeb;
}

.form-control::placeholder {
    color: #3e5239;
    font-weight: bold;
    padding-left: 2rem;
}
</style>