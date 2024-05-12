<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12 custom-form">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="title_app" class="form-label">Название</label>
            <input v-model="title" type="text" class="form-control" id="title_app" placeholder="Введите название заявки"
              maxlength="30" :class="{ 'is-invalid': formSubmitted && !title }">
            <div v-if="formSubmitted && !title" class="invalid-feedback">
              Поле не может быть пустым
            </div>
          </div>
          <div class="mb-3">
            <label for="description">Описание</label>
            <textarea v-model="description" class="form-control" id="description" placeholder="Введите текст" rows="15"
              maxlength="1000" :class="{ 'is-invalid': formSubmitted && !description }"></textarea>
            <div v-if="formSubmitted && !description" class="invalid-feedback">
              Поле не может быть пустым
            </div>
          </div>
          <div class="mb-3">
            <label for="first_price" class="form-label">Цена</label>
            <input type="number" class="form-control" placeholder="Цена" id="first_price" v-model="first_price"
              @input="limitInputLength" :class="{ 'is-invalid': formSubmitted && !first_price }">
            <div v-if="formSubmitted && !price" class="invalid-feedback">
              Поле не может быть пустым
            </div>
          </div>
          <div class="mb-3">
            <label for="delivery_area" class="form-label">Область поставки</label>
            <input v-model="delivery_area" type="text" class="form-control" id="delivery_area" maxlength="70"
              placeholder="Введите название области" :class="{ 'is-invalid': formSubmitted && !delivery_area }">
            <div v-if="formSubmitted && !delivery_area" class="invalid-feedback">
              Поле не может быть пустым
            </div>
          </div>
          <div class="mb-3">
            <label for="delivery_address" class="form-label">Место поставки</label>
            <input v-model="delivery_address" type="text" class="form-control" id="delivery_address" maxlength="70"
              placeholder="Введите место поставки" :class="{ 'is-invalid': formSubmitted && !delivery_address }">
            <div v-if="formSubmitted && !delivery_address" class="invalid-feedback">
              Поле не может быть пустым
            </div>
          </div>
          <div class="mb-3 d-flex justify-content-between">
            <div class="me-3">
              <label for="date-start">Дата начала:</label>
              <br>
              <input type="date" id="date-start" name="date-start" min="2024-01-01" max="2100-12-31"
                v-model="start_date" required/>
              <br>
              <label for="date-time-start">Время начала:</label>
              <br>
              <input type="time" id="date-time-start" name="date-time-start" v-model="start_time" required/>
            </div>
            <div class="ms-auto">
              <label for="date-end">Дата окончания:</label>
              <br>
              <input type="date" id="date-end" name="date-end" min="2024-01-01" max="2100-12-31"
                v-model="end_date" required/>
              <br>
              <label for="date-time-end">Время окончания:</label>
              <br>
              <input type="time" id="date-time-end" name="date-time-end" v-model="end_time" required/>
            </div>
          </div>

          <button type="submit" class="btn btn-primary" style="margin-bottom: 30px;">Отправить</button>

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
      userType: null,
      user_id: null,
      formSubmitted: false,
    };
  },
  methods: {
    limitInputLength(event) {
      const inputValue = event.target.value;
      const maxLength = 12;

      // Удалить все символы, которые не являются цифрами
      const numericValue = inputValue.replace(/\D/g, '');

      // Обрезать значение до максимальной длины
      if (numericValue.length > maxLength) {
        event.target.value = numericValue.slice(0, maxLength);
      } else {
        event.target.value = numericValue;
      }
    },
    submitForm() {
      this.formSubmitted = true;
      const currentDate = new Date();
      const formattedDate = currentDate.toISOString().slice(0, 19).replace('T', ' ');
      const dateTimeStart = this.start_date + ' ' + this.start_time + ':00';
      const dateTimeEnd = this.end_date + ' ' + this.end_time + ':00';

      const formData = {
        tender_status: "open",
        description: this.description,
        start_date_time: dateTimeStart,
        user_id: this.user_id,
        first_price: this.first_price.toString(),
        title: this.title,
        delivery_address: this.delivery_address,
        delivery_area: this.delivery_area,
        created_date_time: formattedDate,
        end_date_time: dateTimeEnd,
      };
      console.log(formData)
      axios.post('/send_tender_info', formData)
        .then(response => {
          console.log(response);
          // Очистить форму после успешной отправки
          this.title = '';
          this.description = '';
          this.first_price = '';
          this.delivery_area = '';
          this.delivery_address = '';
          this.start_date = '';
          this.start_time = '';
          this.end_date = '';
          this.$router.push('/');
        })

        .catch(error => {
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response);
        });
    },
    async getUserType() {
      try {
        const response = await axios.get('/user_info');
        this.userType = response.data.user_type;
        this.user_id = response.data.user_id;
      } catch (error) {
        console.error(error);
      }
    }
  },
  created() {
    this.getUserType();
  },
  watch: {
    userType(newVal) {
      if (newVal != 'customer') {
        this.$router.push('/forbidden');
      }
    }
  }
};
</script>