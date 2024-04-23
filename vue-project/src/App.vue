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
        <a class="navbar-brand" href="/">BrandName</a>
        <form class="form-inline my-2 my-lg-0 d-flex justify-content-between w-100">
            <input class="form-control flex-grow-1" type="search" placeholder="Поиск" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit" style="margin-left: 10px;">Искать <i class="fa-solid fa-magnifying-glass"></i></button>
        </form>
        <div class="px-3">
            <router-link to="/profile"><button class="round"><i class="fa-solid fa-user"></i></button></router-link>
        </div>
    </div>
</nav>
  <router-view></router-view>
</template>

<style scoped>

</style>
