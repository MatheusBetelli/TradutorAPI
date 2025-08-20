"""
Aplicativo de tradução de textos usando Streamlit e deep-translator (GoogleTranslator).

Requisitos:
- streamlit
- deep-translator

Execução:
streamlit run app.py
"""

from typing import Dict, List, Tuple

import streamlit as st
from deep_translator import GoogleTranslator


def configure_page() -> None:
    """Configura metadados e layout da página do Streamlit."""
    st.set_page_config(
        page_title="Tradutor de Textos",
        page_icon="🌐",
        layout="centered",
        initial_sidebar_state="collapsed",
    )


@st.cache_data(show_spinner=False)
def get_supported_languages() -> Dict[str, str]:
    """Retorna o dicionário de idiomas suportados pelo GoogleTranslator.

    Formato: {nome_em_ingles: codigo}
    Ex.: {"english": "en", "portuguese": "pt"}

    Compatível com versões antigas do deep-translator nas quais
    `get_supported_languages` é método de instância.
    """
    try:
        # Versões mais novas: método de classe/estático
        return GoogleTranslator.get_supported_languages(as_dict=True)
    except TypeError:
        # Versões antigas: requer uma instância
        return GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)


def format_language_name(raw_name: str) -> str:
    """Formata o nome do idioma para exibição (Title Case, com espaços)."""
    return raw_name.replace("_", " ").title()


def build_language_options() -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """Monta as opções de idiomas para origem e destino.

    Retorna duas listas de tuplas (label, code):
    - origem_options: inclui a opção de detecção automática
    - destino_options: somente idiomas suportados
    """
    supported = get_supported_languages()  # {name: code}

    # Ordena alfabeticamente pelos nomes formatados
    sorted_items = sorted(
        ((format_language_name(name), code) for name, code in supported.items()),
        key=lambda item: item[0],
    )

    origin_options = [("Detectar automaticamente", "auto")] + sorted_items
    target_options = sorted_items
    return origin_options, target_options


def translate_text(text: str, source_code: str, target_code: str) -> str:
    """Traduza o texto usando GoogleTranslator.

    - source_code: código do idioma de origem (use "auto" para detecção)
    - target_code: código do idioma de destino
    """
    translator = GoogleTranslator(source=source_code, target=target_code)
    return translator.translate(text)


def render_header() -> None:
    """Renderiza título e descrição do app."""
    st.title("Tradutor de Textos")
    st.caption("Traduza frases e parágrafos entre diversos idiomas com o Google Translator via deep-translator.")
    st.divider()


def render_app() -> None:
    """Componente principal da interface do app."""
    render_header()

    origin_options, target_options = build_language_options()

    default_source = "auto"
    default_target = "en"  # Inglês como destino padrão

    # Localiza índices padrão para os selects
    def find_index(options: List[Tuple[str, str]], code: str) -> int:
        for idx, (_, opt_code) in enumerate(options):
            if opt_code == code:
                return idx
        return 0

    with st.container():
        st.subheader("Texto para traduzir")
        text_to_translate = st.text_area(
            label="",
            placeholder="Digite ou cole aqui o texto que deseja traduzir...",
            height=160,
        )

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        source_label, source_code = st.selectbox(
            "Idioma de origem",
            options=origin_options,
            index=find_index(origin_options, default_source),
            format_func=lambda option: option[0] if isinstance(option, tuple) else option,  # type: ignore[return-value]
        )

    with col2:
        target_label, target_code = st.selectbox(
            "Idioma de destino",
            options=target_options,
            index=find_index(target_options, default_target),
            format_func=lambda option: option[0] if isinstance(option, tuple) else option,  # type: ignore[return-value]
        )

    st.write("")
    translate_clicked = st.button("Traduzir", type="primary")

    if translate_clicked:
        if not text_to_translate.strip():
            st.warning("Por favor, digite um texto para traduzir.")
            return

        if target_code == "auto":
            st.error("O idioma de destino não pode ser 'auto'. Selecione um idioma específico.")
            return

        if source_code != "auto" and source_code == target_code:
            st.info("Os idiomas de origem e destino são iguais. Exibindo o texto original.")
            st.text_area("Tradução", value=text_to_translate, height=160, disabled=True)
            return

        try:
            with st.spinner("Traduzindo..."):
                translated = translate_text(text_to_translate, source_code, target_code)

            st.success("Tradução concluída!")
            st.text_area("Tradução", value=translated, height=160, disabled=True)

        except Exception as exc:  # pylint: disable=broad-except
            st.error("Ocorreu um erro ao traduzir. Verifique sua conexão com a internet e tente novamente.")
            with st.expander("Detalhes técnicos"):
                st.exception(exc)

    st.divider()
    st.caption(
        "Feito com ❤️ usando Streamlit e deep-translator (GoogleTranslator)."
    )


def main() -> None:
    """Função principal: orquestra a execução do app."""
    configure_page()
    render_app()


if __name__ == "__main__":
    main()


