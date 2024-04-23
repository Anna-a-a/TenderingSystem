<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 custom-form">
                <form>
                    <div class="mb-3">
                        <label for="name" class="form-label">Название</label>
                        <input type="text" class="form-control" id="name" placeholder="Введите название заявки"> </div>
                    <div class="mb-3">
                        <label for="descriprion">Описание</label>
                        <textarea class="form-control" id="descriprion" placeholder="Введите текст" rows="15"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="price" class="form-label">Цена</label>
                        <input type="text" class="form-control" id="price" placeholder="Введите цену"> 
                    </div>
                    <div class="mb-3">
                        <label for="area" class="form-label">Область поставки</label>
                        <input type="text" class="form-control" id="area" placeholder="Введите название области"> 
                    </div>
                    <div class="mb-3">
                        <label for="place" class="form-label">Место поставки</label>
                        <input type="text" class="form-control" id="place" placeholder="Введите место поставки"> 
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
        </div>
    </div>
</template>