import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df_clean = pd.read_excel('cleaned_dataset.xlsx')

# Title
st.title("Customer Engagement Dashboard")

# Show dataset info
st.subheader('Data Overview')
st.write(df_clean.info())

# Option for the user to select a feature to visualize
option = st.selectbox(
    'Choose a feature to visualize',
    ['Customer Created per Month', 'Account Active per Month', 'Last Activity per Month', 'Status Updates per Month']
)

# Create the visualizations based on selection
if option == 'Customer Created per Month':
    created_counts = df_clean.groupby('CreatedDate_Month').size().reset_index(name='Num_Created')
    st.subheader("Customer Created per Month")
    st.line_chart(created_counts.set_index('CreatedDate_Month')['Num_Created'])
    
elif option == 'Account Active per Month':
    active_counts = df_clean.groupby('SFA_Active_Date_Month').size().reset_index(name='Num_Active')
    st.subheader("Account Active per Month")
    st.line_chart(active_counts.set_index('SFA_Active_Date_Month')['Num_Active'])
    
elif option == 'Last Activity per Month':
    last_activity_counts = df_clean.groupby('LastActivityDate_Opportunity_Month').size().reset_index(name='Num_LastActivity')
    st.subheader("Last Activity per Month")
    st.line_chart(last_activity_counts.set_index('LastActivityDate_Opportunity_Month')['Num_LastActivity'])
    
elif option == 'Status Updates per Month':
    status_counts = df_clean.groupby('SFA_Status_Date_Month').size().reset_index(name='Num_StatusUpdates')
    st.subheader("Status Updates per Month")
    st.line_chart(status_counts.set_index('SFA_Status_Date_Month')['Num_StatusUpdates'])

# Add a slider for selecting the number of top customers
top_customers = st.slider(
    'Select the number of top customers to visualize',
    min_value=1, max_value=10, value=5
)

# Show top customers based on a specific metric (e.g., total revenue)
top_customers_data = df_clean.groupby('Customer Name New')['SFA_Credit_Monitoring__c'].sum().reset_index()
top_customers_data = top_customers_data.sort_values(by='SFA_Credit_Monitoring__c', ascending=False).head(top_customers)

st.subheader(f"Top {top_customers} Customers by Total Revenue")
st.bar_chart(top_customers_data.set_index('Customer Name New')['SFA_Credit_Monitoring__c'])

# Allow user to filter data based on selected columns (e.g., Customer Segment)
customer_segment = st.selectbox('Select Customer Segment', df_clean['SFA_Customer_Segment__c'].unique())
filtered_data = df_clean[df_clean['SFA_Customer_Segment__c'] == customer_segment]

st.write(f"Filtered Data for Segment: {customer_segment}")
st.write(filtered_data)

# Show an interactive plot (Example: Engagement by Communication Channel)
st.subheader("Customer Engagement by Communication Channel")
engagement_by_channel = df_clean.groupby('SFA_Bill_Handling_Code__c').size().reset_index(name='Num_Engagement')

plt.figure(figsize=(12, 6))
sns.barplot(x='Num_Engagement', y='SFA_Bill_Handling_Code__c', data=engagement_by_channel, palette='Blues')
plt.title('Customer Engagement Based on Communication Channels')
plt.xlabel('Number of Engagements')
plt.ylabel('Communication Channel')
st.pyplot()

