<template>
  <div class="container">
      <div class="menu">
          <router-link to="/profile">Личные данные</router-link>
          <router-link to="/mytenders">Мои тендеры</router-link>
          <router-link to="/myresponse">Ответы по заявкам</router-link>
</div>
<div style="margin-left: 300px; padding: 20px;">
    <h1>Мои тендеры</h1>
    
    <div class="container mt-3">
    <div class="row">
        <div class="col-md-12">
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
              <router-link to="/participants" class="btn btn-secondary" role="button">Участники</router-link>
            </div>
        </div>
        </div>
    </div>
    </div>
</div>
</div>
</template>