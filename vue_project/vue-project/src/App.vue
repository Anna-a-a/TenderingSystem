<script>
import axios from 'axios'

export default {
  data() {
    return {
      tenders: []
    }
  },
  created() {
    this.fetchTenders()
  },
  methods: {
    fetchTenders() {
      axios.get('/tenders')
        .then(response => {
          for (let tender of response.data) {
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
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a class="navbar-brand" href="#">BrandName</a>
        <form class="form-inline my-2 my-lg-0 d-flex justify-content-between w-100">
            <input class="form-control flex-grow-1" type="search" placeholder="Поиск" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0 mr-3" type="submit" style="margin-left: 10px;">Искать <i class="fa-solid fa-magnifying-glass"></i></button>
            <router-link to="/create" class="btn btn-primary ml-auto custom-btn" role="button">+</router-link>
        </form>
        <div class="px-3">
            <a href="your-page.html" class="button-link">
                <button class="round" title="Перейти на страницу пользователя">
                    <i class="fa-solid fa-user"></i>
                </button>
            </a>
        </div>
    </div>
</nav>
  <router-view></router-view>
</template>

<!-- <template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a class="navbar-brand" href="#">BrandName</a>
        <form class="form-inline my-2 my-lg-0 d-flex justify-content-between w-100">
            <input class="form-control flex-grow-1" type="search" placeholder="Поиск" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin-left: 10px;">Искать <i class="fa-solid fa-magnifying-glass"></i></button>
        </form>
        <div class="px-3">
            <button class="round"><i class="fa-solid fa-user"></i></button>
        </div>
    </div>
</nav>
<div class="container">
        <div class="row">
            <div class="form-check mr-4">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDisabled" disabled>
                <label class="form-check-label" for="flexCheckDisabled"> Filter 1 (disabled) </label>
            </div>
            <div class="form-check mr-4">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckCheckedDisabled" checked disabled>
                <label class="form-check-label" for="flexCheckCheckedDisabled"> Filter 2 (disabled) </label>
            </div>
            <div class="form-check mr-4">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckCheckedDisabled" checъъked disabled>
                <label class="form-check-label" for="flexCheckCheckedDisabled"> Filter 3 (disabled) </label>
            </div>
        </div>
        <div class="container mt-3">
        <div class="row">
            <div class="col-md-12">
            <div class="card mb-3" v-for="tender in tenders" :key="tender.id">
                <div class="card-header d-flex justify-content-between">
                <span>Тендер №{{ tender.id }} от {{ tender.date }}</span>
                <span>Место поставки: {{ tender.delivery_area }}, {{ tender.delivery_address }}</span>
                </div>
                <div class="card-body">
                {{ tender.description }}
                </div>
                <div class="card-footer d-flex justify-content-between">
                  <span class="text-muted">Окончание (МСК): {{ tender.end_date }} {{ tender.end_time }} </span>
                  <span>Цена: {{ tender.first_price }} ₽</span>
                </div>
            </div>
            </div>
        </div>
        </div>
        <div>
  </div>
  

</div>
</template> -->

<style scoped>

</style>
