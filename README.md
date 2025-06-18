# Projeto Final de TPPE
Aluno: Artur henrique Holz Bartz - 221007869</br>
Professor: Thiago Luiz</br>
Turma: Noturno</br>

Link do repositório antigo (Orientação a Objetos): https://github.com/H0lzz/ATM2023.1</br>

O projeto se trata em uma máquina ATM (projeto de Orientação a Objetos) implementada com as técnicas e tecnologias emergentes aboraddas em sala de aula na disciplina de TPPE.</br>

# Arquitetura
A arquitetura escolhida foi a arquitetura limpa (Clean Archtecture) que garante:</br>
Separação de responsabilidades</br>
Baixo acoplamento</br>
Facilidade de testes</br>
Escalabilidade e manutenibilidade</br>

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

# Modelo Físico do Banco de Dados

![Diagrama do Modelo Físico](assets/modeloFisicoBD.png)

# Backlog - Histórias de Usuário (User Story)

Arquivo de backlog: [Backlog](docs/UserStories.md)</br>
Link Trello: (https://trello.com/invite/b/6816187b0f978e40a257edb1/ATTI5879d2caa32b99bec8bfee3eb1da2d5bF3B54DB1/backlog-tppe)</br>
Protótipo de alta fidelidade (Figma): https://www.figma.com/proto/7igZPLpx9gD3tHRqC0nXxF/ATM2025.1?node-id=7501-175&starting-point-node-id=7501%3A175&t=7HSQscz8ki573vfO-1 </br>
