<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12 custom-form">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="name" class="form-label">Логин</label>
            <input type="text" class="form-control" id="name" v-model="login" placeholder="Введите Ваш логин"
              :class="{ 'is-invalid': submitted &&!login }" />
            <div v-if="submitted &&!login" class="invalid-feedback">
              Логин не может быть пустым
            </div>
          </div>
          <div class="mb-3">
            <label for="thepassword" class="form-label">Пароль</label>
            <input type="password" class="form-control" id="thepassword" v-model="password" placeholder="Введите Ваш пароль"
              :class="{ 'is-invalid': submitted &&!password }" />
            <div v-if="submitted &&!password" class="invalid-feedback">
              Пароль не может быть пустым
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Войти</button>
          &nbsp;
          <router-link to="/regist" class="btn btn-outline-primary" role="button">Зарегистрироваться</router-link>
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
      login: '',
      password: '',
      submitted: false,
      errorMessage: '',
    };
  },
  methods: {
    async onSubmit() {
      this.submitted = true;
      this.errorMessage = '';

      try {
        const response = await axios.post('/login', {
          login: this.login,
          password: this.password,
        });

        // Обработка успешного ответа
        console.log(response.data);
        this.$router.push('/');
        setTimeout(function() {
           location.reload();
         }, 2);
      } catch (error) {
        // Обработка ошибки
        console.error(error);
        this.errorMessage = 'Неверный логин или пароль';
      }
    },
  },
};
</script>
