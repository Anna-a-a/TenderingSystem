<template>
  <div>
    <SideMenu />
    <div class="container">
      <h1 style="text-align: center;">Ответы по заявкам</h1>

      <div v-if="loading" class="loading-container">
      <i class="fa-solid fa-spinner fa-spin"></i>
    </div>

      <div v-else-if="responseData.length > 0">
        <p v-for="(response, index) in responseData" :key="index" class="responseans">
          Вы победили в тендере "{{ response.title }}". Мы передали заказчику ваши контактные данные, ожидайте ответа на почту, которая указана в личном кабинете.
        </p>
      </div>

      <p class="no-info" v-else>Нет данных</p>
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
      this.loading = false;
    }
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
