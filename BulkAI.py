import streamlit as st
import pandas as pd
import openai
import io

# Set the API key
openai.api_key = st.secrets["key"]

# Create a login
def check_password():
    """Returns `True` if the user had the correct username and password."""

    def credentials_entered():
        """Checks whether a username and password entered by the user are correct."""
        if st.session_state["username"] == st.secrets["USERNAME"] and st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input("Username", on_change=credentials_entered, key="username")
    st.text_input("Password", type="password", on_change=credentials_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Username or password incorrect")
    return False

if not check_password():
    st.stop()

# Set Streamlit configuration
st.set_page_config(page_title="MIG Freeform Analysis Tool",
                   page_icon="https://www.agilitypr.com/wp-content/uploads/2018/02/favicon-192.png",
                   layout="wide")

prompt_placeholder = "Please analyze the following story to see if any Yamaha spokespeople appear in it. If yes, list the names. If no, respond with just the word 'No':"

st.title("MIG Freeform Analysis Tool")
st.subheader("Experimental")

with st.expander("Instructions"):
    """
    The app will feed each story into the GPT-4 model to analyze the story based on the custom prompt you provide.
    \nIt will merge in the HEADLINE and COVERAGE SNIPPET fields following your prompt in order to analyze each story.
    \nThe model will then generate a response for each story, and the responses will be displayed in a table below.
    \nYou can also download the results as an Excel file.
    \nUse cases could include identifying specific entities in news stories, associating stories to a list of categories, analyzing sentiment, or any other text-based analysis.
    """

with st.sidebar:
    st.header("Custom Prompt:")
    custom_prompt = st.text_area("Enter your analysis prompt here:",
                                 "Please analyze the following story to see if any Yamaha products appear in it. If yes, respond with only the list of names. If no, respond with just the word 'No': ",
                                 height=250)

    row_limit = st.number_input("Limit rows for testing (0 for all rows):", min_value=0, value=0, step=1)

upload_file = st.file_uploader("Upload a CSV or XLSX file:", type=["csv", "xlsx"])

if upload_file:
    file_type = upload_file.name.split('.')[1]

    if file_type == "csv":
        df = pd.read_csv(upload_file)
    elif file_type == "xlsx":
        xls = pd.ExcelFile(upload_file)
        sheet_names = xls.sheet_names
        sheet = st.selectbox('Select a worksheet', sheet_names)
        df = pd.read_excel(upload_file, sheet_name=sheet)

    if row_limit > 0:
        df = df.head(row_limit)
    st.write(f"Total Stories: {len(df)}")

    if st.button("Analyze Stories"):
        responses = []
        progress_bar = st.progress(0)
        total_stories = len(df)

        for i, row in df.iterrows():
            full_prompt = f"{custom_prompt}\n\n{row['Headline']}. {row['Coverage Snippet']}"
            try:
                response = openai.Chat.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a highly knowledgeable media analysis AI."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                responses.append(response['choices'][0]['message']['content'].strip())
            except openai.OpenAIError as e:
                responses.append(f"Error: {e}")

            progress_bar.progress((i + 1) / total_stories)

        df['Analysis'] = responses
        st.dataframe(df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
        output.seek(0)
        st.download_button(
            label="Download analysis results as Excel file",
            data=output,
            file_name="analysis_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
