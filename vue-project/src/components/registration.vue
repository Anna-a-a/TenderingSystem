<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-12 custom-form">
          <form @submit.prevent="onSubmit">
            <div class="mb-3">
              <label for="surname" class="form-label">ФИО</label>
              <input
                type="text"
                class="form-control"
                id="surname"
                v-model="name"
                placeholder="Введите Ваши ФИО"
              />
            </div>
            <div class="mb-3">
              <label for="mail" class="form-label">Почта</label>
              <input
                type="text"
                class="form-control"
                id="mail"
                v-model="email"
                placeholder="Введите Ваш e-mail"
              />
            </div>
            <div class="mb-3">
              <label for="login" class="form-label">Логин</label>
              <input
                type="text"
                class="form-control"
                id="login"
                v-model="username"
                placeholder="Введите логин"
              />
            </div>
            <div class="mb-3">
              <label for="thepassword1" class="form-label">Пароль</label>
              <input
                type="password"
                class="form-control"
                id="thepassword1"
                v-model="password"
                placeholder="Введите пароль"
              />
            </div>
            <button type="submit" class="btn btn-primary">Зарегестрироваться</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        name: '',
        username: '',
        user_type: '',
        password: '',
        email: ''
      };
    },
    methods: {
      onSubmit() {
        const formData = {
          name: this.name,
          login: this.username, // Используйте this.username вместо this.login
          user_type: "supplier",
          password: this.password,
          email: this.email,
        };
  
        axios.post('/registration', formData)
          .then(response => {
            console.log(response);
            // Очистить форму после успешной отправки
            this.name = '';
            this.username = '';
            this.password = '';
            this.email = '';
          })
  
          .catch(error => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response);
          });
      }
    }
  };
  </script>
  