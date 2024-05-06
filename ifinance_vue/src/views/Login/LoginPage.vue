<template>
  <div class="container">
    <div class="login">
      <h1 class="title">Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email:</label>
          <input v-model="email" type="email" id="email" required />
        </div>

        <div class="form-group">
          <label for="password">Password:</label>
          <input v-model="password" type="password" id="password" required />
        </div>

        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage">{{ errorMessage }}</p>
      <p v-if="welcomeMessage">{{ welcomeMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";

export default {
  name: "LoginPage",
  data: function () {
    return {
      email: "",
      password: "",
      errorMessage: "",
      welcomeMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      console.log(this.email, this.password);
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/user/login/",
          {
            email: this.email,
            password: this.password,
          }
        );
        // Login successful - Update user data in store (assuming 'setUser' mutation)
        // store.commit("setUser", response.data.user);
        this.setUserProfile(response.data.user);
        this.setAuthToken(response.data.token);

        // Login successful - Redirect to desired page (replace with your actual URL)
        this.$router.push("/");
      } catch (error) {
        this.errorMessage = error.response?.data?.error || "Login failed."; // Handle potential errors
      }
    },
    ...mapMutations(["setUserProfile", "setAuthToken"]),
  },
};
</script>

<style scoped>
/* Add your CSS styles here */

.container {
  height: 565px;
  background-color: #1e212a;
  padding-top: 5em;
  width: 40%;
  border-radius: 50px;
}

.login {
  max-width: 400px;
  margin: 0 auto;
}

.title {
  color: #fff;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  background-color: #1e212a;
  border-bottom: 2px solid white;
  border-right: 2px solid #1e212a;
  padding: 0.5rem;
  height: 3em;
  outline: none;
  color: white;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  margin-top: 2em;
  height: 2.5em;
  width: 100%;
  border-radius: 10px;
}

button:hover {
  background-color: green;
  font-weight: 800;
}
</style>
