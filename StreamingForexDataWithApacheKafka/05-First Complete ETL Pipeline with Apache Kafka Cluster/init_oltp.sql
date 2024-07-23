CREATE DATABASE "tradingmarketdata"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	
	
	
\c tradingmarketdata postgres;

CREATE TABLE IF NOT EXISTS public.trades
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    price numeric,
    symbol character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "time" bigint NOT NULL,
    volume numeric
);

ALTER TABLE IF EXISTS public.trades
    OWNER to postgres;
	
CREATE INDEX trades_time_idx
  ON trades("time");
