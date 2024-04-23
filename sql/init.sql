CREATE TABLE "user_account" (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name varchar UNIQUE NOT NULL,
    password varchar NOT NULL,
    eth_address varchar NOT NULL,
    eht_key varchar NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
);