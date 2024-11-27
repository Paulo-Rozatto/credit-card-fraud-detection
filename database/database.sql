

create table city (
    city_id SERIAL primary key,
    city_name VARCHAR(255),
    city_state VARCHAR(255),
    city_pop BIGINT
);

create table client (
    client_id SERIAL primary key,
    client_first_name VARCHAR(150),
    client_last_name VARCHAR(150),
    client_gender CHAR(1),
    client_street VARCHAR(100),
    client_zip BIGINT,
    client_lat FLOAT8,
    client_long FLOAT8,
    client_job VARCHAR(150),
    client_date_of_birth DATE,
    city_id INT references city(city_id)
);

create table credit_card (
	cc_number BIGINT primary key,
	client_id INT references client(client_id)
);

create table merchant (
    merchant_id SERIAL primary key,
    merchant VARCHAR(255),
    merch_lat FLOAT8,
    merch_long FLOAT8,
    merch_zipcode VARCHAR(20)
);

create table transaction (
    trans_num char(32) primary key,
    trans_category VARCHAR(255),
    trans_amt FLOAT8,
    trans_date_trans_time TIMESTAMPTZ,
    trans_unix_time BIGINT,
    trans_is_fraud boolean,
    cc_num BIGINT not null references credit_card(cc_number),
    merchant_id INT not null references merchant(merchant_id)
);
