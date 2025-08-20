# Tradutor de Textos (Streamlit + deep-translator)

Um aplicativo simples e bonito para traduzir textos entre vários idiomas, construído com Python, Streamlit e a biblioteca `deep-translator` (GoogleTranslator).

## Funcionalidades
- Campo para digitar/colar o texto a ser traduzido
- Seletor de idioma de origem (com opção de detecção automática)
- Seletor de idioma de destino
- Botão "Traduzir"
- Exibição do resultado da tradução

## Pré-requisitos
- Python 3.9+

## Instalação
Crie e ative um ambiente virtual (opcional, mas recomendado) e instale as dependências:

```bash
pip install streamlit deep-translator
```

## Executando o projeto
Na pasta do projeto, rode:

```bash
streamlit run app.py
```

## Exemplo de uso
1. Abra o app no navegador (o Streamlit mostrará o link no terminal)
2. Cole um texto em "Texto para traduzir"
3. Selecione o idioma de origem (ou deixe em "Detectar automaticamente")
4. Selecione o idioma de destino
5. Clique em "Traduzir" e veja o resultado abaixo

## Observações
- O idioma de destino não pode ser "auto"; selecione um idioma específico.
- Caso os idiomas de origem e destino sejam iguais, o app mantém o texto original.
- É necessário estar conectado à internet, pois o tradutor usa serviços online.

## Licença
Este projeto é fornecido como exemplo educacional, sem garantias.
