import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Story Generation",page_icon="🤗")

if "model" not in st.session_state:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # Load the base model and tokenizer
    base_model = AutoModelForCausalLM.from_pretrained("fine_tuned_model")
    tokenizer = AutoTokenizer.from_pretrained("fine_tuned_model")
    st.session_state.model=pipeline("text-generation",model=base_model,tokenizer=tokenizer)

st.title("STORY GENERATION APP")

prompt=st.text_input("Enter story first line")
if prompt!="":
   st.write(st.session_state.model(prompt,max_length=200)[0]["generated_text"])
