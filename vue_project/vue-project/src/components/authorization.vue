<template>
    <div class="container">
        <div class="row justify-content">
            <div class="col-md-12 custom-form">
                <form>
                    <div class="mb-3">
                        <label for="name" class="form-label">Логин</label>
                        <input type="text" class="form-control" id="name" placeholder="Введите Ваш логин"> </div>
                    <div class="mb-3">
                        <label for="thepassword" class="form-label">Пароль</label>
                        <input type="password" class="form-control" id="thepassword" placeholder="Введите Ваш пароль"> 
                    </div>
                    <button type="submit" class="btn btn-primary">Войти</button> 
                    &nbsp<router-link to="/regist" class="btn btn-outline-primary" role="button">К Регистрации</router-link>
                </form>
            </div>
        </div>
    </div>
</template>