<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12 custom-form">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="surname" class="form-label">Название компании</label>
            <input type="text" class="form-control" id="surname" v-model="name" placeholder="Введите название компании" maxlength="50"
              :class="{ 'is-invalid': submitted && !name }" />
            <div v-if="submitted && !name" class="invalid-feedback">
              Поле не может быть пустым!
            </div>
          </div>
          <div class="mb-3">
            <label for="mail" class="form-label">Почта</label>
            <input type="text" class="form-control" id="mail" v-model="email" placeholder="Введите Ваш e-mail" maxlength="30"
              :class="{ 'is-invalid': submitted && !validEmail }" />
            <div v-if="submitted && !validEmail" class="invalid-feedback">
              Введите корректный адрес электронной почты
            </div>
          </div>
          <div class="mb-3">
            <label for="login" class="form-label">Логин</label>
            <input type="text" class="form-control" id="login" v-model="username" placeholder="Введите логин" maxlength="20"
              :class="{ 'is-invalid': submitted && !validUsername }" />
            <div v-if="submitted && !validUsername" class="invalid-feedback">
              Логин должен содержать только латинские буквы или цифры
            </div>
          </div>
          <div class="mb-3">
            <label for="thepassword1" class="form-label">Пароль</label>
            <input type="password" class="form-control" id="thepassword1" maxlength="30" v-model="password"
              placeholder="Введите пароль" :class="{ 'is-invalid': submitted && !validPassword }" />
            <div v-if="submitted && !validPassword" class="invalid-feedback">
              Пароль должен содержать не менее 6 символов
            </div>
          </div>
          <div class="mb-3">
            <label for="thepassword2" class="form-label">Подтверждение пароля</label>
            <input type="password" class="form-control" id="thepassword2" maxlength="30" v-model="passwordConfirmation"
              placeholder="Подтвердите пароль" :class="{ 'is-invalid': submitted && !validPasswordConfirmation }" />
            <div v-if="submitted && !validPasswordConfirmation" class="invalid-feedback">
              Пароли не совпадают
            </div>
          </div>
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
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
      submitted: false,
      errorMessage: '',
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
    validUsername() {
      const usernameRegex = /^[a-zA-Z\d]+$/;
      return usernameRegex.test(this.username);
    }
  },
  methods: {
    onSubmit() {
      this.submitted = true;

      if (!this.validUsername || !this.validEmail || !this.validPassword || !this.validPasswordConfirmation || !this.name) {
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
          if (response.data === 'Login already exists') {
            throw new Error('Login already exists');
          }
          else if (response.data === 'Email already exists') {
            throw new Error('Email already exists');
          }
          else {
            this.name = '';
            this.username = '';
            this.password = '';
            this.passwordConfirmation = '';
            this.email = '';
            this.submitted = false;
            this.$router.push('/auth');
          }
        })
        .catch(error => {
          if (error.message === 'Login already exists') {
            this.loginExists = true;
            this.submitted = true;
            this.errorMessage = 'Этот логин уже занят.';
          }
          else if (error.message === 'Email already exists') {
            this.EmailExists = true;
            this.submitted = true;
            this.errorMessage = 'На эту почты уже зарегистрирован другой аккаунт.';
          }
          else {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response);
          }
        });
    }
  }
};
</script>