CREATE TABLE tender_state (
	id bigserial not null primary key,
	description text not null
);
comment on table tender_state is "Tender states"
comment on column tender_state.id is 'Id of state';
comment on column tender_state.description is 'Full description of state(for example: создан ожидает заявки)';


CREATE TABLE tender_user (
	id bigserial not null primary key,
	name text not null,
	login text not null,
	password_hash text not null
);
comment on table tender_user is 'System users'
comment on column tender_user.id is 'Id of user';
comment on column tender_user.name is 'Name of user';
comment on column tender_user.login is 'Login name of user';
comment on column tender_user.password_hash is 'Password hash';


CREATE TABLE supplier (
	id bigserial not null primary key,
	name text not null
);
comment on table supplier is 'Suppliers'
comment on column supplier.id is 'Id of supplier';
comment on column supplier.name is 'Supplier name or name of supplier organization';


CREATE TABLE tender (
	id bigserial not null primary key,
	tender_status_id bigint not null references tender_state,
	description text not null,
	created_date_time TIMESTAMP not null default current_date,
	start_date_time TIMESTAMP not null,
	end_date_time TIMESTAMP,
	user_id bigint not null references tender_user
);
comment on table tender is 'Tenders info'
comment on column tender.id is 'Id of tender';
comment on column tender.tender_status_id is 'Id of the tender state';
comment on column tender.description is 'Tender description';
comment on column tender.created_date_time is 'Time of creating tender';
comment on column tender.start_date_time is 'Time of starting tender';
comment on column tender.end_date_time is 'Time of ending tender';
comment on column tender.user_id is 'Id of user who created the tender';


CREATE TABLE tender_supplier (
	tender_id bigint not null references tender,
	supplier_id bigint not null references supplier,
	price bigint not null,
	is_winner boolean not null default false
);
comment on table tender_supplier is 'Tender-supplier info';
comment on column tender_supplier.tender_id is 'Id of tender';
comment on column tender_supplier.supplier_id is 'id of supplier';
comment on column tender_supplier.price is 'Price of tender';
comment on column tender_supplier.is_winner is 'Status of supplier';


INSERT INTO tender_state(description)
VALUES ('создан'),
       ('ожидает заявок'),
       ('закончен');

INSERT INTO tender_user(name, login, password_hash)
VALUES ('Владимир Владимирович Влидимирлв', 'company_ceo', '9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05');


INSERT INTO supplier(name)
VALUES ('OOO Подрядчик1'),
       ('OOO Подрядчик2');


INSERT INTO tender(tender_status_id, description, start_date_time, user_id)
VALUES (2, 'Проектирование, монтаж и обслуживание сигнализации, пожароохранных, контрольно-пропускных систем и оборудования', '2021-09-27 15:00:00', 1);


INSERT INTO tender_supplier(tender_id, supplier_id, price)
VALUES (1 , 1, 100000),
       (1 , 2, 1000500);