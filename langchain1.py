# Imports
import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.llms import LLM
import os
import getpass 
from  dotenv import load_dotenv
import google.generativeai as genai

# Define OpenAI API KEY
#os.environ['GOOGLE_API_KEY'] = getpass.getpass('AIzaSyAwTrLqf_Kpq4jvXDOtls9EqpkjKzCGlu0')
genai.configure(api_key="AIzaSyAwTrLqf_Kpq4jvXDOtls9EqpkjKzCGlu0")

# CSS styling
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 85%;
  padding: 0 1.25rem;
  color: #fff;
}
'''
st.write(css, unsafe_allow_html=True)

# Define user and bot templates
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://resizing.flixster.com/ocuc8yjm8Fu5UK5Ze8lbdp58m9Y=/300x300/v2/https://flxt.tmsimg.com/assets/p11759522_i_h9_aa.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.shutterstock.com/image-vector/nerd-robot-vector-illustration-version-260nw-2126944997.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# App Title
st.title("Stock Price Relative Returns AI Tool")
st.caption("Visualizations and OpenAI Chatbot Comparing Multiple Stocks Over A Specified Period")

# Define Stocke Drop Down Menu and Available Stock to choose from
tickers = ['TSL', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD']
dropdown = st.multiselect('Pick Asset:', tickers)

start = st.date_input('Start', value=pd.to_datetime('2023-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

# Define function to convert price to relative returns
def relret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret

# Only when a stock is selected
if len(dropdown) > 0:
    #df = yf.download(dropdown,start,end)['Adj Close']s
    df = relret(yf.download(dropdown,start,end)['Adj Close'])
    st.header("Relative Returns of {}".format(dropdown))
    st.line_chart(df)
    st.header("Chat with your Data") 

     # Accept input from users
    query = st.text_input("Enter a query:") 

    # Execute pandas response logic
    if st.button("Execute") and query:
        with st.spinner('Generating response...'):
            try:

                 # Define pandas df agent - 0 ~ no creativity vs 1 ~ very creative
                #agent = create_pandas_dataframe_agent(genai(temperature=0.5),pd.DataFrame(df),verbose=True) 
                #agent = LLM(model="genai")
                #df_dict = df.to_dict(orient='records')
                #agent.context = df_dict
                #verbose = True
                #agent = genai.GenerativeModel('gemini-1.0-pro-latest')
                # model = genai.GenerativeModel('gemini-1.0-pro-latest')
                model = genai.GenerativeModel('models/gemini-pro')

                # Run agent and retrieve answer
                # answer = model.run(query)
                chat = model.start_chat()
                response = chat.send_message(query)
                answer = response.text


                # Display user query and agents answer
                st.write(user_template.replace("{{MSG}}",query ), unsafe_allow_html=True)
                st.write(bot_template.replace("{{MSG}}", answer ), unsafe_allow_html=True)
                st.write("")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")