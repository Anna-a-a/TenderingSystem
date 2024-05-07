<template>
  <div class="side-menu">
    <router-link to="/profile">Личные данные</router-link>
    <router-link to="/mytenders">Мои тендеры</router-link>
    <router-link to="/myresponse">Ответы по заявкам</router-link>
    <a @click="showModal = true">Выйти из профиля</a>

    <!-- Модальное окно -->
    <div v-if="showModal" class="modal">
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
</template>

<script>
import Cookies from 'js-cookie';

export default {
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    removeCookies() {
      Cookies.remove('auth');
      this.$router.push('/auth');
      setTimeout(() => {
        location.reload();
      }, 20);
    },
  },
};
</script>

<style scoped>
.side-menu {
  position: fixed;
  margin-left: 27px;
  margin-top: 10px;
  border-radius: 10px;
  width: 230px;
  background-color: #343a40;
  color: #fff;
  padding: 20px 20px;
}

.side-menu ul {
  list-style-type: none;
  padding: 0;
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

.side-menu a {
  cursor: pointer;
}
</style>
