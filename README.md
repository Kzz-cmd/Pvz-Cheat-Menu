# 🧟‍♂️ Plants vs. Zombies - Python Memory Trainer

Um *trainer* (manipulador de memória) de código aberto para o jogo Plants vs. Zombies original, desenvolvido inteiramente em Python. 

Este projeto foi criado com propósitos educacionais para demonstrar na prática conceitos de Engenharia Reversa, leitura de ponteiros estáticos/multiníveis (lidando com ASLR) e injeção de AOB (*Array of Bytes*) diretamente na memória RAM do processo.

##  Funcionalidades

O script acessa diretamente a memória do executável (`popcapgame1.exe`) para permitir as seguintes alterações em tempo real:

* **Modificar Sóis:** Altera a quantidade de sóis na fase atual (utiliza mapeamento de ponteiros de múltiplos níveis).
* **Modificar Dinheiro:** Altera o saldo de moedas na loja do Crazy Dave. *(Nota: O jogo armazena o dinheiro dividido por 10 na memória).*
* **Zero Cooldown (Plantas Instântaneas):** Remove o tempo de recarga das plantas através de *AOB Scanning* e injeção de bytes (`NOP`), permitindo plantar sem parar. O script possui recuperação de estado (*State Recovery*) para identificar se a memória já foi modificada anteriormente.

---

## Como usar (Versão Fácil / Executável)

Se você quer apenas usar o Trainer sem mexer com código, não precisa instalar o Python:

1. Abra o seu jogo (Plants vs. Zombies).
2. Entre em uma fase qualquer.
3. Vá na aba [Releases](../../releases) aqui do GitHub e baixe o arquivo `.exe` mais recente.
4. Execute o arquivo baixado (pode ser necessário executar como Administrador).
5. Siga o menu no terminal!

---

## Para Desenvolvedores (Rodando do Código Fonte)

Se você quiser analisar, modificar ou compilar o código fonte, siga os passos abaixo:

### Pré-requisitos
* **Python 3.10+** (O código utiliza a estrutura `match/case`).
* Sistema Operacional Windows (necessário para a manipulação de processos via WinAPI).

### Instalação

1. Clone este repositório:
   ```bash
   git clone [https://github.com/Kzz-cmd/Pvz-Cheat-Menu.git](https://github.com/Kzz-cmd/Pvz-Cheat-Menu.git)
   cd Pvz-Cheat-Menu



