# YouTube Downloader

## Descrição
YouTube Downloader é uma aplicação desktop simples e eficiente que permite baixar vídeos e áudios do YouTube em diferentes formatos e qualidades. Desenvolvida com Python e Tkinter, esta ferramenta oferece uma interface gráfica intuitiva para facilitar o processo de download.

## Funcionalidades
- Download de vídeos do YouTube em diferentes resoluções
- Extração de áudio em formato MP3
- Interface gráfica amigável
- Barra de progresso para acompanhar o download
- Seleção de pasta de destino para os arquivos baixados

## Requisitos
- Python 3.6 ou superior
- Bibliotecas Python (listadas no arquivo requirements.txt):
  - tkinter (geralmente incluído com o Python)
  - yt-dlp
- FFmpeg (necessário para processamento de áudio e vídeo)

## Instalação
1. Clone ou baixe este repositório
2. Instale as dependências usando o requirements.txt:
   ```
   pip install -r requirements.txt
   ```
3. Instale o FFmpeg (necessário para o funcionamento do aplicativo):
   - **Opção 1**: Baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html) e coloque o arquivo ffmpeg.exe na mesma pasta do script downloader.py
   - **Opção 2**: Instale o FFmpeg globalmente e adicione-o ao PATH do sistema
     - No Windows:
       - Use [Chocolatey](https://chocolatey.org/) com o comando `choco install ffmpeg`
       - Ou baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html), extraia os arquivos e adicione ao PATH:
         1. Extraia o arquivo baixado em uma pasta (ex: `C:\ffmpeg`)
         2. Adicione o caminho da pasta bin ao PATH do sistema:
            - Clique com o botão direito em "Este Computador" > "Propriedades" > "Configurações avançadas do sistema"
            - Clique em "Variáveis de Ambiente"
            - Na seção "Variáveis do sistema", selecione "Path" e clique em "Editar"
            - Clique em "Novo" e adicione o caminho para a pasta bin (ex: `C:\ffmpeg\bin`)
            - Clique em "OK" para fechar todas as janelas
            - Reinicie o prompt de comando ou PowerShell para aplicar as alterações
     - No Linux: Use `sudo apt install ffmpeg` (Ubuntu/Debian) ou equivalente para sua distribuição
     - No macOS: Use [Homebrew](https://brew.sh/) com o comando `brew install ffmpeg`
4. Execute o script:
   ```
   python downloader.py
   ```

## Como Usar
1. Inicie a aplicação
2. Cole a URL do vídeo do YouTube no campo de entrada
3. Clique em "Carregar Opções" para ver as qualidades disponíveis
4. Selecione a qualidade desejada na lista
5. Clique em "Baixar" e escolha a pasta de destino
6. Aguarde o download ser concluído

## Notas
- A aplicação utiliza FFmpeg para processamento de áudio e vídeo
  - O programa buscará o FFmpeg primeiro na pasta local e depois no PATH do sistema
  - Se o FFmpeg não for encontrado, um erro será exibido
- Para downloads de áudio, o formato final será MP3
- Para downloads de vídeo, o formato dependerá da opção selecionada

## Licença
Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Créditos
Este aplicativo utiliza as seguintes bibliotecas de código aberto:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): Uma bifurcação do youtube-dl com recursos adicionais e correções
- [FFmpeg](https://ffmpeg.org/): Uma solução completa para gravar, converter e transmitir áudio e vídeo