## Histórias de Usuário (User Stories)

### **1. Cliente**

#### **US01 - Autenticação**
**Como** cliente,  
**Quero** autenticar-me com número de conta e PIN,  
**Para** acessar meu saldo e operações bancárias.  

**Critérios de Aceitação**:  
- Validação correta do PIN.  
- Redirecionamento para o menu principal após login.  

---

#### **US02 - Saque**  
**Como** cliente,  
**Quero** sacar dinheiro em valores pré-definidos (ex: $20, $100),  
**Para** obter dinheiro físico rapidamente.  

**Critérios de Aceitação**:  
- Menu com opções de valor fixo.  
- Atualização do saldo após saque.  
- Notificação por SMS/email.  

---

#### **US03 - Depósito**  
**Como** cliente,  
**Quero** depositar envelopes de dinheiro/cheques,  
**Para** adicionar fundos à minha conta.  

**Critérios de Aceitação**:  
- Confirmação do valor depositado.  
- Saldo atualizado após verificação.  

---

#### **US04 - Notificações**  
**Como** cliente,  
**Quero** receber notificações por SMS/email sobre transações,  
**Para** monitorar minha conta em tempo real.  

**Critérios de Aceitação**:  
- Notificação disparada para saques/depósitos.  
- Mensagem clara com valor e tipo de transação.  

---

### **2. Administrador**

#### **US05 - Criar Conta**  
**Como** administrador,  
**Quero** adicionar novas contas (normais ou administrativas),  
**Para** gerenciar usuários do sistema.  

**Critérios de Aceitação**:  
- Validação de número de conta único.  
- Persistência no banco de dados.  

---

#### **US06 - Listar Contas**  
**Como** administrador,  
**Quero** listar todas as contas com saldos e detalhes,  
**Para** auditoria e gestão.  

**Critérios de Aceitação**:  
- Exibição formatada em tabela.  
- Filtro por tipo de conta.  

---

#### **US07 - Atualizar/Remover Contas**  
**Como** administrador,  
**Quero** atualizar ou remover contas existentes (exceto admins),  
**Para** manter a base de dados atualizada.  

**Critérios de Aceitação**:  
- Impedir exclusão de contas admin.  
- Validação de campos atualizados.  

---

#### **US08 - Acesso Biométrico**  
**Como** administrador,  
**Quero** acessar o modo administrativo com autenticação biométrica,  
**Para** maior segurança.  

**Critérios de Aceitação**:  
- Acesso apenas com conta admin.  
- Fallback para PIN se a biometria falhar.  

---

### **3. Sistema**

#### **US09 - Autenticação em Cadeia**  
**Como** sistema,  
**Quero** gerenciar a cadeia de autenticação (PIN/biometria),  
**Para** oferecer opções flexíveis de login.  

**Critérios de Aceitação**:  
- Priorizar PIN, com fallback para biometria.  
- Log de tentativas falhas.  

---

#### **US10 - Gerenciar Dispensador**  
**Como** sistema,  
**Quero** alternar entre dispensadores de notas ($20/$100),  
**Para** otimizar o uso de cédulas.  

**Critérios de Aceitação**:  
- Troca dinâmica de estratégia.  
- Mensagem de confirmação.  

---

#### **US11 - Recuperação de Dados**  
**Como** sistema,  
**Quero** carregar contas padrão se o arquivo JSON estiver corrompido,  
**Para** garantir disponibilidade.  

**Critérios de Aceitação**:  
- Criar arquivo padrão automaticamente.  
- Manter dados críticos (ex: conta admin).  