import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import datetime

# Initialize Groq API
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(model_name="llama-3.3-70b-specdec", api_key=GROQ_API_KEY)

# Define Prompt Templates
property_search_prompt = PromptTemplate(
    input_variables=["location", "budget", "property_type"],
    template="Find me {property_type} properties in {location} within a {budget} budget."
)

mortgage_calc_prompt = PromptTemplate(
    input_variables=["home_price", "down_payment", "interest_rate", "loan_term"],
    template="Calculate mortgage for a home priced at {home_price} with a down payment of {down_payment}, an interest rate of {interest_rate}%, and a loan term of {loan_term} years."
)

# Create Chains
property_chain = LLMChain(llm=llm, prompt=property_search_prompt) 
mortgage_chain = LLMChain(llm=llm, prompt=mortgage_calc_prompt) 

#property_chain = property_search_prompt|llm|JsonOutputParser()
#mortgage_chain = mortgage_calc_prompt|llm|JsonOutputParser()

# Streamlit UI
st.set_page_config(page_title="Real Estate Property Advisor", layout="wide")
st.title("🏡 Real Estate Property Advisor")

# Property Search
st.header("🔍 Property Search")
location = st.text_input("Enter Location:")
budget = st.text_input("Enter Budget:")
property_type = st.selectbox("Property Type", ["Apartment", "House", "Condo", "Townhouse"])
if st.button("Find Properties"):
    response = property_chain.run({"location": location, "budget": budget, "property_type": property_type})
    st.write("### Suggested Properties:")
    st.write(response)

# Mortgage Calculator
st.header("💰 Mortgage Calculator")
home_price = st.number_input("Home Price ($)", min_value=10000)
down_payment = st.number_input("Down Payment ($)", min_value=0)
interest_rate = st.number_input("Interest Rate (%)", min_value=0.1, max_value=20.0, step=0.1)
loan_term = st.slider("Loan Term (Years)", 5, 30, 15)
if st.button("Calculate Mortgage"):
    mortgage_result = mortgage_chain.run({"home_price": home_price, "down_payment": down_payment, "interest_rate": interest_rate, "loan_term": loan_term})
    st.write("### Monthly Payment Estimate:")
    st.write(mortgage_result)

# Schedule Property Tour
st.header("📅 Schedule a Property Tour")
name = st.text_input("Your Name")
email = st.text_input("Your Email")
visit_date = st.date_input("Select a Date", min_value=datetime.date.today())
if st.button("Schedule Tour"):
    st.success(f"✅ Tour scheduled for {name} on {visit_date}!")

st.sidebar.header("🔗 Integrations")
st.sidebar.write("- MLS API for listings")
st.sidebar.write("- Calendar booking system")
st.sidebar.write("- CRM lead management")
