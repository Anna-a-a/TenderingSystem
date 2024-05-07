<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/">TenderingSystem</a>
        <form class="form-inline my-2 my-lg-0 d-flex justify-content-between w-100">
            <input class="form-control flex-grow-1" type="search" placeholder="Поиск" aria-label="Search" v-model="searchQuery" @input="searchTenders">
            <button class="btn btn-outline-info my-2 my-sm-0" type="submit" style="margin-left: 10px;" @click="clearSearch">Очистить поиск <i class="fa-solid fa-eraser"></i></button>
            <router-link to="/create" v-if="userType == 'customer'">
                <button class="btn btn-outline-info my-2 my-sm-0 ml-2 btn-add"><i class="fa-solid fa-plus"></i></button>
            </router-link>
        </form>
        <div class="px-3">
          <template v-if="!userType">
            <router-link to="/auth"><button class="round"><i class="fa-solid fa-user"></i></button></router-link>
          </template>
          <template v-else>
            <router-link to="/profile"><button class="round"><i class="fa-solid fa-user"></i></button></router-link>
          </template>
        </div>
    </div>
  </nav>
  <div class="container mt-5" v-if="searchQuery != ''">
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
    <div class="noresult" v-else><strong v-if="searchQuery.length > 2">Ничего не найдено <i class="fa-solid fa-face-sad-tear"></i></strong></div>
  </div>
  <router-view v-else></router-view>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tenders: [],
      searchQuery: '',
      userType: null,
    }
  },
  methods: {
    async searchTenders() {
      if (this.searchQuery.length < 2) {
        this.tenders = [];
        return;
      }

      const response = await fetch(`/tenders?search=${this.searchQuery}`);
      const data = await response.json();

      // Очищаем массив tenders перед добавлением результатов поиска
      this.tenders = [];

      for (let tender of data) {
        let id = tender.id
        let date = new Date(tender.created_data_time).toLocaleDateString()
        let time = new Date(tender.start_data_time).toLocaleTimeString();
        let description = tender.description
        let end_date = new Date(tender.end_data_time).toLocaleDateString()
        let end_time = new Date(tender.end_data_time).toLocaleTimeString()
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
    },
    goToTender(id) {
      const path = `/tender/${String(id)}`;
      this.$router.push(path);
      this.searchQuery = '';
    },
    async getUserType() {
      try {
        const response = await axios.get('/user_info'); 
        this.userType = response.data.user_type; 
      } catch (error) {
        console.error(error);
      }
    },
    clearSearch() {
    this.searchQuery = '';
  },
  },
  created() {
    this.getUserType();
  }
}
</script>
