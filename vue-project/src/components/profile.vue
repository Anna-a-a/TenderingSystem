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
          Email:
          <input type="email" v-model="email" :disabled="!editingEmail">
          <button @click="editEmail" v-if="!editingEmail" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
          <button @click="saveEmail" v-if="editingEmail" class="btn-edit btn-edit__accept"><i class="fa-solid fa-check"></i></button>
          <button @click="cancelEditEmail" v-if="editingEmail" class="btn-edit btn-edit__cancel"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="data-form">
          Name:
          <input type="text" v-model="name" :disabled="!editingName">
          <button @click="editName" v-if="!editingName" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
          <button @click="saveName" v-if="editingName" class="btn-edit btn-edit__accept"><i class="fa-solid fa-check"></i></button>
          <button @click="cancelEditName" v-if="editingName" class="btn-edit btn-edit__cancel"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="data-form">
          Surname:
          <input type="text" v-model="surname" :disabled="!editingSurname">
          <button @click="editSurname" v-if="!editingSurname" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
          <button @click="saveSurname" v-if="editingSurname" class="btn-edit btn-edit__accept"><i class="fa-solid fa-check"></i></button>
          <button @click="cancelEditSurname" v-if="editingSurname" class="btn-edit btn-edit__cancel"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="data-form">
          Password:
          <input type="password" v-model="password" :disabled="!editingPassword">
          <button @click="editPassword" v-if="!editingPassword" class="btn-edit"><i class="fa-solid fa-pen-to-square"></i></button>
          <button @click="savePassword" v-if="editingPassword" class="btn-edit btn-edit__accept"><i class="fa-solid fa-check"></i></button>
          <button @click="cancelEditPassword" v-if="editingPassword" class="btn-edit btn-edit__cancel"><i class="fa-solid fa-xmark"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      email: "user@example.com",
      name: "John",
      surname: "Doe",
      password: "******",
      editingEmail: false,
      editingName: false,
      editingSurname: false,
      editingPassword: false
    }
  },
  methods: {
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
    editSurname() {
      this.editingSurname = true;
    },
    saveSurname() {
      this.editingSurname = false;
    },
    cancelEditSurname() {
      this.editingSurname = false;
    },
    editPassword() {
      this.editingPassword = true;
    },
    savePassword() {
      this.editingPassword = false;
    },
    cancelEditPassword() {
      this.editingPassword = false;
    }
  }
}
</script>
