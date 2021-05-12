<template>
  <div class="wrapper-content wrapper-content--fixed">
    <section>
    
      <div class="container">
          <div>
        <img src="../images/CatPng7.png">
      </div>
      <div>
        <h1>
          404
        </h1>
        <h2>
          Няяяя!!! Страница не найдена. Прейдите на главную старницу
          <router-link class="link" to="/typesAnalytics">main page</router-link>
        </h2>  
      </div>
      </div>
    </section>
  </div>
</template>


<style scoped>
.wrapper-content {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}


.container {
  display: flex;
  justify-content: space-around;
  margin-bottom: 50px;
  align-items: center;
}

h1 {
  Font-style: Bold;
Font-size: 288px;
Line-height: 351px;
Line-height: 100%;
Vertical-align: Center;
color: #D5AAE1;
}

h2 {
Font-style: Light;
Font-size: 48px;
Line-height: 59px;
Line-height: 100%;  
Vertical-align: Center;
color: #D5AAE1;
}



</style>
