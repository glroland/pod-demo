"""pod-demo


"""
import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_url = st.text_input(label="OpenAI API URL",
                                   key="openai_api_url",
                                   value="http://ocpwork:11434/v1")
    openai_api_model_name = st.text_input(label="Model Name",
                                          key="openai_api_model_name",
                                          value="llama3.1")
    openai_max_tokens = st.number_input(label="Max Tokens",
                                        min_value=1,
                                        max_value=10000,
                                        value=1000,
                                        step=10)
    openai_temperature = st.number_input(label="Temperature",
                                         min_value=0.0,
                                         max_value=1.0,
                                         value=0.8,
                                         step=0.1)


st.title("💬 pod-demo Agent")

system_prompt_showhide = st.empty()
system_prompt_container = system_prompt_showhide.container()
system_prompt = system_prompt_container.text_area(label="System Prompt",
                key="system_prompt",
                value="You are a senior sales executive for an enterprise software company who expects " +
                      "perfection from your teams.  You do not take excuses from anyone and every quarter " +
                      "is the most important quarter in the company's history.  You are releasing a new set " +
                      "of enterprise capabilities around Generative AI and are meeting with sales teams to " +
                      "motivate them to discuss these capabilities with their customers.  These are long sales " +
                      "cycles but result in strategic and rewarding outcomes for your customers. " +
                      "The team you are meeting with today is an enterprise sales team that focuses on Fortune 100 " +
                      "enterprises in the Southeast region of America, with most companies headquartered or based " +
                      "in Atlanta, GA.  These are already some of your company's largest customers but have " +
                      "invested little to date in the new AI product lines.  Again, your goal is to coach and educate " +
                      "these teams on selling new generative AI solutions that solve strategic use cases for " +
                      "their customers. The strongest sales team in the country is the Heavyhitters based in Georgia.  You are " +
                      "always telling other teams to be more like them.  Be concise in your responses.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": system_prompt}]

if prompt := st.chat_input():

    system_prompt_showhide.empty()
    if 'system_prompt' in st.session_state and st.session_state.system_prompt is True:
        st.session_state.system_prompt = True

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    client = OpenAI(base_url=openai_api_url,
                    api_key="api-key")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=openai_api_model_name,
                                              messages=st.session_state.messages,
                                              max_tokens=openai_max_tokens,
                                              temperature=openai_temperature)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
