<template>
  <div class="signup">
    <form @submit.prevent="handleSignUp">
      <div class="form-group">
        <label for="firstName">First Name:</label>
        <input v-model="firstName" type="text" id="firstName" required />
      </div>

      <div class="form-group">
        <label for="lastName">Last Name:</label>
        <input v-model="lastName" type="text" id="lastName" required />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input
          v-model="confirmPassword"
          type="password"
          id="confirmPassword"
          required
        />
      </div>

      <div class="form-group">
        <label for="bankBalance">Bank Balance:</label>
        <input v-model="bankBalance" type="number" id="bankBalance" />
        <p v-if="bankBalanceError" class="error-message">
          Please enter your bank balance.
        </p>
      </div>

      <button type="submit">Sign Up</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpPage",
  data: function () {
    return {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
      bankBalance: 0, // Initialize bank balance
      bankBalanceError: false,
    };
  },
  methods: {
    handleSignUp() {
      this.bankBalanceError = false; // Reset error flag

      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      // Check for empty bank balance
      if (!this.bankBalance) {
        this.bankBalanceError = true;
        this.errorMessage = "Please enter your bank balance.";
        return;
      }

      // Validate bank balance (already implemented in previous version)
      const decimalCount = (this.bankBalance.toString().split(".")[1] || "")
        .length;
      if (decimalCount > 2) {
        this.bankBalanceError = true;
        return;
      }

      axios
        .post("http://127.0.0.1:8000/api/user/", {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          password: this.password,
          bank_balance: this.bankBalance, // Add bank balance to data
        })
        .then((response) => {
          // Handle successful signup (e.g., redirect to login page)
          this.$router.push("/");
        })
        .catch((error) => {
          this.errorMessage = "An error occurred while signing up";
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your CSS styles here */
.signup {
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input[type="email"],
input[type="password"],
input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: green;
}
</style>
