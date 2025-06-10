-- Inserir contas
INSERT INTO account (account_number, pin, available_balance, total_balance, is_admin)
VALUES 
(1001, 1234, 500.00, 500.00, FALSE),
(1002, 5678, 1000.00, 1200.00, FALSE),
(1003, 4321, 1500.00, 1500.00, FALSE),
(1004, 1234, 500.00, 500.00, FALSE),
(1005, 5678, 1000.00, 1200.00, FALSE),
(1006, 4321, 1500.00, 1500.00, FALSE),
(1007, 1234, 500.00, 500.00, FALSE),
(1008, 5678, 1000.00, 1200.00, FALSE),
(1009, 4321, 1500.00, 1500.00, FALSE),
(1010, 1234, 500.00, 500.00, FALSE),
(1011, 5678, 1000.00, 1200.00, FALSE),
(1012, 4321, 1500.00, 1500.00, FALSE),
(9999, 9999, 10000.00, 10000.00, TRUE); -- Conta admin

-- Inserir transações para a conta 1001
INSERT INTO transaction (account_id, type, amount, timestamp)
VALUES 
(1, 'deposit', 500.00, NOW());

-- Inserir transações para a conta 1002
INSERT INTO transaction (account_id, type, amount, timestamp)
VALUES 
(2, 'deposit', 1200.00, NOW()),
(2, 'withdraw', 200.00, NOW());

-- Inserir transações para a conta 1003
INSERT INTO transaction (account_id, type, amount, timestamp)
VALUES 
(3, 'deposit', 1500.00, NOW());

-- Inserir transações para a conta admin (9999)
INSERT INTO transaction (account_id, type, amount, timestamp)
VALUES 
(4, 'deposit', 10000.00, NOW());
