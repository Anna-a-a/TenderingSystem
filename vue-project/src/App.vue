<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/">TenderingSystem</a>
        <form class="form-inline my-2 my-lg-0 d-flex justify-content-between w-100">
            <input class="form-control flex-grow-1" type="search" placeholder="Поиск" aria-label="Search" v-model="searchQuery" @input="searchTenders">
            <button class="btn btn-outline-info my-2 my-sm-0" type="submit" style="margin-left: 10px;">Искать <i class="fa-solid fa-magnifying-glass"></i></button>
        </form>
        <div class="px-3">
          <template v-if="!$store.state.isAuthenticated">
            <router-link to="/auth"><button class="round"><i class="fa-solid fa-user"></i></button></router-link>
          </template>
          <template v-else>
            <router-link to="/profile"><button class="round"><i class="fa-solid fa-user"></i></button></router-link>
          </template>
        </div>
    </div>
  </nav>
  <div class="container mt-5" v-if="searchQuery != ''">
    <div class="row">
      <div class="col-md-4" v-for="tender in tenders" :key="tender.id">
        <div class="card mb-4">
          <div class="card-body card-body__search">
            <h5 class="card-title">{{ tender.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ tender.date }} / {{ tender.end_date }}</h6>
            <p class="card-text card-text__search">{{ tender.description }}</p>
            <p class="card-text"><strong>Область:</strong> {{ tender.delivery_area }}</p>
            <p class="card-text"><strong>Место:</strong> {{ tender.delivery_address }}</p>
            <p class="card-text"><strong>Начальная цена:</strong> {{ tender.first_price }} ₽</p>
            <router-link :to="'/tender/' + tender.id" class="btn btn-primary ">Подробнее</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
  <router-view v-else></router-view>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tenders: [],
      searchQuery: ''
    }
  },
  methods: {
    async searchTenders() {
      if (this.searchQuery.length < 1) {
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
          description,
          end_date,
          end_time,
          delivery_area,
          delivery_address,
          first_price,
          title
        })
      }
    }
  }
}
</script>
