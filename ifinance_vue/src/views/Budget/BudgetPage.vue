<template>
  <div class="container">
    <form @submit.prevent="submitBudget">
      <label for="budget-name">Budget Name:</label>
      <input type="text" id="budget-name" v-model="budgetName" required />

      <label for="start-date">Start Date:</label>
      <input type="date" id="start-date" v-model="startDate" required />

      <label for="end-date">End Date:</label>
      <input type="date" id="end-date" v-model="endDate" required />

      <label for="budget-amount">Budget Amount:</label>
      <input type="number" id="budget-amount" v-model="budgetAmount" required />

      <button type="submit">Submit Budget</button>
    </form>
  </div>

  <!-- Header row -->
  <div class="budgets">
    <div class="budget-header">
      <p>Budget Name</p>
      <p>Start Date</p>
      <p>End Date</p>
      <p>Budget Amount</p>
      <p>Remaining Budget</p>
    </div>

    <!-- Budget items -->
    <div class="budget" v-for="budgetItem in budgets" :key="budgetItem.id">
      <p>{{ budgetItem.budget_name }}</p>
      <p>{{ formatDate(budgetItem.start_date) }}</p>
      <p>{{ formatDate(budgetItem.end_date) }}</p>
      <p>$ {{ budgetItem.budget_amount }}</p>
      <!-- You can calculate remaining budget here if needed -->
      <!-- <p>$ {{ calculateRemainingBudget(budgetItem) }}</p> -->
      <p>$ {{ calculateRemainingBudget(budgetItem) }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "BudgetPage",
  computed: {
    ...mapGetters({
      getUserProfile: "getUserProfile",
    }),
  },
  data() {
    return {
      budgetName: "",
      startDate: "",
      endDate: "",
      budgetAmount: null,
      budgets: [],
    };
  },
  created() {
    if (this.getUserProfile) {
      this.fetchUserBudgets();
    }
  },
  methods: {
    submitBudget() {
      const userId = this.getUserProfile.user_object_id;

      const budgetData = {
        budget_name: this.budgetName,
        budget_amount: this.budgetAmount,
        start_date: this.startDate,
        end_date: this.endDate,
      };

      console.log("Budget Data:", budgetData);

      const alertMessage = `You've set a budget of $${this.budgetAmount} from ${this.startDate} to ${this.endDate}`;
      window.alert(alertMessage);

      axios
        .post("http://127.0.0.1:8000/api/budget/", budgetData)
        .then((response) => {
          console.log("Budget submitted:", response.data);
          this.budgets.push(response.data);
        })
        .catch((error) => {
          console.error("Failed to submit budget:", error);
        });
    },
    fetchUserBudgets() {
      const userId = this.getUserProfile.user_object_id;

      axios
        .get(`http://127.0.0.1:8000/api/budget/?user=${userId}`)
        .then((response) => {
          console.log("User budgets:", response.data);
          this.budgets = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch user budgets:", error);
        });
    },
    calculateRemainingBudget(budgetItem) {
      // Calculate remaining budget
      const remainingBudget =
        budgetItem.budget_amount - this.calculateTotalExpense(budgetItem);

      // Return remaining budget
      return remainingBudget >= 0
        ? `$ ${remainingBudget.toFixed(2)}`
        : "Exceeded";
    },

    calculateTotalExpense(budgetItem) {
      // Initialize totalExpense variable
      let totalExpense = 0;

      // Iterate over expenses array and sum up expenses for the given budget item
      for (const expense of this.$store.state.expenses) {
        if (expense.budget === budgetItem.id) {
          totalExpense += parseFloat(expense.amount);
        }
      }

      // Return total expense
      return totalExpense.toFixed(2); // Adjust toFixed(2) to format the number to two decimal places
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day < 10 ? "0" + day : day}-${
        month < 10 ? "0" + month : month
      }-${year}`;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 50%;
  height: 50vh;
  border-radius: 2em;
}

label {
  display: block;
  margin-bottom: 0.5em;
  color: white;
}

input[type="date"],
input[type="number"],
input[type="text"] {
  width: 100%;
  padding: 0.5em;
  margin-bottom: 1em;
}

.budgets {
  margin-top: 130px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  display: grid;
}

.budget {
  background-color: #1e212a;
  color: white;
  padding: 2em;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1em;
  align-items: flex-start;
  text-align: center;
}

.budget:hover {
  background-color: rgba(0, 128, 0, 0.2);
}

button {
  width: 100%;
  padding: 0.5em;
  background-color: #1e212a;
  color: white;
  border: none;
  border-radius: 10px;
  margin-top: 1em;
  cursor: pointer;
}

button:hover {
  background-color: green;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  background-color: #1e212a;
  color: white;
  padding: 0.5em 1em;
  border-radius: 10px;
  margin-bottom: 1em;
  font-weight: bold;
  margin-top: 10%;
}

.budget-header p {
  flex: 1;
  text-align: center;
}

/* Modal styles */
.budgets {
  margin-top: 20px; /* Adjust margin-top as needed */
}

.budget-header {
  display: flex;
  justify-content: space-between;
  background-color: #1e212a;
  color: white;
  padding: 0.5em 1em;
  border-radius: 10px;
  margin-bottom: 1em;
  font-weight: bold;
}

.budget-header p {
  flex: 1;
  text-align: center;
}

.budget {
  background-color: #1e212a;
  color: white;
  padding: 2em;
  border-radius: 10px;
  margin-bottom: 1em;
  display: flex;
  justify-content: space-between;
}

.budget p {
  flex: 1;
  text-align: center;
}
</style>
