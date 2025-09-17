#---------------------------------------------------------------------------------------------------------------------------------
### Authenticator
#---------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
#---------------------------------------------------------------------------------------------------------------------------------
### Template Graphics
#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
### Import Libraries
#---------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import plotly.express as px

#---------------------------------------------------------------------------------------------------------------------------------
### Title for your Streamlit app
#---------------------------------------------------------------------------------------------------------------------------------
#import custom_style()
st.set_page_config(page_title="Investment Studio | v1.0",
                   layout="wide",
                   page_icon="💻",              
                   initial_sidebar_state="auto")
#---------------------------------------------------------------------------------------------------------------------------------
### CSS
#---------------------------------------------------------------------------------------------------------------------------------
st.markdown(
        """
        <style>
        .centered-info {display: flex; justify-content: center; align-items: center; 
                        font-weight: bold; font-size: 15px; color: #007BFF; 
                        padding: 5px; background-color: #FFFFFF;  border-radius: 5px; border: 1px solid #007BFF;
                        margin-top: 0px;margin-bottom: 5px;}
        .stMarkdown {margin-top: 0px !important; padding-top: 0px !important;}                       
        </style>
        """,unsafe_allow_html=True,)

#---------------------------------------------------------------------------------------------------------------------------------
### Description for your Streamlit app
#---------------------------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .title-large {
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .title-small {
        text-align: center;
        font-size: 20px;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <div class="title-large">Investment Studio</div>
    <div class="title-small">Version : 1.0</div>
    """,
    unsafe_allow_html=True
)

#----------------------------------------
st.divider()
#----------------------------------------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F0F2F6;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        z-index: 100;
    }
    .footer p {
        margin: 0;
    }
    .footer .highlight {
        font-weight: bold;
        color: blue;
    }
    </style>

    <div class="footer">
        <p>© 2025 | Created by : <span class="highlight">Avijit Chakraborty</span> | <a href="mailto:avijit.mba18@gmail.com"> 📩 </a></p> <span class="highlight">Thank you for visiting the app | Unauthorized uses or copying is strictly prohibited | For best view of the app, please zoom out the browser to 75%.</span>
    </div>
    """,
    unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------
### Functions & Definitions
#---------------------------------------------------------------------------------------------------------------------------------
def calculate_investment(principal, step_up_percent, step_up_frequency, interest_rate, years):
    # Convert annual interest rate to monthly
    monthly_rate = interest_rate / 12 / 100
    total_months = years * 12
    principal_list = []
    interest_list = []
    total_list = []
    months_list = []
    current_principal = principal
    accumulated_amount = principal
    frequency_dict = {
        'Monthly': 1,
        'Quarterly': 3,
        'Half Yearly': 6,
        'Yearly': 12}
    step_up_months = frequency_dict[step_up_frequency]
    for month in range(1, total_months + 1):
        interest = accumulated_amount * monthly_rate
        accumulated_amount += interest
        if month % step_up_months == 0:
            step_up_amount = current_principal * (step_up_percent / 100)
            current_principal += step_up_amount
            accumulated_amount += step_up_amount
        principal_list.append(current_principal)
        total_list.append(accumulated_amount)
        interest_list.append(accumulated_amount - current_principal)
        months_list.append(month)
    return months_list, principal_list, interest_list, total_list

#---------------------------------------------------------------------------------------------------------------------------------
### Main App
#---------------------------------------------------------------------------------------------------------------------------------

col1, col2= st.columns((0.15,0.85))
with col1:           
    with st.expander("**⚙️ Parameters**", expanded=True):
    
        principal = st.number_input("**Initial Principal Amount**", min_value=0, value=10000)
        step_up_percent = st.number_input("**Step-up Percentage (%)**", min_value=0.0, max_value=100.0, value=5.0,help="Percentage increase in principal at each step-up interval")
        step_up_frequency = st.selectbox("**Step-up Frequency**",options=['Monthly', 'Quarterly', 'Half Yearly', 'Yearly'])
        interest_rate = st.number_input("**ROI (%)**", min_value=0.00, value=8.00)
        years = st.number_input("**Period (Years)**", min_value=1, value=5)
    
    months, principal_values, interest_values, total_values = calculate_investment(principal, step_up_percent, step_up_frequency, interest_rate, years)   
    st.info(f"""
        💡 Investment Details:
        - Initial Principal: ₹{principal:,.2f}
        - Step-up: {step_up_percent}% {step_up_frequency.lower()}
        - First step-up amount: ₹{(principal * step_up_percent / 100):,.2f}
        - Last step-up amount: ₹{(principal_values[-2] * step_up_percent / 100):,.2f}
        - ROI : {interest_rate:,.2f} | Investment years : {years}
        """)

with col2:
    with st.expander("**📊 Basic Info**", expanded=True):
    
        df = pd.DataFrame({'Month': months,'Principal': principal_values,'Interest': interest_values,'Total': total_values})
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7) 

        col1.metric("**Total Principal**", f"₹{principal_values[-1]:,.2f}")
        col2.metric("**Total Interest**", f"₹{interest_values[-1]:,.2f}")
        col3.metric("**Total Value**", f"₹{total_values[-1]:,.2f}")

    col1, col2= st.columns((0.65,0.35))
    with col1: 
        with st.expander("**📊 Visualizations**", expanded=True):
                fig = px.line(df, x='Month', y=['Principal', 'Interest', 'Total'],
                            title='Growth Chart',labels={'value': 'Amount (₹)', 'variable': 'Component'})
                st.plotly_chart(fig, use_container_width=True)
    
    with col2: 
        with st.expander("**📝 Detailed Calculations**", expanded=True):
            st.dataframe(df)

