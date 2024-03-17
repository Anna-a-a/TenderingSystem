-- Создание таблицы tender_state
CREATE TABLE tender_state (
    id bigserial not null primary key,
    description text not null
);
COMMENT ON TABLE tender_state IS 'Tender states';
COMMENT ON COLUMN tender_state.id IS 'Id of state';
COMMENT ON COLUMN tender_state.description IS 'Full description of state(for example: создан ожидает заявки)';

-- Создание таблицы tender_user
CREATE TABLE tender_user (
    id bigserial not null primary key,
    name text not null,
    login text not null,
    password_hash text not null
);
COMMENT ON TABLE tender_user IS 'System users';
COMMENT ON COLUMN tender_user.id IS 'Id of user';
COMMENT ON COLUMN tender_user.name IS 'Name of user';
COMMENT ON COLUMN tender_user.login IS 'Login name of user';
COMMENT ON COLUMN tender_user.password_hash IS 'Password hash';

-- Создание таблицы supplier
CREATE TABLE supplier (
    id bigserial not null primary key,
    name text not null
);
COMMENT ON TABLE supplier IS 'Suppliers';
COMMENT ON COLUMN supplier.id IS 'Id of supplier';
COMMENT ON COLUMN supplier.name IS 'Supplier name or name of supplier organization';

-- Создание таблицы tender
CREATE TABLE tender (
    id bigserial not null primary key,
    tender_status_id bigint not null references tender_state,
    description text not null,
    created_date_time TIMESTAMP not null default current_date,
    start_date_time TIMESTAMP not null,
    end_date_time TIMESTAMP,
    user_id bigint not null references tender_user,
    first_price bigint not null,
    title text not null,
    delivery_address text not null,
    delivery_area text not null
);
COMMENT ON TABLE tender IS 'Tenders info';
COMMENT ON COLUMN tender.id IS 'Id of tender';
COMMENT ON COLUMN tender.tender_status_id IS 'Id of the tender state';
COMMENT ON COLUMN tender.description IS 'Tender description';
COMMENT ON COLUMN tender.created_date_time IS 'Time of creating tender';
COMMENT ON COLUMN tender.start_date_time IS 'Time of starting tender';
COMMENT ON COLUMN tender.end_date_time IS 'Time of ending tender';
COMMENT ON COLUMN tender.user_id IS 'Id of user who created the tender';
COMMENT ON COLUMN tender.first_price IS 'Tender first price';
COMMENT ON COLUMN tender.title IS 'Title of tender';
COMMENT ON COLUMN tender.delivery_address IS 'Address of supply';
COMMENT ON COLUMN tender.delivery_area IS 'Area of supply';

-- Создание таблицы tender_supplier
CREATE TABLE tender_supplier (
    tender_id bigint not null references tender,
    supplier_id bigint not null references supplier,
    price bigint not null,
    is_winner boolean not null default false
);
COMMENT ON TABLE tender_supplier IS 'Tender-supplier info';
COMMENT ON COLUMN tender_supplier.tender_id IS 'Id of tender';
COMMENT ON COLUMN tender_supplier.supplier_id IS 'id of supplier';
COMMENT ON COLUMN tender_supplier.price IS 'Price of tender';
COMMENT ON COLUMN tender_supplier.is_winner IS 'Status of supplier';

-- Создание таблицы tender_documents
CREATE TABLE tender_documents (
    id SERIAL PRIMARY KEY,
    tender_id bigint not null references tender,
    file_name VARCHAR(255),
    file_data BYTEA
);
COMMENT ON TABLE tender_documents IS 'Tender documents';
COMMENT ON COLUMN tender_documents.id IS 'Id of document';
COMMENT ON COLUMN tender_documents.tender_id IS 'Id of tender';
COMMENT ON COLUMN tender_documents.file_name IS 'Filename of document';
COMMENT ON COLUMN tender_documents.file_data IS 'Document data';
