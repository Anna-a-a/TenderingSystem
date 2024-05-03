@ -0,0 +1,38 @@
<template>
    <div class="container">
        <div class="menu">
            <router-link to="/profile">Личные данные</router-link>
            <router-link to="/mytenders">Мои тендеры</router-link>
            <router-link to="/myresponse">Ответы по заявкам</router-link>
        </div>
    <div style="margin-left: 300px; padding: 20px;">
        <div class="card mb-3" >
                <div class="card-header d-flex justify-content-between">
                <span>Тендер № [номер] от [дата]</span>
                <span>Место поставки: [область], [адрес]</span>
                </div>
                <div class="card-body">
                  [описание тендера]
                </div>
                <div class="card-footer d-flex justify-content-between">
                  <span class="text-muted">Окончание (МСК): [дата] [время] </span>
                  <span>Цена: [цена] ₽</span>
                </div>
        </div>
        <h1>Участники:</h1>
        <div class="container mt-3">
        <div class="row">
            <div class="col-md-12">
            <div class="card mb-3" >
                <div class="card-body d-flex justify-content-between">
                    <span> [Подрядчик] </span>
                    <span>Цена: [цена] ₽</span>
                    <button type="button" class="btn btn-outline-dark">Выбрать как победителя</button>
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
    </div>
</template>