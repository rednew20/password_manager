CREATE TABLE IF NOT EXISTS user_info (
	id integer PRIMARY KEY ,
	username text NOT NULL,
  password text NOT NULL,
	email text NOT NULL	
);

-- accounts table
CREATE TABLE IF NOT EXISTS accounts (
	id integer PRIMARY KEY,
	account_name text NOT NULL,	
);

-- accounts credentials
CREATE TABLE IF NOT EXISTS account_info (
	account_id integer PRIMARY KEY,
	account_username text NOT NULL,
	account_password text NOT NULL,
	created_at text NOT NULL,
	updated_At text NOT NULL,
	FOREIGN KEY (account_id) REFERENCES accounts (id)
);