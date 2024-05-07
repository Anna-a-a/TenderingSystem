<template>
  <div class="container">
    <div v-if="tender">
      <div class="tender-card">
        <p class="overflow-text">
          <h4>{{ tender.title }}</h4>
        </p>
        <p class="overflow-text"><i class="fa-solid fa-location-dot red"></i> {{ tender.delivery_area }}, {{ tender.delivery_address }}</p>
        <p class="overflow-text"><i class="fa-regular fa-calendar"></i> {{ tender.date }} ({{ tender.time }}) - {{ tender.end_date }} ({{ tender.end_time }})</p>
        <p class="overflow-text">Цена: {{ tender.first_price }} <i class="fa-solid fa-ruble-sign"></i></p>
        <p class="overflow-text">{{ tender.description }}</p>
        <div v-if="userType == 'supplier'">
          <button class="mybtn" @click="goToAnswerPage(tender.id)">Участвовать</button>
        </div>
      </div>
      <div class="tender-card-participants" v-if="userType == 'customer'">
        <div class="tender-card-participants__head">Список участников</div>
        <div class="tender-card-participants__body" v-for="(participant, index) in tender.supplier_logins" :key="index">
          <div v-if="participant">
            <div class="tender-card-participants__body-info">Пользователь: {{ participant }}</div>
            <div class="tender-card-participants__body-info">Компания/ИП: {{ tender.supplier_names[index] }}</div>
            <div class="tender-card-participants__body-info">Цена: {{ tender.supplier_prices[index] }} <i class="fa-solid fa-ruble-sign"></i></div>
            <button class="mybtn" @click="chooseWinner(participant, tender.id)">Выбрать как победителя</button>
          </div>
          <div v-else>
            <div class="tender-card-participants__body-info">Участников пока нет</div>
          </div>
        </div>
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
      tender: null,
      userType: null,
      login: '',
    }
  },
  created() {
    this.getUserType();
    this.fetchTender();
    axios.get('/user_info')
      .then(response => {
        this.login = response.data.login;
      })
      .catch(error => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response);
      });
  },
  methods: {
    async getUserType() {
      try {
        const response = await axios.get('/user_info');
        this.userType = response.data.user_type;
      } catch (error) {
        console.error(error);
      }
    },
    fetchTender() {
      const id = this.id;
      const url = `/tenders_suppliers/${id}`;
      axios.get(url)
        .then(response => {
          this.tender = response.data;
          console.log(this.tender);
          if (!this.tender) {
            this.tender = null;
          }
          else {
            this.tender.date = new Date(this.tender.created_date_time).toLocaleDateString();
            this.tender.time = new Date(this.tender.start_date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            this.tender.end_date = new Date(this.tender.end_date_time).toLocaleDateString();
            this.tender.end_time = new Date(this.tender.end_date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            this.tender.delivery_address = this.tender.delivery_address.charAt(0).toUpperCase() + this.tender.delivery_address.slice(1);
            this.tender.delivery_area = this.tender.delivery_area.charAt(0).toUpperCase() + this.tender.delivery_area.slice(1);
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    goToAnswerPage(id) {
      this.$router.push(`/tender/${id}/response`);
    },
    chooseWinner(login, id) {
      const formData = {
                login: login,
                tender_id: id,
            };
      axios.post('/tender_winner', formData)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
  }
}
</script>