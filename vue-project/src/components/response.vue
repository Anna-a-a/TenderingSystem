<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <form @submit.prevent="submitForm">
                    <div class="form-group">
                        <label for="price">Цена</label>
                        <input type="number" class="form-control" id="price" v-model="price" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    props: ['id'],
    data() {
        return {
            price: '',
            login: '',
        };
    },
    created() {
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
        submitForm() {
            const formData = {
                tender_id: this.id,
                price: this.price,
                login: this.login,
            };
            console.log(formData);
            axios.post('/supplier_response', formData)
                .then(response => {
                    console.log(response);
                    // Очистить форму после успешной отправки
                    this.price = '';
                    this.$router.push('/');
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
