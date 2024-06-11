CREATE TABLE "user_account" (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name varchar UNIQUE NOT NULL,
    password varchar NOT NULL,
    eth_address varchar NOT NULL,
    eht_key varchar NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.wallet (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	coin varchar NOT NULL,
	count int2 NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	updated_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT wallet_pk PRIMARY KEY (id, coin)
);