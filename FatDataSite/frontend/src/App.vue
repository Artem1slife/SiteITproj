<template>
  <div class="wrapper">
    <header>
      <div class="navbar">
        <div class="container">
          <div class="navbar-content">
             <ul class="navbar-list">
            <img src="../src/images/logo.png" class="logo">
           
              <li class="navbar-item" v-for="link in linksDcr" :key="link.title">
                <router-link class="navbar-link" :title="link.title" :to="link.url">{{ link.title }}</router-link>
              </li>
            </ul>

            <ul class="navbar-list">
              <li class="navbar-item" v-for="link in linksMain" :key="link.title">
                <router-link class="navbar-link" :title="link.title" :to="link.url">{{ link.title }}</router-link>
              </li>
            </ul>

            <ul class="navbar-list">
              <li class="navbar-item" v-for="link in linksProf" :key="link.title">
                <router-link class="navbar-link" :title="link.title" :to="link.url">{{ link.title }}</router-link>
              </li>
               <li class="navbar-item" v-if="checkUser" @click="logout">
                 <span class="navbar-link">Logout</span>
               </li>
            </ul>

            
          </div>
        </div>
      </div>
    </header>

    <router-view></router-view>

    <!-- <footer></footer> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      linksMain: [
        { title: "Вес слов", url: "/weightWords" },
        { title: "Облако слов", url: "/wordCloud" },
        { title: "Схожесть текстов", url: "/similarityTexts" },
        { title: "Количественный анализ", url: "/quantitativeАnalysis" },
        
      ],
      linksDcr: [
        { title: "O CAT", url: "/aboutCat" },
        { title: "Виды аналитики", url: "/typesAnalytics" },
      ],
    }
  },
   methods: {
    logout () {
      this.$store.dispatch('logoutUser')
      this.$router.push('/login')
    }
  },
  computed: {
    checkUser () {
      return this.$store.getters.checkUser
    },
    linksProf () {
      if(this.checkUser) {
        return [
          { title: "Личный кабинет", url: "/personalArea"},
        ]
      }
      return [
        { title: "Регистрация", url: "/registration"},
        { title: "Войти", url: "/login"},    
      ]
    }
  },
};
</script>

<style lang="scss">
.navbar-link {
  &.router-link-exact-active {
    color: #5247e7;
  }
}
</style>
