<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12 custom-form">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="surname" class="form-label">ФИО</label>
            <input type="text" class="form-control" id="surname" v-model="name" placeholder="Введите Ваши ФИО" />
          </div>
          <div class="mb-3">
            <label for="mail" class="form-label">Почта</label>
            <input type="text" class="form-control" id="mail" v-model="email" placeholder="Введите Ваш e-mail"
              :class="{ 'is-invalid': submitted && !validEmail }" />
            <div v-if="submitted && !validEmail" class="invalid-feedback">
              Введите корректный адрес электронной почты
            </div>
          </div>
          <div class="mb-3">
            <label for="login" class="form-label">Логин</label>
            <input type="text" class="form-control" id="login" v-model="username" placeholder="Введите логин"
              :class="{ 'is-invalid': submitted && !validUsername }" />
            <div v-if="submitted && !validUsername" class="invalid-feedback">
              Логин должен содержать только латинские буквы
            </div>
          </div>
          <div class="mb-3">
            <label for="thepassword1" class="form-label">Пароль</label>
            <input type="password" class="form-control" id="thepassword1" v-model="password"
              placeholder="Введите пароль" :class="{ 'is-invalid': submitted && !validPassword }" />
            <div v-if="submitted && !validPassword" class="invalid-feedback">
              Пароль должен содержать не менее 6 символов
            </div>
          </div>
          <div class="mb-3">
            <label for="thepassword2" class="form-label">Подтверждение пароля</label>
            <input type="password" class="form-control" id="thepassword2" v-model="passwordConfirmation"
              placeholder="Подтвердите пароль" :class="{ 'is-invalid': submitted && !validPasswordConfirmation }" />
            <div v-if="submitted && !validPasswordConfirmation" class="invalid-feedback">
              Пароли не совпадают
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
          &nbsp;
          <router-link to="/auth" class="btn btn-outline-primary" role="button">Вернуться к авторизации</router-link>
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
      passwordConfirmation: '',
      email: '',
      submitted: false
    };
  },
  computed: {
    validEmail() {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailRegex.test(this.email);
    },
    validPassword() {
      return this.password.length >= 6;
    },
    validPasswordConfirmation() {
      return this.password === this.passwordConfirmation;
    },
    validUsername() { // Добавлено для валидации логина
      const usernameRegex = /^[a-zA-Z]+$/; // Регулярное выражение для проверки, что логин состоит только из английских букв
      return usernameRegex.test(this.username);
    }
  },
  methods: {
    onSubmit() {
      this.submitted = true;

      if (!this.validUsername || !this.validEmail || !this.validPassword || !this.validPasswordConfirmation) {
        return;
      }

      const formData = {
        name: this.name,
        login: this.username,
        user_type: "supplier",
        password: this.password,
        email: this.email,
      };

      axios.post('/registration', formData)
        .then(response => {
          // console.log(response);
          // Очистить форму после успешной отправки
          this.name = '';
          this.username = '';
          this.password = '';
          this.passwordConfirmation = '';
          this.email = '';
          this.submitted = false;
          this.$router.push('/auth');
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
