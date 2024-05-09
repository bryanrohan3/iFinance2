<template>
  <div class="banner">
    <div class="home">
      <p v-if="getUserProfile" class="hi_user">
        Welcome {{ getUserProfile.first_name }}
      </p>
      <p v-else>Please log in to see your account name.</p>
    </div>
  </div>

  <div class="bank_balance" v-if="getUserProfile">
    <p class="balance_amount">$ {{ getUserProfile.bank_balance }}</p>
    <p class="balance_name">Balance</p>
  </div>

  <div v-if="transactions.length > 0 && getUserProfile">
    <h1 class="title">Recent Transactions</h1>
    <template
      v-for="(transactionGroup, index) in groupedTransactions"
      :key="index"
    >
      <div class="date_trans">
        <span class="date_text">{{ transactionGroup.date }}</span>
      </div>

      <template
        v-for="transaction in transactionGroup.transactions"
        :key="transaction.id"
      >
        <div v-if="transaction.type === 'income'" class="transaction_positive">
          <div class="icon"></div>
          <div class="text_category">
            <div class="text">{{ transaction.source }}</div>
            <div class="category">{{ transaction.category_name }}</div>
          </div>
          <div class="amount">+ ${{ transaction.amount }}</div>
        </div>
        <div
          v-else-if="transaction.type === 'expense'"
          class="transaction_negative"
        >
          <div class="icon"></div>
          <div class="text_category">
            <div class="text">{{ transaction.source }}</div>
            <div class="category">{{ transaction.category_name }}</div>
          </div>
          <div class="amount_negative">- ${{ transaction.amount }}</div>
        </div>
      </template>
    </template>
  </div>

  <div v-else>
    <p v-if="!getUserProfile">Please log in to see your transactions.</p>
    <p v-else>No transactions found.</p>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      transactions: [],
    };
  },
  computed: {
    ...mapGetters({
      getUserProfile: "getUserProfile",
    }),
    // Group transactions by date
    groupedTransactions() {
      const grouped = {};
      this.transactions.forEach((transaction) => {
        const date = this.formatDate(transaction.date);
        if (!grouped[date]) {
          grouped[date] = [];
        }
        grouped[date].push(transaction);
      });

      // Convert grouped transactions into an array
      const groupedArray = Object.entries(grouped).map(
        ([date, transactions]) => ({
          date,
          transactions,
        })
      );

      // Sort the grouped array by date in descending order
      groupedArray.sort((a, b) => new Date(b.date) - new Date(a.date));

      return groupedArray;
    },
  },
  created() {
    // Fetch user transactions on component creation
    if (this.getUserProfile) {
      // Only fetch transactions if user is logged in
      this.fetchUserTransactions();
    }
  },
  methods: {
    fetchUserTransactions() {
      const userId = this.getUserProfile.user_object_id;

      // Fetch both income and expense transactions for the logged-in user
      axios
        .all([
          axios.get("http://127.0.0.1:8000/api/income", {
            params: {
              user: userId,
            },
          }),
          axios.get("http://127.0.0.1:8000/api/expense", {
            params: {
              user: userId,
            },
          }),
        ])
        .then(
          axios.spread((incomeResponse, expenseResponse) => {
            const incomeTransactions = incomeResponse.data.map(
              (transaction) => ({ ...transaction, type: "income" })
            );
            const expenseTransactions = expenseResponse.data.map(
              (transaction) => ({ ...transaction, type: "expense" })
            );
            // Combine and sort all transactions by both date and creation date
            this.transactions = [
              ...incomeTransactions,
              ...expenseTransactions,
            ].sort((a, b) => {
              const dateComparison = new Date(b.date) - new Date(a.date);
              if (dateComparison !== 0) {
                return dateComparison;
              } else {
                return (
                  new Date(b.date_time_created) - new Date(a.date_time_created)
                );
              }
            });
          })
        )
        .catch((error) => {
          console.error(error);
        });
    },

    formatDate(date) {
      // Implement date formatting logic here
      return new Date(date).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.home {
  max-width: 80%;
  margin: 0 auto;
}

.title {
  font-size: 1.5em;
  color: white;
  font-weight: 800;
  margin-top: 2%;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.hi_user {
  font-size: 1.6em;
  color: white;
  font-weight: 800;
}

.bank_balance {
  max-width: 80%;
  margin: 0 auto;
  border-radius: 10px;
  padding-top: 2%;
  padding-bottom: 2%;
}

.bank_balance:hover {
  background-color: #1e212a;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.bank_balance:hover .balance_amount {
  color: green;
  transition: color 0.3s ease;
  cursor: pointer;
}

.balance_name {
  font-size: 1em;
  margin-left: 3%;
  color: white;
  text-align: center;
}

.balance_amount {
  font-weight: 800;
  font-size: 2.5em;
  margin-left: 3%;
  color: white;
  text-align: center;
}

.banner {
  padding-top: 2%;
  padding-bottom: 2%;
}

/* Date of Transaction */

.date_trans {
  border-radius: 30px;
  padding: 0.6%;
  margin-top: 1em;
  max-width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.date_text {
  font-size: 1em;
  color: white;
  background-color: #1e212a;
  padding: 1% 2%;
  font-weight: 800;

  border-radius: 30px;
}

.date_text:hover {
  background-color: #1e212f;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

/* Transaction History */

.transaction_positive {
  max-width: 80%;
  margin-top: 1em;
  border-radius: 10px;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  padding: 1.5em 0.5em;

  /* background-color: rgba(0, 128, 0, 0.2); */
  background-color: #1e212a;
  transition: background-color 0.3s ease;
}

.transaction_positive:hover {
  background-color: rgba(0, 128, 0, 0.1);
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.icon {
  background-color: gray;
  margin: 0 auto;
  width: 40px;
  height: 40px;
  border-radius: 100px;
  margin-left: 2em;
}

.text {
  font-weight: 800;
  margin: auto 40em 0 0;
}

.text_catergory {
  flex: 1;
}

.amount {
  margin: 0 auto;
  color: green;
  font-weight: 800;
  float: right;
  margin-right: 2em;
}

.amount_negative {
  margin: 0 auto;
  color: red;
  font-weight: 800;
  float: right;
  margin-right: 2em;
}

.category {
  font-size: 1em;
  color: gray;
  border-radius: 30px;
}

/* Negative Transaction */
.transaction_negative {
  max-width: 80%;
  margin-top: 1em;
  border-radius: 10px;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  padding: 1.5em 0.5em;

  /* background-color: rgba(0, 128, 0, 0.2); */
  background-color: #1e212a;
  transition: background-color 0.3s ease;
}

.transaction_negetive {
  max-width: 80%;
  margin-top: 1em;
  border-radius: 10px;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  padding: 1.5em 0.5em;

  /* background-color: rgba(0, 128, 0, 0.2); */
  background-color: #1e212a;
  transition: background-color 0.3s ease;
}

.transaction_negative:hover {
  background-color: rgba(128, 0, 0, 0.2);
  transition: background-color 0.3s ease;
  cursor: pointer;
}
</style>
