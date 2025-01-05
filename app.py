from typing import Union

import pandas as pd
import streamlit as st

from model import *
from langchain_core.prompts.prompt import PromptTemplate
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_experimental.agents.agent_toolkits.pandas.prompt import (
    PREFIX,
    SUFFIX_WITH_DF,
)
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from langchain.agents.agent import (
    AgentExecutor,
    BaseMultiActionAgent,
    BaseSingleActionAgent,
    RunnableAgent,
)
from langchain.agents.react.agent import create_react_agent



st.header('RAG from `csv` files')
ss = st.session_state

with st.sidebar:
    st.header(f"Add your documents!")
    uploaded_file = st.file_uploader("Choose your `csv` file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df)

if uploaded_file:
    
    def create_prompt(df, number_of_head_rows: int = 5,):
        suffix_to_use = SUFFIX_WITH_DF
        prefix = PREFIX

        template = "\n\n".join([prefix, "{tools}", FORMAT_INSTRUCTIONS, suffix_to_use])
        prompt = PromptTemplate.from_template(template)
        partial_prompt = prompt.partial()
        if "df_head" in partial_prompt.input_variables:
            df_head = str(df.head(number_of_head_rows).to_markdown())
            partial_prompt = partial_prompt.partial(df_head=df_head)
        return partial_prompt
    
    def custom_df_agent(llm, df):
        df_locals = {}
        df_locals["df"] = df
        tools = [PythonAstREPLTool(locals=df_locals)]
        prompt = create_prompt(df)
        agent: Union[BaseSingleActionAgent, BaseMultiActionAgent] = RunnableAgent(
            runnable=create_react_agent(llm, tools, prompt),  # type: ignore
            input_keys_arg=["input"],
            return_keys_arg=["output"],
        )
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent = custom_df_agent(model, df)

    if 'messages' not in ss:
        ss.messages = []

    for msg in ss.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])

    human_input = st.chat_input('Say something')

    if human_input:
        with st.chat_message('human'):
            st.write(human_input)
            ss.messages.append({'role':'human', 'content':f'{human_input}'})

        with st.chat_message('ai'):
            response = agent.run(human_input)
            st.write(response)
            ss.messages.append({'role':'ai', 'content':f'{response}'})

        
                    

                    