<template>
    <div class="container">
       <div class="row justify-content">
         <div class="col-md-12 custom-form">
           <form @submit.prevent="onSubmit">
             <div class="mb-3">
               <label for="name" class="form-label">Логин</label>
               <input
                 type="text"
                 class="form-control"
                 id="name"
                 v-model="login"
                 placeholder="Введите Ваш логин"
               />
             </div>
             <div class="mb-3">
               <label for="thepassword" class="form-label">Пароль</label>
               <input
                 type="password"
                 class="form-control"
                 id="thepassword"
                 v-model="password"
                 placeholder="Введите Ваш пароль"
               />
             </div>
             <div v-if="errorMessage" class="alert alert-danger" role="alert">
              {{ errorMessage }}
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
       };
    },
    methods: {
       async onSubmit() {
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
           // Здесь вы можете показать сообщение об ошибке пользователю
           this.errorMessage = 'Неверный логин или пароль';
         }
       },
    },
   };
   </script>
   