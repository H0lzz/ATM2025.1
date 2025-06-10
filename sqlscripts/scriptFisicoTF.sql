CREATE TABLE account (
id INTEGER NOT NULL AUTO_INCREMENT, 
account_number INTEGER NOT NULL, 
pin INTEGER NOT NULL, 
available_balance FLOAT, 
total_balance FLOAT, 
is_admin BOOL, 
PRIMARY KEY (id)
);

CREATE TABLE transaction (
id INTEGER NOT NULL AUTO_INCREMENT, 
account_id INTEGER NOT NULL, 
type ENUM('deposit','withdraw') NOT NULL, 
amount FLOAT NOT NULL, 
timestamp DATETIME DEFAULT (now()), 
PRIMARY KEY (id), 
FOREIGN KEY(account_id) REFERENCES account (id)
);