<template>
  <div class="container">

    <div v-if="loading" class="loading-container">
      <i class="fa-solid fa-spinner fa-spin"></i>
    </div>

    <div v-else-if="filteredTenders.length == 0 && !userType" class="noresult">
      <strong>Вы не авторизовались <i class="fa-solid fa-face-sad-tear"></i></strong>
    </div>

    <div class="filter-container" v-else>
      <label class="checkbox style-c">
        <input type="checkbox" value="open" v-model="filterStatus" @click="updateFilterStatus('open')"/>
        <div class="checkbox__checkmark"></div>
        <div class="checkbox__body" >Открытые тендеры</div>
      </label>
      <label class="checkbox style-c">
        <input type="checkbox" value="in progress" v-model="filterStatus" @click="updateFilterStatus('in progress')"/>
        <div class="checkbox__checkmark"></div>
        <div class="checkbox__body" >Тендеры в процессе</div>
      </label>
      <label class="checkbox style-c">
        <input type="checkbox" value="closed" v-model="filterStatus" @click="updateFilterStatus('closed')"/>
        <div class="checkbox__checkmark"></div>
        <div class="checkbox__body" >Закрытые тендеры</div>
      </label>
    </div>
    <div class="mycard" v-if="sortedTenders.length > 0">
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
        <div class="mycard-col" v-if="filterStatus.length === 0">
          <div>
            Статус
          </div>
        </div>
        <div class="mycard-col">
          <div>
            Цена
          </div>
        </div>
      </div>
      <div class="mycard-body mycard-tender" v-for="tender in sortedTenders" :key="tender.id"
        @click="goToTender(tender.id)">
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
        <div class="mycard-col" v-if="filterStatus.length === 0">
          <div class="mycard-col__content" :class="getStatusClass(tender.status)">
            {{ getStatusName(tender.status) }} 
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

export default {
  data() {
    return {
      tenders: [],
      in_progress_tenders: [],
      closed_tenders: [],
      filterStatus: [],
      userType: '',
      loading: true,
    };
  },
  created() {
    this.getUserType();
    this.fetchTenders();
  },
  methods: {
    getStatusClass(status) {
    if (status === 'in progress') {
      return 'text-success';
    } else if (status === 'closed') {
      return 'text-danger';
    }
  },
    getStatusName(status) {
    if (status === 'open') {
      return 'Открыт';
    } else if (status === 'in progress') {
      return 'В процессе';
    } else if (status === 'closed') {
      return 'Закрыт';
    } else {
      return status;
    }
  },
    updateFilterStatus(status) {
      if (this.filterStatus.includes(status)) {
        this.filterStatus = this.filterStatus.filter(item => item !== status);
      } else {
        this.filterStatus = [status];
      }
    },
    async getUserType() {
      try {
        const response = await axios.get('/user_info');
        this.userType = response.data.user_type;
        console.log(1)
        console.log(response.data.user_type)
      } catch (error) {
        this.loading = false;
        console.error(error);
      }
    },
    fetchTenders() {
      axios.get('/tenders')
        .then(response => {
          for (let tender of response.data) {
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
            let status = tender.status

            description = description.charAt(0).toUpperCase() + description.slice(1);
            delivery_address = delivery_address.charAt(0).toUpperCase() + delivery_address.slice(1);
            delivery_area = delivery_area.charAt(0).toUpperCase() + delivery_area.slice(1);

            if (tender.status == 'open') {
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
                title,
                status,
              });
            } else if (tender.status == 'in progress') {
              this.in_progress_tenders.push({
                id,
                date,
                time,
                description,
                end_date,
                end_time,
                delivery_area,
                delivery_address,
                first_price,
                title,
                status,
              });
            } else {
              this.closed_tenders.push({
                id,
                date,
                time,
                description,
                end_date,
                end_time,
                delivery_area,
                delivery_address,
                first_price,
                title,
                status,
              });
            }
          }
          if (this.sortedTenders.length) {
            this.loading = false;
          }
        })
        .catch(error => {
          console.error(error)
        })
    },

    goToTender(id) {
      const path = `/tender/${String(id)}`;
      this.$router.push(path);
    }

  },
  computed: {
    filteredTenders() {
      if (this.filterStatus.length === 0) {
        return this.tenders.concat(this.in_progress_tenders, this.closed_tenders);
      }
      const filtered = [];
      if (this.filterStatus.includes('open')) {
        filtered.push(...this.tenders);
      }
      if (this.filterStatus.includes('in progress')) {
        filtered.push(...this.in_progress_tenders);
      }
      if (this.filterStatus.includes('closed')) {
        filtered.push(...this.closed_tenders);
      }
      return filtered;
    },
    sortedTenders() {
      return this.filteredTenders.sort((a, b) => b.id - a.id);
    }
  }
}
</script>
