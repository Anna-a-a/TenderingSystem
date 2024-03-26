<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 custom-form">
                <form>
                    <div class="mb-3">
                        <label for="name2" class="form-label">Название фирмы</label>
                        <input type="text" class="form-control" id="name2" placeholder="Введите название"> </div>
                    <div class="mb-3">
                        <label for="price2" class="form-label">Цена</label>
                        <input type="text" class="form-control" id="price2" placeholder="Введите цену"> 
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="applicationAgreement">
                        <label class="form-check-label" for="applicationAgreement">Согласен с условиями</label>
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
        </div>
    </div>
</template>