import streamlit as st
import pandas as pd 
from DButils import create_tables, get_survey, save_question, save_results, get_results, get_choice_id
import plotly.express as px
import random

st.set_page_config(layout="wide")

create_tables()  
df_survey = get_survey()

if 'survey' not in st.session_state:
    st.session_state['survey'] = get_survey()

st.title("Sustainability Survey Using Streamlit + SQLite")
st.write("""Enter the question and provide possible choices. """)
with st.expander("More Information"):
    st.write("""
    **Overview:** This project showcases how to use Streamlit for gathering and analyzing online surveys. It utilizes SQLite, a user-friendly database system, ideal for small-scale data management.
    **About the Developer:** I'm Hassan Sheikh, a dedicated Python developer with a strong background in urban planning and environmental management. Let's connect on LinkedIn: https://www.linkedin.com/in/hsheikh7/
    **Source Code:** You can access the code on GitHub: https://github.com/hsheikh7/Streamlit_Projects
    """)

st.header("Drafting The Survey")
q_text = st.text_input("Question")

possible_responses = ["Daily,Weekly,Monthly,Rarely,Never", 
            "Yes,No,Not sure",
           "Strongly agree,Agree,Neither agree not disagree,Disagree,Strongly disagree" ]

q_choices = st.selectbox('Some possible choices, you can choose among them:', possible_responses)

new_choices = st.text_input('Write your specific choices and separate them by commas.')

if new_choices:
    q_choices = new_choices

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
st.header("Answer the questions and submit the form.")

questions = get_survey()
responses = []

for index, row in questions.iterrows():
    question_text = row['question']
    choices = row['choices'].split(', ')
    response = st.radio(question_text, choices)
    choice_id = get_choice_id(response)
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
        st.session_state['num1'] = random.randint(1, 10)
        st.session_state['num2'] = random.randint(1, 10)

    else:
        st.error("Incorrect captcha. Please try again.")


#---------- Show Results -----------------
st.header("Results")
st.write("The results are presented as a dataframe.")

df = get_results()
st.dataframe(df, use_container_width=True)

# -------------- Download Button------------------ 
df = get_results()
st.download_button(
    label="Download data as CSV",
    data=df.to_csv().encode("utf-8"),
    file_name="survey_results.csv",
    mime="text/csv",
)

# -------------- Visualize  ------------------ 
st.header("Analysis of DataResults")
fig = px.bar(df, x='id', y='count', color='choice_text', title='Survey Results',
             labels={'id':'Question ID', 'count':'Number of Responses', 'choice_text':'Choice'},
             template='plotly_dark')

st.plotly_chart(fig)

# ------- Vis Part 2: an array of bar graph figures, one for each question 
# figures = []

# for q in df['question_text'].unique():
#     # Filter the data for the current question
#     data = df[df['question_text'] == q]
    
#     # Create a bar chart for the current question
#     fig = px.bar(data, x='choice_text', y='count', title=q)
#     fig.update_layout(showlegend=False)
#     fig.update_xaxes(title_text="Response")
#     fig.update_yaxes(title_text="Count")
    
#     # Append the figure to the list of figures
#     figures.append(fig)

# # Choose which graph to display with a set of radio buttons
# if not df.empty:
#     st.info("### Choose the graph for a specific question")
#     f = st.radio("Choose a graph", options=df['question_text'].unique())
#     column_index = list(df['question_text'].unique()).index(f)
#     st.plotly_chart(figures[column_index])
# else:
#     st.warning("No data available to display.")


# survey = get_survey()
# results = get_results()

# figures = []

# # Iterate over each question in the survey
# for q in survey['question'].unique():
#     # Get the list of all choices for the current question
#     choices = survey[survey['question'] == q]['choices'].iloc[0].split(', ')
    
#     # Filter the results for the current question
#     data = results[results['question_text'] == q]
    
#     # Create a DataFrame with all choices and zero counts
#     all_choices = pd.DataFrame({'choice_text': choices, 'count': [0] * len(choices)})
    
#     # Merge the data with the all_choices DataFrame
#     data = pd.merge(all_choices, data, on='choice_text', how='left')
    
#     # Merge the data with the all_choices DataFrame
#     data = pd.merge(all_choices, data, on='choice_text', how='left', suffixes=('', '_y'))

#     # Fill missing values with zero
#     data['count'] = data['count'].fillna(0)
    
#     # Create a bar chart for the current question
#     fig = px.bar(data, x='choice_text', y='count', title=q)
#     fig.update_layout(showlegend=False)
#     fig.update_xaxes(title_text="Response")
#     fig.update_yaxes(title_text="Count")
    
#     # Append the figure to the list of figures
#     figures.append(fig)

# # Choose which graph to display with a set of radio buttons
# if not results.empty:
#     st.info("### Choose the graph for a specific question")
#     f = st.radio("Choose a graph", options=survey['question'].unique())
#     column_index = list(survey['question'].unique()).index(f)
#     st.plotly_chart(figures[column_index])
# else:
#     st.warning("No data available to display.")


df = get_survey()
results = get_results()

# Create a list of figures, one for each question
figures = []
for q in df['question'].unique():
    # Filter the data for the current question
    data = results[results['question_text'] == q]
    
    # Get all choices for the current question
    choices = df[df['question'] == q]['choices'].iloc[0].split(', ')
    
    # Create a bar chart for the current question
    fig = px.bar(data, x='choice_text', y='count', title=q)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="Response", categoryorder='array', categoryarray=choices)
    fig.update_yaxes(title_text="Count")
    
    # Append the figure to the list of figures
    figures.append(fig)

# Choose which graph to display with a set of radio buttons
if not df.empty:
    st.info("### Choose the graph for a specific question")
    f = st.radio("Choose a graph", options=df['question'].unique())
    column_index = list(df['question'].unique()).index(f)
    st.plotly_chart(figures[column_index])
else:
    st.warning("No data available to display.")
