-- Вставка начальных данных в таблицу tender_state
INSERT INTO tender_state(description)
VALUES ('создан'),
       ('ожидает заявок'),
       ('закончен');

-- Вставка начальных данных в таблицу tender_user
INSERT INTO tender_user(name, login, password_hash)
VALUES ('Владимир Владимирович Влидимирлв', 'company_ceo', '9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05');

-- Вставка начальных данных в таблицу supplier
INSERT INTO supplier(name)
VALUES ('OOO Подрядчик1'),
       ('OOO Подрядчик2');

-- Вставка начальных данных в таблицу tender
INSERT INTO tender(tender_status_id, description, start_date_time, end_date_time, user_id, first_price, title, delivery_address, delivery_area)
VALUES (2, 'Проектирование, монтаж и обслуживание сигнализации, пожароохранных, контрольно-пропускных систем и оборудования', '2024-03-15 15:00:00','2024-03-20 15:00:00', 1, 1230, 'Проектирование', 'пгниу', 'Пермский край'),
       (3, 'Монтаж и обслуживание сигнализации, пожароохранных, контрольно-пропускных систем и оборудования', '2021-09-27 12:00:00', '2021-10-27 12:00:00', 1, 12302002, 'Монтаж', 'пгниу', 'Пермский край');

-- Вставка начальных данных в таблицу tender_supplier
INSERT INTO tender_supplier(tender_id, supplier_id, price, is_winner)
VALUES (1 , 1, 100000, 'false'),
       (2 , 2, 1000500, 'true');