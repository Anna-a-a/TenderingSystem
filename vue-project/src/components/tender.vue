<template>
  <div class="container">
    <div v-if="tender">
    <div class="tender-card">
      <p><h4>{{ tender.title }}</h4></p>
      <p><i class="fa-solid fa-location-dot red"></i> {{ tender.delivery_area }}, {{ tender.delivery_address }}</p>
      <p><i class="fa-regular fa-calendar"></i> {{ tender.date }} - {{ tender.end_date }}</p>
      <p>Цена: {{ tender.first_price }} <i class="fa-solid fa-ruble-sign"></i></p>
      <p>{{ tender.description }}</p>
      
    </div>
  </div>
    <div v-else>
      <p>Тендер не найден</p>
    </div>
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
      console.log(this.tender);
      if (!this.tender) {
        this.tender = null;
      }
      else {
        this.tender.date = new Date(this.tender.created_data_time).toLocaleDateString();
        this.tender.end_date = new Date(this.tender.end_data_time).toLocaleDateString();
        this.tender.end_time = new Date(this.tender.end_data_time).toLocaleTimeString();
        this.tender.delivery_address = this.tender.delivery_address.charAt(0).toUpperCase() + this.tender.delivery_address.slice(1);
        this.tender.delivery_area = this.tender.delivery_area.charAt(0).toUpperCase() + this.tender.delivery_area.slice(1);
      }
    })
    .catch(error => {
      console.error(error);
    });
}


  }
}
</script>
