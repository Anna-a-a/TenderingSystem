<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-12 custom-form">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="title_app" class="form-label">Название</label>
            <input v-model="title" type="text" class="form-control" id="title_app"
              placeholder="Введите название заявки">
          </div>
          <div class="mb-3">
            <label for="description">Описание</label>
            <textarea v-model="description" class="form-control" id="description" placeholder="Введите текст"
              rows="15"></textarea>
          </div>
          <div class="mb-3">
            <label for="first_price" class="form-label">Цена</label>
            <input v-model="first_price" type="text" class="form-control" id="first_price" placeholder="Введите цену"
              :class="{ 'is-invalid': formSubmitted && !validPrice }">
            <div v-if="formSubmitted && !validPrice" class="invalid-feedback">
              Цена должна содержать только цифры
            </div>
          </div>


          <div class="mb-3">
            <label for="delivery_area" class="form-label">Область поставки</label>
            <input v-model="delivery_area" type="text" class="form-control" id="delivery_area"
              placeholder="Введите название области">
          </div>
          <div class="mb-3">
            <label for="delivery_address" class="form-label">Место поставки</label>
            <input v-model="delivery_address" type="text" class="form-control" id="delivery_address"
              placeholder="Введите место поставки">
          </div>
          <div class="mb-3 d-flex justify-content-between">
            <div class="me-3">
              <label for="date-start">Дата начала:</label>
              <br>
              <input type="date" id="date-start" name="date-start" value="2024-01-01" min="2024-01-01" max="2100-12-31"
                v-model="start_date" />
              <br>
              <label for="date-time-start">Время начала:</label>
              <br>
              <input type="time" id="date-time-start" name="date-time-start" value="13:37" v-model="start_time" />
            </div>
            <div class="ms-auto">
              <label for="date-end">Дата окончания:</label>
              <br>
              <input type="date" id="date-end" name="date-end" value="2024-01-02" min="2024-01-01" max="2100-12-31"
                v-model="end_date" />
              <br>
              <label for="date-time-end">Время окончания:</label>
              <br>
              <input type="time" id="date-time-end" name="date-time-end" value="13:37" v-model="end_time" />
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
      title: '',
      description: '',
      first_price: '',
      delivery_area: '',
      delivery_address: '',
      userType: null,
      user_id: null,
      formSubmitted: false,
    };
  },
  computed: {
    validPrice() { // Добавлено для валидации цены
      const priceRegex = /^\d+$/; // Регулярное выражение для проверки, что цена состоит только из цифр
      return priceRegex.test(this.first_price);
    }
  },
  methods: {
    submitForm() {
      this.formSubmitted = true;
      if (!this.validPrice) {
        // Здесь можно добавить логику для отображения ошибки, если цена не проходит валидацию
        return;
      }
      const currentDate = new Date();
      const formattedDate = currentDate.toISOString().slice(0, 19).replace('T', ' ');
      const dateTimeStart = this.start_date + ' ' + this.start_time + ':00';
      const dateTimeEnd = this.end_date + ' ' + this.end_time + ':00';

      const formData = {
        tender_status: "open",
        description: this.description,
        start_date_time: formattedDate,
        user_id: this.user_id,
        created_date_time: dateTimeStart,
        end_date_time: dateTimeEnd,
        first_price: this.first_price,
        title: this.title,
        delivery_address: this.delivery_address,
        delivery_area: this.delivery_area,
      };

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
