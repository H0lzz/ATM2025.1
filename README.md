# Projeto Final de TPPE
Aluno: Artur henrique Holz Bartz - 221007869
Professor: Thiago Luiz
Turma: Noturno

Link do repositório antigo (Orientação a Objetos): https://github.com/H0lzz/ATM2023.1

O projeto se trata em uma máquina ATM (projeto de Orientação a Objetos) implementada com as técnicas e tecnologias emergentes aboraddas em sala de aula na disciplina de TPPE.

# Diagrama UML

![Diagrama UML](assets/UMLTFTPPE.drawio.png)

Relacionamentos:

ATM -> BankDatabase: Composição (1:1)
ATM -> AdminInterface: Composição (1:1)
ATM -> CashDispenserStrategy: Agragação (1:1)
ATM -> AuthHandler: Agragação (1:1)
ATM -> BankDatabase: Agregação (1:n)

BankDatabse -> Account: Agregação (1:n)

Account -> AccountObserver: Associação (1:n)

AuthHandler -> Authhandler: Autoassociação (1:n)
AuthHandler -> PinAuthHandler: Associação (1:n)
AuthHandler -> BiometricAuthHendler: Associação (1:n)
PinAuthHandler -> BiometricAuthHandler (Ordem de Cadeia)

CashDispenserStrategy <- StandardDispenser: Generalização (1:1)
CashDispenserStrategy <- largeBillDispenser: Generalização (1:1)

AdminInterface -> BankDatabase: Dependência (1:1)

Transaction <- Withdrawal: Generalização (1:n)
Transaction <- Deposit: Generalização (1:n)
Transaction <- BalanceInquiry: Generalização (1:n)
Transaction -> BankDatabase: Dependência (1:1)

AccountFactory -> Account: Dependência (1:n)
AccountFactory -> SavingsAccount: Dependência (1:n)
AccountFactory -> CheckingAccount: Dependência (1:n)

Account -> EmailNotifier: Associação (1:2)
Account -> SMSNotifier: Associação (1:2)
