<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"
          ><strong>iFinance</strong></router-link
        >

        <a
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu"
        >
          >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div
        class="navbar-menu"
        id="navbar-menu"
        v-bind:class="{ 'is-active': showMobileMenu }"
      >
        <div class="navbar-end">
          <router-link to="/transactions" class="navbar-item"
            >Transactions</router-link
          >
          <router-link to="/budget" class="navbar-item">Budget</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <a
                v-if="getUserProfile"
                @click="logout()"
                href="/login"
                class="button is-light"
                >Log Out</a
              >

              <a v-else href="/login" class="button is-dark">Log In</a>
              <a
                v-if="!getUserProfile"
                href="/signup"
                class="button is-primary"
              >
                <strong>Sign up</strong>
              </a>
              <p v-if="getUserProfile">
                Weclome, {{ getUserProfile.first_name }} 👋
              </p>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view />
    </section>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapGetters({
      getUserProfile: "getUserProfile",
    }),
  },
  created() {
    if (localStorage.getItem("token")) {
      this.fetchUserDetails();
    }
  },
  methods: {
    ...mapMutations(["logout"]),
    fetchUserDetails() {
      axios
        .get("http://127.0.0.1:8000/api/user/get_current_user_details/")
        .then((response) => {
          store.commit("setUser", response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleLogout() {
      this.logout();
      this.$router.push("/login");
    },
  },
  data() {
    return {
      showMobileMenu: false,
    };
  },
};
</script>

<style lang="scss">
@import "../node_modules/bulma";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
