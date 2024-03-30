CREATE TYPE tender_state AS ENUM ('open', 'in progress', 'closed');
CREATE TYPE user_type AS ENUM ('customer', 'supplier');

-- Создание таблицы tender_user
CREATE TABLE tender_system_user (
    id bigserial not null primary key,
    name text not null,
    login text not null unique,
    user_type user_type not null,
    password_hash text not null,
    email text not null unique
);
COMMENT ON TABLE tender_system_user IS 'System users';
COMMENT ON COLUMN tender_system_user.id IS 'Id of user';
COMMENT ON COLUMN tender_system_user.name IS 'Name of user';
COMMENT ON COLUMN tender_system_user.login IS 'Login name of user';
COMMENT ON COLUMN tender_system_user.user_type IS 'Type of user';
COMMENT ON COLUMN tender_system_user.password_hash IS 'Password hash';
COMMENT ON COLUMN tender_system_user.email IS 'Email';

-- Создание таблицы tender
CREATE TABLE tender (
    id bigserial not null primary key,
    tender_status tender_state NOT NULL,
    description text not null,
    created_date_time TIMESTAMP not null default current_date,
    start_date_time TIMESTAMP not null,
    end_date_time TIMESTAMP,
    user_id bigint not null references tender_system_user,
    first_price bigint not null,
    title text not null,
    delivery_address text not null,
    delivery_area text not null
);
COMMENT ON TABLE tender IS 'Tenders info';
COMMENT ON COLUMN tender.id IS 'Id of tender';
COMMENT ON COLUMN tender.tender_status IS 'Id of the tender state';
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
    supplier_id bigint not null references tender_system_user,
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
    file_name text not null,
    file_hash text
);
COMMENT ON TABLE tender_documents IS 'Tender documents';
COMMENT ON COLUMN tender_documents.id IS 'Id of document';
COMMENT ON COLUMN tender_documents.tender_id IS 'Id of tender';
COMMENT ON COLUMN tender_documents.file_name IS 'Filename of document';
COMMENT ON COLUMN tender_documents.file_hash IS 'Document hash';
