-- Вставка начальных данных в таблицу tender_user
INSERT INTO tender_system_user(name, login, user_type, password_hash, email)
VALUES ('Владимир Владимирович Влидимирлв', 'company_ceo', 'customer' ,'9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05', 'pppp@gmail.com'),
        ('Александр Александрович А', 'company_2_employee', 'supplier' ,'9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05', 'cccpp@gmail.com'),
        ('Никитич никита никитов', 'ffjfkkf_90', 'supplier' ,'9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05', 'ppdxkdkp@gmail.com');



-- Вставка начальных данных в таблицу tender
INSERT INTO tender(tender_status, description, start_date_time, end_date_time, user_id, first_price, title, delivery_address, delivery_area)
VALUES ('in progress', 'Проектирование, монтаж и обслуживание сигнализации, пожароохранных, контрольно-пропускных систем и оборудования', '2024-03-15 15:00:00','2024-03-20 15:00:00', 1, 1230, 'Проектирование', 'пгниу', 'Пермский край'),
       ('closed', 'Монтаж и обслуживание сигнализации, пожароохранных, контрольно-пропускных систем и оборудования', '2021-09-27 12:00:00', '2021-10-27 12:00:00', 1, 12302002, 'Монтаж', 'пгниу', 'Пермский край');

-- Вставка начальных данных в таблицу tender_supplier
INSERT INTO tender_supplier(tender_id, supplier_id, price, is_winner)
VALUES (1 , 3, 100000, 'false'),
       (2 , 2, 1000500, 'true');