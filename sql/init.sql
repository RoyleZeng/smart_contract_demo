CREATE TYPE role AS ENUM ('manufacture', 'customer');


CREATE TABLE "user_account" (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	"role" role NOT NULL DEFAULT 'customer',
	name varchar NOT NULL,
    password varchar NOT NULL,
    eth_address varchar NOT NULL,
    eht_key varchar NOT NULL,
    phone varchar NOT NULL,
    birthday varchar NOT NULL,
    address varchar NOT NULL,
    email varchar NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT user_account_unique UNIQUE (phone)
);

CREATE TABLE public.wallet (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	coin varchar NOT NULL,
	count int2 NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	updated_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT wallet_pk PRIMARY KEY (id, coin)
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    barcodes varchar[] NOT NULL DEFAULT '{}',
    owner uuid,
    is_registered BOOLEAN NOT NULL DEFAULT false,
    is_listed BOOLEAN NOT NULL DEFAULT false,
    product_token varchar NOT NULL,
    registered_at timestamptz,
    listed_at timestamptz,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
);