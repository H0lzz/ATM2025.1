# Projeto Final de TPPE
Aluno: Artur henrique Holz Bartz - 221007869
Professor: Thiago Luiz
Turma: Noturno

Link do repositório antigo (Orientação a Objetos): https://github.com/H0lzz/ATM2023.1

O projeto se trata em uma máquina ATM (projeto de Orientação a Objetos) implementada com as técnicas e tecnologias emergentes aboraddas em sala de aula na disciplina de TPPE.

# Diagrama UML

![Diagrama UML](assets/UMLTFTPPE.drawio.png)

Relacionamentos:

ATM -> BankDatabase: Composição (1:1)</br>
ATM -> AdminInterface: Composição (1:1)</br>
ATM -> CashDispenserStrategy: Agragação (1:1)</br>
ATM -> AuthHandler: Agragação (1:1)</br>
ATM -> BankDatabase: Agregação (1:n)</br>

BankDatabse -> Account: Agregação (1:n)</br>

Account -> AccountObserver: Associação (1:n)</br>

AuthHandler -> Authhandler: Autoassociação (1:n)</br>
AuthHandler -> PinAuthHandler: Associação (1:n)</br>
AuthHandler -> BiometricAuthHendler: Associação (1:n)</br>
PinAuthHandler -> BiometricAuthHandler (Ordem de Cadeia)</br>

CashDispenserStrategy <- StandardDispenser: Generalização (1:1)</br>
CashDispenserStrategy <- largeBillDispenser: Generalização (1:1)</br>

AdminInterface -> BankDatabase: Dependência (1:1)</br>

Transaction <- Withdrawal: Generalização (1:n)</br>
Transaction <- Deposit: Generalização (1:n)</br>
Transaction <- BalanceInquiry: Generalização (1:n)</br>
Transaction -> BankDatabase: Dependência (1:1)</br>

AccountFactory -> Account: Dependência (1:n)</br>
AccountFactory -> SavingsAccount: Dependência (1:n)</br>
AccountFactory -> CheckingAccount: Dependência (1:n)</br>

Account -> EmailNotifier: Associação (1:2)</br>
Account -> SMSNotifier: Associação (1:2)</br>
