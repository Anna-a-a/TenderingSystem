<template>
  <div class="container">
    <div class="menu">
      <router-link to="/profile">Личные данные</router-link>
      <router-link to="/mytenders">Мои тендеры</router-link>
      <router-link to="/myresponse">Ответы по заявкам</router-link>
    </div>
    <div style="margin-left: 300px; padding: 20px;">
      <h1>Личные данные</h1>
      <div id="data">
        <div class="data-form">
          <div class="data-form-label">Логин:</div>
          <div class="data-form-field">
            <input type="text" v-model="login" :disabled="!editingLogin">
          </div>
          <div class="data-form-buttons">
            <button @click="editLogin" v-if="!editingLogin" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
            <button @click="saveLogin" v-if="editingLogin" class="btn-edit green"><i class="fa-solid fa-check"></i></button>
            <button @click="cancelEditLogin" v-if="editingLogin" class="btn-edit red"><i class="fa-solid fa-xmark"></i></button>
          </div>
        </div>
        <div class="data-form">
          <div class="data-form-label">Email:</div>
          <div class="data-form-field">
            <input type="email" v-model="email" :disabled="!editingEmail">
          </div>
          <div class="data-form-buttons">
            <button @click="editEmail" v-if="!editingEmail" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
            <button @click="saveEmail" v-if="editingEmail" class="btn-edit green"><i class="fa-solid fa-check"></i></button>
            <button @click="cancelEditEmail" v-if="editingEmail" class="btn-edit red"><i class="fa-solid fa-xmark"></i></button>
          </div>
        </div>
        <div class="data-form">
          <div class="data-form-label">ФИО:</div>
          <div class="data-form-field">
            <input type="text" v-model="name" :disabled="!editingName">
          </div>
          <div class="data-form-buttons">
            <button @click="editName" v-if="!editingName" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
            <button @click="saveName" v-if="editingName" class="btn-edit green"><i class="fa-solid fa-check"></i></button>
            <button @click="cancelEditName" v-if="editingName" class="btn-edit red"><i class="fa-solid fa-xmark"></i></button>
          </div>
        </div>
      </div>
      <div>
        <button class="mybtn" @click="removeCookies">Выйти</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  data() {
    return {
      email: '',
      name: '',
      login: '',
      editingEmail: false,
      editingName: false,
      editingLogin: false,
    }
  },
  async created() {
    try {
      const response = await axios.get('/user_info');
      this.email = response.data.email;
      this.name = response.data.name;
      this.login = response.data.login;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    removeCookies() {
      Cookies.remove('auth');
      // location.reload();
      this.$router.push('/auth');
      setTimeout(function() {
      location.reload();
    }, 20);
    },
    editEmail() {
      this.editingEmail = true;
    },
    saveEmail() {
      this.editingEmail = false;
    },
    cancelEditEmail() {
      this.editingEmail = false;
    },
    editName() {
      this.editingName = true;
    },
    saveName() {
      this.editingName = false;
    },
    cancelEditName() {
      this.editingName = false;
    },
    editLogin() {
      this.editingLogin = true;
    },
    saveLogin() {
      this.editingLogin = false;
    },
    cancelEditLogin() {
      this.editingLogin = false;
    }
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
