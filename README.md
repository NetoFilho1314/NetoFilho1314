Aqui está o arquivo `README.md` para o projeto "Stikman World":

```markdown
# Stikman World

**Stikman World** é um jogo 2D de plataforma desenvolvido em Python usando a biblioteca Pygame. Neste jogo, você controla um personagem (Stikman) que pode interagir com diferentes blocos, pular, e explorar o mundo do jogo.

## Requisitos

Para rodar o jogo, você precisa ter Python 3.x instalado em seu sistema, além da biblioteca Pygame. Você pode instalar o Pygame usando o seguinte comando:

```bash
pip install pygame
```

## Estrutura do Projeto

1. **Inicialização e Configuração**
   - Inicializa o Pygame e o mixer de áudio.
   - Configura a largura e a altura da janela do jogo.
   - Define o título da janela e carrega a imagem de fundo.

2. **Paleta de Blocos**
   - Cria uma paleta de blocos com diferentes cores e texturas, incluindo grama, terra, pedra, areia e diamante.

3. **Configurações do Jogador**
   - Define o jogador com propriedades como velocidade, gravidade e controle de pulo.
   - Inclui visibilidade do jogador e movimentação.

4. **Funções do Jogo**
   - Funções para desenhar o fundo, blocos, paleta de cores e outros elementos gráficos.
   - Implementa lógica para aplicação de gravidade, colisões e atualizações de blocos e jogador.

5. **Menus e Tela de Ajuda**
   - Exibe um menu inicial com opções para começar o jogo e acessar a ajuda.
   - Mostra uma tela de ajuda com controles e instruções do jogo.

6. **Loop Principal**
   - Controla o fluxo do jogo, processando eventos de entrada do usuário e atualizando o estado do jogo.
   - Gerencia a música de fundo, mostrando a paleta de cores e manipulando os blocos no jogo.

## Instruções de Uso

1. **Iniciar o Jogo**
   - Execute o script Python para iniciar o jogo. O menu inicial será exibido.

2. **Controles**
   - `W`: Pular
   - `A`: Mover para a esquerda
   - `D`: Mover para a direita
   - `B`: Adicionar bloco
   - `R`: Remover bloco
   - `P`: Mostrar/Ocultar paleta de cores
   - `V`: Mostrar o jogador
   - Setas para cima/baixo: Rolagem da paleta
   - `H`: Mostrar tela de ajuda

3. **Interação**
   - Clique em blocos na tela para adicionar ou remover blocos.
   - Use a paleta de cores para selecionar diferentes tipos de blocos.
   - Navegue pelas opções do menu usando o mouse.

## Recursos

- **Imagens**: A imagem de fundo é carregada do diretório `resources/sprites`.
- **Música**: Músicas são carregadas do diretório `resources/music`.

Certifique-se de ter as imagens e músicas nos diretórios apropriados antes de executar o código. Ajuste os caminhos dos arquivos conforme necessário para corresponder à estrutura do seu projeto.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).
```

Salve o conteúdo acima em um arquivo chamado `README.md` na raiz do seu projeto. Este arquivo fornece uma visão geral completa do projeto, instruções para instalação, uso e detalhes sobre os recursos do jogo.
