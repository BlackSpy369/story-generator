import streamlit as st
from transformers import pipeline
import time
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
    max_length=st.slider("Max Length",50,800,200,10)

# prompt=st.text_input("Enter first line of story (min 5 words)")
prompt=st.text_area("Enter first line of story (min 5 words)")
if st.button("Generate"):
    if len(prompt.split(" "))>=5:
        with st.container(border=True):
            status.write("Generating Story, Please wait...")
            status.update(label="Status",expanded=True,state="running")
            start_time=time.time()
            generated_story=st.session_state.model(prompt,max_length=max_length)[0]["generated_text"]
            st.write(generated_story)
            end_time=time.time()

        cols=st.columns(2)
        with cols[0]:
            st.write("Time Taken")
            st.write("{}s".format(round(end_time-start_time,2)))
        with cols[1]:
            st.write("Length of Story")
            st.write("{} words".format(len(generated_story.split(" "))))

            status.update(label="Status",expanded=False,state="complete")
            status.write("Completed...")

    else:
        status.update(label="Status",expanded=False,state="error")
        st.error("Please atleast enter five words of story...")

st.warning("Sometimes Model may be unavailbale to generate, it will end up repeating words, in that case please reduce max length to 100 to 200 or try to regenerate...")