from typing import Union

import streamlit as st
from faq import faq
from providers import AnthropicModels, OpenAIModels, ProviderProtocol, anthropic, openai


def get_provider(provider: str) -> ProviderProtocol:
    return {
        "Anthropic": anthropic,
        "OpenAI": openai,
    }[provider]


def get_model_names(provider: str) -> tuple[str]:
    models = {
        "Anthropic": AnthropicModels.model_names(),
        "OpenAI": OpenAIModels.model_names(),
    }
    return models[provider]


def get_provider_index(providers: tuple, provider) -> int:
    if provider not in providers:
        return 0
    return providers.index(provider)


def get_model_index(models: tuple, model) -> Union[int, None]:
    if model not in models:
        return 0
    return models.index(model)


def sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            ## How to use
            - Select a provider from the dropdown
            - Enter a prompt in the text area
            - Click the submit button
            """
        )
        providers = ("Anthropic", "OpenAI")
        if "llm" not in st.session_state and "model" not in st.session_state:
            st.session_state.llm = "OpenAI"
            st.session_state.model = "gpt-3.5-turbo"

        llm_provider = st.selectbox(
            "Select a provider",
            providers,
            index=get_provider_index(providers, st.session_state.llm),
            placeholder="Select provider...",
        )
        st.session_state.llm = llm_provider

        if not llm_provider:
            st.stop()

        models = get_model_names(llm_provider)
        llm_model = st.session_state.model
        llm_model = st.selectbox(
            "Select a model",
            models,
            index=get_model_index(models, llm_model),
            placeholder="Select model...",
        )
        st.session_state.model = llm_model

        if llm_provider and llm_model:
            provider = get_provider(llm_provider)
            st.session_state.chat = provider.chat(model_name=llm_model)

        faq()
