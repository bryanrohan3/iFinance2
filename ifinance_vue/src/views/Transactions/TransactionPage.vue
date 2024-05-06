<template>
  <div class="container">
    <!-- button that enables a pop up -->
    <div v-if="isLoggedIn" class="add_transaction" @click="showModal = true">
      <button class="button">+</button>
      <p>Add Transaction</p>
    </div>
    <p v-else class="login-message">
      You need to be logged in to make a transaction
    </p>

    <!-- Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <!-- Modal content -->
        <span class="close" @click="closeModal">&times;</span>

        <div class="tabs">
          <ul>
            <li
              :class="{ 'is-active': activeTab === 'expense' }"
              @click="activeTab = 'expense'"
            >
              <a>Expense</a>
            </li>
            <li
              :class="{ 'is-active': activeTab === 'income' }"
              @click="activeTab = 'income'"
            >
              <a>Income</a>
            </li>
          </ul>
        </div>

        <div v-if="activeTab === 'expense'">
          <form @submit.prevent="submitExpense">
            <label for="expense-tag">Tag:</label>
            <select id="expense-tag" v-model="expense.tag" required>
              <option value="" disabled>Select Tag</option>
              <option value="0">Food</option>
              <option value="1">Transport</option>
              <option value="2">Utilities</option>
              <option value="3">Entertainment</option>
              <option value="4">Other</option>
            </select>

            <label for="expense-cost">Cost:</label>
            <input
              type="number"
              id="expense-cost"
              v-model="expense.cost"
              required
            />

            <label for="expense-date">Date:</label>
            <input
              type="date"
              id="expense-date"
              v-model="expense.date"
              required
            />

            <label for="expense-budget">Budget:</label>
            <select id="expense-budget" v-model="expense.budget">
              <option value="" disabled>Select Budget (optional)</option>
              <option v-for="budget in budgets" :value="budget.id">
                {{ budget.budget_name }}
              </option>
            </select>

            <button type="submit">Submit Expense</button>
          </form>
        </div>

        <div v-if="activeTab === 'income'">
          <form @submit.prevent="submitIncome">
            <label for="income-tag">Tag:</label>
            <select id="income-tag" v-model="income.tag" required>
              <option value="" disabled>Select Tag</option>
              <option value="0">Salary</option>
              <option value="1">Bonus</option>
              <option value="2">Gift</option>
              <option value="3">Other</option>
            </select>

            <label for="income-cost">Cost:</label>
            <input
              type="number"
              id="income-cost"
              v-model="income.cost"
              required
            />

            <label for="income-date">Date:</label>
            <input
              type="date"
              id="income-date"
              v-model="income.date"
              required
            />

            <button type="submit">Submit Income</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "TransactionPage",
  computed: {
    ...mapGetters({
      getUserProfile: "getUserProfile",
    }),
  },
  data() {
    return {
      showModal: false,
      activeTab: "expense",
      expense: {
        type: "expense",
        tag: "",
        cost: null,
        date: "",
        budget: null,
      },
      income: {
        type: "income",
        tag: "",
        cost: null,
        date: "",
      },
      budgets: [],
    };
  },
  created() {
    if (this.getUserProfile) {
      this.fetchBudgets();
    }
  },
  methods: {
    closeModal() {
      this.showModal = false;
    },
    async fetchBudgets() {
      const userId = this.$store.getters.getUserProfile.user_object_id;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/budget/?user=${userId}`
        );
        this.budgets = response.data;
      } catch (error) {
        console.error("Failed to fetch budgets:", error);
        this.budgets = [];
      }
    },
    async fetchBudgetsInRange(date) {
      const userId = this.$store.getters.getUserProfile.user_object_id;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/budget/?user=${userId}&start_date__lte=${date}&end_date__gte=${date}`
        );
        this.budgets = response.data.filter(
          (budget) => budget.start_date <= date && budget.end_date >= date
        );
      } catch (error) {
        console.error("Failed to fetch budgets:", error);
        this.budgets = [];
      }
    },

    submitExpense() {
      const userId = this.$store.getters.getUserProfile.user_object_id;

      const expenseData = {
        category: this.expense.tag,
        amount: this.expense.cost,
        date: this.expense.date,
        budget: this.expense.budget,
      };

      axios
        .post("http://127.0.0.1:8000/api/expense/", expenseData)
        .then((response) => {
          console.log("Expense submitted:", response.data);
          // Update budget amount on successful submission
          const budgetIndex = this.budgets.findIndex(
            (budget) => budget.id === this.expense.budget
          );
          if (budgetIndex !== -1) {
            // Subtract expense amount from budget amount
            this.budgets[budgetIndex].budget_amount -= this.expense.cost;
            // Update budget amount in the backend
            axios
              .patch(
                `http://127.0.0.1:8000/api/budget/${this.expense.budget}/`,
                {
                  budget_amount: this.budgets[budgetIndex].budget_amount,
                }
              )
              .then((response) => {
                console.log("Budget amount updated:", response.data);
              })
              .catch((error) => {
                console.error("Failed to update budget amount:", error);
              });
          }
          this.closeModal();
        })
        .catch((error) => {
          this.errorMessage = "Failed to submit expense!";
          console.error(error);
        });
    },

    submitIncome() {
      const userId = this.$store.getters.getUserProfile.user_object_id;
      // ...

      const incomeData = {
        category: this.income.tag,
        amount: this.income.cost,
        date: this.income.date,
        user: userId,
      };

      axios
        .post("http://127.0.0.1:8000/api/income/", incomeData)
        .then((response) => {
          console.log("Income submitted:", response.data);
          this.closeModal();
        })
        .catch((error) => {
          this.errorMessage = "Failed to submit income";
          console.error(error);
        });
    },
  },
  computed: {
    isLoggedIn() {
      return !!this.$store.getters.getUserProfile;
    },
  },
  watch: {
    "expense.date"(newDate) {
      if (newDate) {
        this.fetchBudgetsInRange(newDate);
      }
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
  background-color: #1e212a;
}

.button {
  background-color: gray;
  color: #fff;
  border: none;
  cursor: pointer;
  height: 2em;
  width: 2em;
  transition: background-color 0.3s ease;
  border-radius: 80px;
  margin-left: 3em;
  margin-right: 1em;
}

.button:hover {
  background-color: green;
  transition: background-color 0.3s ease;
}

.add_transaction {
  display: flex;
  margin-top: 3em;
  align-content: center;
  cursor: pointer;
}

.add_transaction p {
  color: white;
  margin-left: 0.5em;
  align-self: center;
  font-weight: 800;
}

.login-message {
  color: white;
  margin-top: 1em;
  align-self: center;
  font-weight: bold;
  justify-content: center;
  align-items: center;
  display: flex;
  position: relative;
  top: 30%;
}

/* Modal styles */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 20px;
  width: 50%;
  border-radius: 1em;
  height: auto; /* Remove fixed height */
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

form {
  margin-bottom: 2em;
}

label {
  display: block;
  margin-bottom: 0.5em;
}

input,
select {
  width: 100%;
  padding: 0.5em;
  margin-bottom: 1em;
}

.tabs {
  margin-bottom: 1em;
}

.tabs ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
}

.tabs li {
  margin-right: 1em;
  cursor: pointer;
}

.tabs li.is-active a {
  font-weight: 800;
  color: #1e212a;
}

.submit {
  margin-top: 1em;
  width: 100%;
  padding: 0.5em;
  background-color: #1e212a;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
</style>
