<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 custom-form">
                <form>
                    <div class="mb-3">
                        <label for="surname" class="form-label">ФИО</label>
                        <input type="text" class="form-control" id="surname" placeholder="Введите Ваши ФИО">
                    </div>
                    <div class="mb-3">
                        <label for="mail" class="form-label">Почта</label>
                        <input type="text" class="form-control" id="mail" placeholder="Введите Ваш e-mail">
                    </div>
                    <div class="mb-3">
                        <label for="login" class="form-label">Логин</label>
                        <input type="text" class="form-control" id="login" placeholder="Введите логин">
                    </div>
                    <div class="mb-3">
                        <label for="thepassword1" class="form-label">Пароль</label>
                        <input type="password" class="form-control" id="thepassword1" placeholder="Введите пароль"> 
                    </div>
                    <div class="mb-3">
                        <label for="thepassword2" class="form-label">Подтвердите пароль</label>
                        <input type="password" class="form-control" id="thepassword2" placeholder="Повторите пароль"> 
                    </div>
                    <button type="submit" class="btn btn-primary">Зарегестрироваться</button>
                </form>
            </div>
        </div>
    </div>
</template>