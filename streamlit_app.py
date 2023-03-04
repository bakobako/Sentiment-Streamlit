import streamlit as st
import pandas as pd
import altair as alt

input_dir = '/data/in/tables/'


@st.cache_data
def read_df(file_name, index_col=None, date_col=None):
    return pd.read_csv(input_dir + file_name, index_col=index_col, parse_dates=date_col)


# Load Data
df = read_df('parsed_comment_analysis')

# title
st.title('LinkedIn Comment Analyzer')
st.write("##")
st.markdown("This streamlit app performs analysis on the comments on a specific LinkedIn Post. "
            "The comments are analyzed on their sentiment and whether or not they should be responded to.")
st.write("##")
st.write("##")

# Select Comment
st.header('Select which LinedIn post you want to analyze')
st.write("##")
posts = df['post_text'].drop_duplicates()
post_choice = st.selectbox('Select your Post:', posts)
comments_of_specific_post = df.loc[df["post_text"] == post_choice]
st.write("##")
st.write("##")
st.write("##")

# analyzing comments of the post

st.header('Analysis of the comments on the post')
st.write("##")

# SENTIMENT

data_to_show = comments_of_specific_post["tone"].value_counts()
for column in ["very negative", "negative", "slightly negative", "neutral", "positive", "very positive"]:
    if column not in data_to_show.index:
        # add the column with default value of 0
        data_to_show[column] = 0

data_to_show = data_to_show.reindex(
    index=["very negative", "negative", "slightly negative", "neutral", "positive", "very positive"])
data_to_show = data_to_show.to_frame('counts').reset_index()
data_to_show.rename(columns={'index': 'Sentiment'}, inplace=True)
data_to_show.rename(columns={'counts': 'Comment Counts'}, inplace=True)

bar = alt.Chart(data_to_show).mark_bar().encode(
    x=alt.X('Sentiment', sort=None),
    y='Comment Counts'
)
st.altair_chart(bar, use_container_width=True)

st.write("##")
st.write("##")

# Messages to respond to

st.header('Messages to respond to')
st.markdown("The analysis of the text determined that the following comments should be responded to")
st.write("##")

messages_to_respond = comments_of_specific_post.loc[df['to_respond'], 'comment_text'].tolist()
print(messages_to_respond)


for message in messages_to_respond:
    st.markdown(f"\"{message}\"")
    st.checkbox("Request response", key=message)
    st.write("##")

st.button("Request responses")
