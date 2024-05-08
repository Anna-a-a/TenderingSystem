<template>
  <SideMenu />
  <div class="container">
    <h1 style="text-align: center;">Мои тендеры</h1>
    <div class="mycard" v-if="tenders.length > 0">
      <div class="mycard-head">
        <div class="mycard-col">
          <div>
            Наименование
          </div>
        </div>
        <div class="mycard-col">
          <div>
            Место поставки
          </div>
        </div>
        <div class="mycard-col">
          <div>
            Цена
          </div>
        </div>
      </div>
      <div class="mycard-body mycard-tender" v-for="tender in tenders" :key="tender.id" @click="goToTender(tender.id)">
        <div class="mycard-col">
          <div class="mycard-col__content">
            <span class="tender-name">Тендер №{{ tender.id }} от {{ tender.date }} до {{ tender.end_date }}</span>
            <br>
            {{ tender.description }}
          </div>
        </div>
        <div class="mycard-col">
          <div class="mycard-col__content">
            {{ tender.delivery_area }}, {{ tender.delivery_address }}
          </div>
        </div>
        <div class="mycard-col">
          <div class="mycard-col__content">
            {{ tender.first_price }} ₽
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import SideMenu from './SideMenu.vue';

export default {
  components: {
    SideMenu,
  },
  data() {
    return {
      tenders: [],
      user_id: 0,
      userType: null,
    }
  },
  created() {
    this.getUserType();
    axios.get('/user_info')
      .then(response => {
        this.user_id = response.data.user_id;
        console.log(this.user_id);
        this.fetchTenders()
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
    fetchTenders() {
      let apiPath = '';
      if (this.userType === 'customer') {
        apiPath = `/user_tenders/${this.user_id}`;
      } else if (this.userType === 'supplier') {
        apiPath = `/supplier_tenders/${this.user_id}`;
      }
      if (apiPath) {
        axios.get(apiPath)
          .then(response => {
            for (let tender of response.data) {
              let id = tender.id
              let date = new Date(tender.created_date_time).toLocaleDateString()
              let time = new Date(tender.start_date_time).toLocaleTimeString();
              let description = tender.description
              let end_date = new Date(tender.end_date_time).toLocaleDateString()
              let end_time = new Date(tender.end_date_time).toLocaleTimeString()
              let delivery_area = tender.delivery_area
              let delivery_address = tender.delivery_address
              let first_price = tender.first_price
              let title = tender.title

              delivery_address = delivery_address.charAt(0).toUpperCase() + delivery_address.slice(1);
              delivery_area = delivery_area.charAt(0).toUpperCase() + delivery_area.slice(1);

              this.tenders.push({
                id,
                date,
                time,
                description,
                end_date,
                end_time,
                delivery_area,
                delivery_address,
                first_price,
                title
              })
            }
            this.tenders.sort((a, b) => b.id - a.id)
          })
          .catch(error => {
            console.error(error)
          })
      }
    },

    goToTender(id) {
      const path = `/tender/${String(id)}`;
      this.$router.push(path);
    }

  }
}
</script>
