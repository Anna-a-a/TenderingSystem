<template>
  <SideMenu />
  <div class="container">
    <h1 style="text-align: center;">Личные данные</h1>
    <div v-if="loading" class="loading-container">
      <i class="fa-solid fa-spinner fa-spin"></i>
    </div>

    <div id="data" v-else>
      <div class="data-form">
        <div class="data-form-label">Логин:</div>
        <div class="data-form-field">
          <input type="text" v-model="login" disabled>
        </div>
      </div>
      <div class="data-form">
        <div class="data-form-label">Email:</div>
        <div class="data-form-field">
          <input type="email" v-model="email" :disabled="!editingEmail" maxlength="30">
        </div>
        <div class="data-form-buttons">
          <button @click="editEmail" v-if="!editingEmail" class="btn-edit"><i
              class="fa-solid fa-pen-to-square"></i></button>
          <button @click="saveEmail" v-if="editingEmail" class="btn-edit green"><i
              class="fa-solid fa-check"></i></button>
          <button @click="cancelEditEmail" v-if="editingEmail" class="btn-edit red"><i
              class="fa-solid fa-xmark"></i></button>
        </div>
      </div>
      <div class="data-form">
        <div class="data-form-label">Компания:</div>
        <div class="data-form-field">
          <input type="text" v-model="name" :disabled="!editingName" maxlength="50">
        </div>
        <div class="data-form-buttons">
          <button @click="editName" v-if="!editingName" class="btn-edit"><i
              class="fa-solid fa-pen-to-square"></i></button>
          <button @click="saveName" v-if="editingName" class="btn-edit green"><i class="fa-solid fa-check"></i></button>
          <button @click="cancelEditName" v-if="editingName" class="btn-edit red"><i
              class="fa-solid fa-xmark"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import SideMenu from './SideMenu.vue';

export default {
  components: {
    SideMenu,
  },
  data() {
    return {
      email: '',
      name: '',
      login: '',
      editingEmail: false,
      editingName: false,
      user_id: 0,
      userType: null,
      emailError: null,
      previousName: '',
      previousEmail: '',
      loading: true,
    }
  },
  async created() {
    await this.getUserInfo();
  },
  methods: {
    async getUserInfo() {
      try {
        const response = await axios.get('/user_info');
        this.email = response.data.email;
        this.name = response.data.name;
        this.login = response.data.login;
        this.user_id = response.data.user_id;
        this.userType = response.data.user_type;
        this.loading = false;
      } catch (error) {
        console.error(error);
      }
    },
    removeCookies() {
      Cookies.remove('auth');
      this.$router.push('/auth');
      setTimeout(function () {
        location.reload();
      }, 20);
    },
    editEmail() {
      this.previousEmail = this.email;
      this.editingEmail = true;
    },
    async saveEmail() {
      this.editingEmail = false;

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.email)) {
      this.email = this.previousEmail;
      alert('Введите корректный адрес электронной почты');
      return;
    }

      try {
        const response = await axios.post(`/update_email`, {
          user_id: this.user_id,
          email: this.email
        });
        // здесь можно добавить обработку успешного ответа сервера, если нужно
      } catch (error) {
        if (error.response && error.response.status === 500) {
          this.email = this.previousEmail;
          alert('На эту почту уже зарегистрирован другой аккаунт');
        } else {
          console.error(error);
        }
      }
    },

    cancelEditEmail() {
      this.email = this.previousEmail;
      this.editingEmail = false;
    },
    editName() {
      this.previousName = this.name;
      this.editingName = true;
    },
    async saveName() {
      this.editingName = false;
      try {
        await axios.post(`/update_name`, {
          user_id: this.user_id,
          name: this.name
        });
      } catch (error) {
        console.error(error);
      }
    },
    cancelEditName() {
      this.name = this.previousName;
      this.editingName = false;
    },
  }
}
</script>

<style scoped>
.data-form {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 10px;
}

.data-form-label {
  width: 100px;
  text-align: right;
  margin-right: 10px;
}

.data-form-field {
  flex-grow: 1;
  margin-right: 10px;
}

.data-form-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.btn-edit {
  margin-right: 5px;
}
</style>
