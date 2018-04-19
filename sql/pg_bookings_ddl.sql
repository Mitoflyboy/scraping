-- Table: stayzdb.stayz_bookings

DROP TABLE stayzdb.stayz_bookings;

CREATE TABLE stayzdb.stayz_bookings
(
    property_id int NOT NULL,
    ext_at date,
    arr_dt date,
    dep_dt date,
    book_days smallint
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE stayzdb.stayz_bookings
    OWNER to postgres;