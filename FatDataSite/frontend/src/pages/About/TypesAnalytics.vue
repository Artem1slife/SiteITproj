<template>
  <div class="wrapper-content wrapper-content--fixed">
    <section>
      <div class="container">
        <div>
          <h1>Качественный анализ (вес слов)</h1>
          <p>
            В каждом документе определяется вес слова в зависимости от частоты
            вхождения этого слова в корпус. Для нормализации результата
            используется статистическая метрика TF-IDF* Для одного документа
            также можно рассчитать вес - предложения принимаются за отдельные
            документы и вес слов рассчитывается уже по отношению к ним. <br><br> *TF-IDF
            (от англ. TF — term frequency, IDF — inverse document frequency).
            Вес некоторого слова пропорционален частоте употребления этого слова
            в документе и обратно пропорционален частоте употребления слова во
            всех документах коллекции
          </p>
        </div>

        <div>
          <img src="@/images/temp.png" />
        </div>
      </div>

      <div class="container">
        <div>
          <img src="@/images/temp.png" />
        </div>
        <div>
          <h1>Облако слов</h1>
          <p>
            Эта техника широко применяется в инфографике и презентациях --
            облако слов наглядно представляет ключевые слова в тексте. Размер
            слова зависит от количества повторений его в тексте
          </p>
        </div>
      </div>

      <div class="container">
        <div>
          <h1>Схожесть текстов</h1>
          <p>
            Для решения задачи определения близости двух текстов мы рассчитываем
            косинусное расстояние между векторами их представления. Результат
            представлен в виде тепловой карты, где показаны значения близости
            двух и более корпусов
          </p>
        </div>

        <div>
          <img src="@/images/temp.png" />
        </div>
      </div>

      <div class="container">
        <div>
          <img src="@/images/temp.png" />
        </div>
        <div>
          <h1>Колличественный анализ</h1>
          <p>
            Результатом работы является таблица слов, которые повторяются в
            документе наибольшее количество раз. Такой вид анализа подходит для
            быстрого просмотра страницы или документа на наличие повторов
            определенных слов.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 50px;
}

p {
  font-size: 24px;
  line-height: 29px;
  line-height: 100%;
  vertical-align: Top;
  max-width: 700px;
}

h1 {
  font-style: Bold;
  font-size: 36px;
  line-height: 44px;
  line-height: 100%;
  vertical-align: Top;
  color: #9d4edd;
  margin-bottom: 36px;
}

ul {
  margin: 36px;
}

li {
  margin: 24px;
}
</style>
