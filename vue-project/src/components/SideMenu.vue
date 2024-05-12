<template>
  <div class="side-menu-container">
    <div class="button-container">
    <button class="side-menu-button" @click="toggleSideMenu">
      <i class="fa-solid fa-bars"></i>
    </button>
  </div>
    <div class="side-menu" v-if="showSideMenu">
      <router-link to="/">На главную</router-link>
      <router-link to="/profile">Личные данные</router-link>
      <router-link to="/mytenders">Мои тендеры</router-link>
      <router-link to="/myresponse" v-show="userTypeVuex=='supplier'">Ответы по заявкам</router-link>
      <a @click="showModal = true">Выйти из профиля</a>

      <!-- Модальное окно -->
      <div v-if="showModal" class="modal ">
        <div class="modal-content">
          <p>Вы уверены, что хотите выйти из профиля?</p>
          <div class="modal-buttons">
            <button @click="removeCookies">Да</button>
            <button @click="showModal = false">Нет</button>
          </div>
        </div>
      </div>
      <!-- /Модальное окно -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      showSideMenu: false,
      showModal: false,
    };
  },
  created() {
    this.$store.dispatch('getUserTypeVuex');
  },
  mounted() {
    // Проверяем, сохранено ли состояние меню в localStorage
    const sideMenuState = localStorage.getItem('sideMenuState');
    if (sideMenuState !== null) {
      this.showSideMenu = JSON.parse(sideMenuState);
    }
  },
  watch: {
    // Отслеживаем изменения showSideMenu и сохраняем их в localStorage
    showSideMenu(newValue) {
      localStorage.setItem('sideMenuState', JSON.stringify(newValue));
    },
  },
  methods: {
    toggleSideMenu() {
      this.showSideMenu = !this.showSideMenu;
    },
    removeCookies() {
      Cookies.remove('auth');
      this.$router.push('/auth');
      setTimeout(() => {
        location.reload();
      }, 20);
    },
  },
  computed: {
    ...mapState(['userTypeVuex']),
  },
};

</script>

<style scoped>

.side-menu-wrapper {
  position: fixed; /* Добавляем новый родительский элемент с position: fixed */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 999;
}

.button-container {
  margin-left: 25px; /* Отступ слева для кнопки */
}

.side-menu-container {
  position: absolute;
  margin-top: 14px;
  /* margin-left: 25px; */
  /* height: 66px; */
  top: 0;
  left: 0;
  z-index: 1000;
  background-color: #343a40;
}

.side-menu-button {
  outline: none;
  background-color: transparent;
  border: none;
  color: #fff;
  font-size: 25px;
  /* padding: 10px; */
  cursor: pointer;
}

.side-menu-button:hover {
  color: #c1d5f5;
}

.side-menu {
  position: absolute;
  left: 0;
  width: 230px;
  background-color: #343a40;
  color: #fff;
  padding: 20px 20px;
  transition: left 0.3s ease;
  border-radius: 0px 0px 20px 0px;
}

.side-menu a {
  color: #fff;
  text-decoration: none;
  display: block;
  padding: 10px;
}

.side-menu a:hover {
  background-color: #555;
}

.side-menu button {
  cursor: pointer;
  color: black;
  background-color: #c1d5f5;
  border: none;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.side-menu button:hover {
  background-color: #98baf0;
}

/* Модальное окно */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #343a40;
  color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  width: fit-content;
  max-width: 300px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 20px;
}

.modal-buttons button {
  flex-grow: 1;
  margin-right: 10px;
}

.modal-buttons button:last-child {
  margin-right: 0px;
}

.side-menu a {
  cursor: pointer;
}
</style>
