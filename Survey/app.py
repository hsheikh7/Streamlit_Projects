import streamlit as st
import pandas as pd 
from DButils import create_tables, get_survey, save_question, save_results, get_results 
import plotly.express as px
import sqlite3
import random

st.set_page_config(layout="wide")

create_tables()  
df_survey = get_survey()

if 'survey' not in st.session_state:
    st.session_state['survey'] = get_survey()

st.title("Smaple Survey Using Streamlit")
st.write("""Enter the question and provide possible choices. """)
with st.expander("More Information"):
    st.write("""
    **Overview:** This project showcases how to use Streamlit for gathering and analyzing online surveys. It utilizes SQLite, a user-friendly database system, ideal for small-scale data management.
    
    **About the Developer:** I'm Hassan Sheikh, a dedicated Python developer with a strong background in urban planning and environmental management. Let's connect on LinkedIn: https://www.linkedin.com/in/hsheikh7/
    
    **Source Code:** You can access the code on GitHub: https://github.com/hsheikh7/Streamlit_Projects
    """)

st.header("Question")
q_text = st.text_input("Question")

possible_responses = ["Yes,No,Not sure",
           "Strongly agree,Agree,Neither agree not disagree,Disagree,Strongly disagree",
           "Daily,Weekly,Monthly,Rarely,Never"]
q_choices = st.selectbox('Some possible answers, you can choose among them:', possible_responses)

new_response = st.text_input('Write your specific responses and separate them by commas.')

if new_response:
    q_choices = new_response

st.write(f'You selected: {q_choices}')

submitted = st.button("Add question to survey")  

if submitted:
    save_question(q_text, q_choices)
    st.session_state['survey'] = get_survey()

# ---------- Show Question After Drafting --------------------
st.write("Here are questions.")

survey_df = pd.DataFrame(st.session_state['survey'])
st.table(survey_df)

# ------------ Present Questions and Save Results 
st.info("## Select the answer to each question and then click on 'Submit'")

questions = get_survey()
responses = []

for index, row in questions.iterrows():
    question_text = row['question']
    choices = row['choices'].split(', ')
    response = st.radio(question_text, choices)
    choice_id = choices.index(response) + 1
    responses.append((index + 1, choice_id))

if 'num1' not in st.session_state:
    st.session_state['num1'] = random.randint(1, 10)
if 'num2' not in st.session_state:
    st.session_state['num2'] = random.randint(1, 10)

st.write(f"What is {st.session_state['num1']} + {st.session_state['num2']}?") 
captcha = st.text_input("Please inter the right number.")

if st.button("Submit"):
    if captcha == str(st.session_state['num1'] + st.session_state['num2']):
        save_results(responses)
        st.success("Answers submitted successfully!")
    else:
        st.error("Incorrect captcha. Please try again.")


#---------- Show Analysis of Results -----------------
st.info("## Here are the results:")
st.write("The results are presented as a dataframe.")

df = get_results()
st.dataframe(df, use_container_width=True)

# -------------- Download ------------------ 
df = get_results()
st.download_button(
    label="Download data as CSV",
    data=df.to_csv().encode("utf-8"),
    file_name="survey_results.csv",
    mime="text/csv",
)

# -------------- Visualize  ------------------ 
# Create a bar chart
fig = px.bar(df, x='question_text', y='count', color='choice_text', title='Survey Results',
             labels={'question_text':'Question', 'count':'Number of Responses', 'choice_text':'Choice'},
             template='plotly_dark')

# Show the plot in Streamlit
st.plotly_chart(fig)

# ------- Vis Part 2: an array of bar graph figures, one for each question 
figures = []

for q in df['question_text'].unique():
    # Filter the data for the current question
    data = df[df['question_text'] == q]
    
    # Create a bar chart for the current question
    fig = px.bar(data, x='choice_text', y='count', title=q)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="Response")
    fig.update_yaxes(title_text="Count")
    
    # Append the figure to the list of figures
    figures.append(fig)

# Choose which graph to display with a set of radio buttons
st.info("### Choose the graph for a specific question")
f = st.radio("Choose a graph", options=df['question_text'].unique())
column_index = list(df['question_text'].unique()).index(f)
st.plotly_chart(figures[column_index])

