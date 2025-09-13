import streamlit as st
import pandas as pd
from src.Generate_Tests import Generate
from src.Preprocessing import Precessing 
from docx import Document
import io

st.set_page_config(layout='wide',page_title="Test Case Generator")


# Initialize session state
if "generating" not in st.session_state:
    st.session_state.generating = False

def generate():
    st.session_state.generating = True


st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .custom-title {
        font-size: 48px;
        text-align: left;
        width: 80%;
        background-color: ;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    <div class="custom-title">🧪 Test Case Generator</div>
""", unsafe_allow_html=True)

# st.title("Test Case Generator")
generator = Generate()
precessing=Precessing()


@st.dialog("Edit table")
def output_markdown(text):
    st.markdown(
        """
        <style>
        .stDialog>div>div{
            width:90vw !important; max-width: 1200px !important:
        }
</style>
        """,
        unsafe_allow_html=True
    )
    data=pd.DataFrame(text,columns=['Requriement',"Test Cases"])
    
    # Display in editable table
    edited_data=st.data_editor(data, num_rows="static", use_container_width=True, key="editable_table")
    csv = edited_data.to_csv(index=False)
    if st.download_button(
    label="Save Report",
    data=csv,
    file_name="Testcases_report.csv",
    mime="text/csv",
    use_container_width=True
):
        edited_data.to_csv("Testcases_report.csv",index=False)
        st.info("Sucessfully downloaded the reports")
        st.rerun()
        
    



    



st.write(" ### A Test Case Generator is a tool or script designed to automatically create test inputs and outputs for validating software programs, especially in the context of algorithmic problems, competitive programming, or software testing.")
choice=st.radio("Select test case Type:",
                ["None","File upload","Text"], horizontal=True)
if choice=="Text":
    
    input_query=st.text_area("Enter the Input query",height=100)
    input_query=precessing.text_file_preprocessing(input_query)
    if st.button("Submit",False):
        output=[]
        for i in input_query:
            test_cases=generator.generate_test_cases(i)
            output.append((i,str(test_cases)))
        output_markdown(output)

        
        

        st.write()
elif choice=="File upload":
    uploaded_file = st.file_uploader('Upload your .txt or .docx file', type=["txt", "docx"])
    if uploaded_file:
        if uploaded_file.type.split("/")[-1]=="plain":
            st.success(f"Uploaded file: {uploaded_file.name}")
            
            gen_btn,space=st.columns([1,0.2])
            with gen_btn:
                st.button("Generate",key="key_generator",help="Generate Button",disabled=st.session_state.generating,
        on_click=generate)
            with space:
                if st.session_state.generating:
                    with st.spinner(""):
                        st.write("")
            if st.session_state.generating and uploaded_file is not None:
                with st.spinner("Generating test cases..."):
                    content = uploaded_file.read()
                    content=precessing.text_file_preprocessing(content.decode("utf-8"))
                    output=[]
                    for text in content:
                        test_cases=generator.generate_test_cases(text)
                        
                        output.append((text,str(test_cases)))
                        # Ensure test_cases is string (not list)
                            
                    st.success("Test case generation completed!")
    
                    output_markdown(output)
                # Reset generating state
                st.session_state.generating = False
        else:
            print("Hellloo")
            # uploaded_file.seek(0)
            st.write("Uploaded file name:", uploaded_file.name)
            st.write("MIME type:", uploaded_file.type)
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            content=precessing.text_file_preprocessing(text)
            btn_genration,space=st.columns([1,12])
            with btn_genration:
                st.spinner("Generating Tests")
                output=[]
                for text in content:
                    test_cases=generator.generate_test_cases(text)
                    
                    output.append((text,str(test_cases)))
                    # Ensure test_cases is string (not list)
                output_markdown(output)
                        
                st.success("Test case generation completed!")






                    
else:
    st.info("Please select a test case input method.")
    