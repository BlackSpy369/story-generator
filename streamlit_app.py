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

with st.status("Status",expanded=False) as status:
    st.write("Loading Model...")

with st.sidebar:
    max_length=st.slider("Max Length",10,800,200,10)

# prompt=st.text_input("Enter first line of story (min 5 words)")
prompt=st.text_area("Enter first line of story (min 5 words)")
if st.button("Generate"):
    if len(prompt.split(" "))>5:
        with st.container(border=True):
            status.write("Generating Story, Please wait...")
            status.update(label="Status",expanded=True,state="running")
            st.write(st.session_state.model(prompt,max_length=max_length)[0]["generated_text"])
            status.update(label="Status",expanded=False,state="complete")
            status.write("Completed...")

    else:
        status.update(label="Status",expanded=False,state="error")
        st.error("Please atleast enter five words of story...")

st.info("Sometimes Model may be unavailbale to generate, it will end up repeating words, in that case please reduce max length to 100 to 200 or try to regenerate...")