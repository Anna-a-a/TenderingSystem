<template>
  <div>
    <SideMenu />
    <div class="container">
      <h1 style="text-align: center;">Ответы по заявкам</h1>
      <div v-if="responseData.length > 0">
        <p v-for="(response, index) in responseData" :key="index" class="responseans">
          Вы победили в тендере "{{ response.title }}". Мы передали заказчику ваши контактные данные, ожидайте ответа на почту, которая указана в личном кабинете.
        </p>
      </div>
      <p v-else-if="user_id === 0 && !loading">Загрузка данных...</p>
      <p class="no-info" v-else-if="!loading">Нет данных</p>
    </div>
  </div>
</template>

<script>
import SideMenu from './SideMenu.vue';
import axios from 'axios';

export default {
  components: {
    SideMenu,
  },
  data() {
    return {
      responseData: [],
      user_id: 0,
      userType: null,
      loading: true,
    };
  },
  async created() {
    await this.getUserInfo();

    if (this.user_id !== 0) {
      const tenderResponse = await axios.get(`/responses_to_requests/${this.user_id}`);
      this.responseData = tenderResponse.data;
      console.log(this.responseData);
    }

    setTimeout(() => {
      this.loading = false;
    }, 30);
  },

  methods: {
    async getUserInfo() {
      try {
        const response = await axios.get('/user_info');
        this.user_id = response.data.user_id;
        this.userType = response.data.user_type;
        console.log(this.user_id);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
