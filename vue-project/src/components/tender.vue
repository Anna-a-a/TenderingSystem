<template>
  <div class="container">
    <div v-if="tender">
      <div class="tender-card">
        <p class="overflow-text">
        <h4>{{ tender.title }}</h4>
        </p>
        <p class="overflow-text"><i class="fa-solid fa-location-dot red"></i> {{ tender.delivery_area }}, {{
      tender.delivery_address }}</p>
        <p class="overflow-text"><i class="fa-regular fa-calendar"></i> {{ tender.date }} ({{ tender.time }}) - {{
      tender.end_date }} ({{ tender.end_time }})</p>
        <p class="overflow-text">Цена: {{ tender.first_price }} <i class="fa-solid fa-ruble-sign"></i></p>
        <p class="overflow-text">{{ tender.description }}</p>
        <div v-if="userType == 'supplier'">
          <button class="mybtn" @click="goToAnswerPage(tender.id)">Участвовать</button>
        </div>
      </div>
      <div class="tender-card-participants" v-if="userType == 'customer'">
        <div class="tender-card-participants__head">Список участников</div>
        <div class="tender-card-participants__body" v-for="(participant, index) in tender.supplier_logins" :key="index">
          <div v-if="participant">
            <div class="tender-card-participants__body-info">Пользователь: {{ participant }}</div>
            <div class="tender-card-participants__body-info">Компания/ИП: {{ tender.supplier_names[index] }}</div>
            <div class="tender-card-participants__body-info">Цена: {{ tender.supplier_prices[index] }} <i
                class="fa-solid fa-ruble-sign"></i></div>
            <button class="mybtn" @click="openModalForWinner(participant, tender.id)">Выбрать как победителя</button>
          </div>
          <div v-else>
            <div class="tender-card-participants__body-info">Участников пока нет</div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Тендер не найден</p>
    </div>

    <div v-if="showModal" class="modal1">
      <div class="modal-content1">
        <h4>Подтверждение</h4>
        <p>Вы уверены, что хотите выбрать этого участника ({{ selectedWinner.login }}) как победителя?</p>
        <div class="modal-buttons1">
          <button @click="closeModal">Отмена</button>
          <button @click="confirmWinner">Подтвердить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['id'],
  data() {
    return {
      tender: null,
      userType: null,
      login: '',
      showModal: false, // Добавлено состояние модального окна
      selectedWinner: null, // Добавлено состояние для выбранного победителя
    }
  },
  created() {
    this.getUserType();
    this.fetchTender();
    axios.get('/user_info')
      .then(response => {
        this.login = response.data.login;
      })
      .catch(error => {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response);
      });
  },
  methods: {
    async getUserType() {
      try {
        const response = await axios.get('/user_info');
        this.userType = response.data.user_type;
      } catch (error) {
        console.error(error);
      }
    },
    fetchTender() {
      const id = this.id;
      const url = `/tenders_suppliers/${id}`;
      axios.get(url)
        .then(response => {
          this.tender = response.data;
          console.log(this.tender);
          if (!this.tender) {
            this.tender = null;
          }
          else {
            this.tender.date = new Date(this.tender.created_date_time).toLocaleDateString();
            this.tender.time = new Date(this.tender.start_date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            this.tender.end_date = new Date(this.tender.end_date_time).toLocaleDateString();
            this.tender.end_time = new Date(this.tender.end_date_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            this.tender.delivery_address = this.tender.delivery_address.charAt(0).toUpperCase() + this.tender.delivery_address.slice(1);
            this.tender.delivery_area = this.tender.delivery_area.charAt(0).toUpperCase() + this.tender.delivery_area.slice(1);
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    goToAnswerPage(id) {
      this.$router.push(`/tender/${id}/response`);
    },
    openModalForWinner(login, id) {
      this.selectedWinner = { login, id };
      this.openModal();
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    confirmWinner() {
      const { login, id } = this.selectedWinner;
      const formData = {
        login: login,
        tender_id: id,
      };
      axios.post('/tender_winner', formData)
        .then(response => {
          console.log(response.data);
          setTimeout(() => {
        location.reload(); // Обновляем страницу через 3 секунды
      }, 30);
          this.closeModal(); // Закрываем модальное окно после подтверждения
        })
        .catch(error => {
          console.error(error);
          this.closeModal(); // Закрываем модальное окно в случае ошибки
        });
    },
  }
}
</script>

<style>
.modal1 {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.modal-content1 {
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

.modal-buttons1 {
  /* justify-content: center; */
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 20px;
}

.modal-buttons1 button {
  flex-grow: 1;
  margin-right: 10px;
  cursor: pointer;
  color: black;
  background-color: #c1d5f5;
  border: none;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.modal-buttons1 button:last-child {
  margin-right: 0px;
}

.modal-buttons1 button:hover {
  background-color: #98baf0;
}

</style>