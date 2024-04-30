<template>
  <div v-if="tender">
    <h1>{{ tender.title }}</h1>
    <p>ID: {{ tender.id }}</p>
    <p>Дата: {{ tender.date }}</p>
    <p>Описание: {{ tender.description }}</p>
    <p>Место поставки: {{ tender.delivery_area }}, {{ tender.delivery_address }}</p>
    <p>Цена: {{ tender.first_price }} ₽</p>
    <p>Окончание (МСК): {{ tender.end_date }} {{ tender.end_time }}</p>
  </div>
  <div v-else>
    <p>Тендер не найден</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['id'],
  data() {
    return {
      tender: null
    }
  },
  created() {
    this.fetchTender()
  },
  methods: {
    fetchTender() {
  axios.get('/tenders')
    .then(response => {
      const tenders = response.data;
      this.tender = tenders.find(tender => tender.id.toString() === this.id.toString());
      if (!this.tender) {
        this.tender = null;
      }
    })
    .catch(error => {
      console.error(error);
    });
}


  }
}
</script>
