import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set up page configuration for a wide layout
st.set_page_config(page_title="Salesforce Dashboard", layout="wide")

# Inject CSS to hide scrollbars and reduce padding, plus set fixed height
st.markdown(
    """
    <style>
    body {
        overflow-y: hidden;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        margin-bottom: 0.5rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    .main {
        height: 100vh;  /* Full height of the viewport */
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load dataset
@st.cache
def load_data():
    return pd.read_excel("cleaned_dataset.xlsx")

data = load_data()

# Sidebar filter for customer type selection
st.sidebar.header("Filters")
segment_filter = st.sidebar.selectbox("Select Customer Segment", options=['All'] + list(data['Type'].unique()))

# Filter data based on selected segment
filtered_data = data if segment_filter == 'All' else data[data['Type'] == segment_filter]

# Main title
st.markdown("## Salesforce Data 2024 Dashboard")

# --- Row 1: Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("Customer Name Count")
    name_count = filtered_data['Name'].value_counts().reset_index(name='Count')
    st.dataframe(name_count.head(3), height=100)

with col2:
    st.caption("New Customers Created per Month")
    
    # Ensure 'CreatedDate' is in datetime format
    filtered_data['CreatedDate'] = pd.to_datetime(filtered_data['CreatedDate'], errors='coerce')

    # Create 'CreatedDate_Month' column for grouping by month-year
    filtered_data['CreatedDate_Month'] = filtered_data['CreatedDate'].dt.to_period('M')

    # Count distinct customers (Name) for each month
    new_customers_per_month = filtered_data.groupby('CreatedDate_Month')['Name'].nunique().reset_index()

    # Rename the column for clarity
    new_customers_per_month.columns = ['CreatedDate_Month', 'Num_New_Customers']

    # Convert 'CreatedDate_Month' back to string format (YYYY-MM)
    new_customers_per_month['CreatedDate_Month'] = new_customers_per_month['CreatedDate_Month'].astype(str)
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted figure size for readability
    ax.plot(new_customers_per_month['CreatedDate_Month'], new_customers_per_month['Num_New_Customers'], color='skyblue', marker='o')
    ax.set_xticklabels(new_customers_per_month['CreatedDate_Month'], rotation=45, fontsize=8)
    ax.set_title('')
    st.pyplot(fig)

with col3:
    st.caption("Revenue per Customer Segment")
    revenue = filtered_data.groupby('Type')['SFA_Credit_Monitoring__c'].sum() / 1_000_000_000
    st.bar_chart(revenue)

# --- Row 2: Created Date & Credit Class ---
col4, col5 = st.columns(2)

with col4:
    st.caption("Customer Created Date")
    created_date_count = filtered_data.groupby(filtered_data['CreatedDate'].dt.to_period('M')).size()
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted figure size for better readability
    ax.plot(created_date_count.index.astype(str), created_date_count.values, color='lightgreen', marker='s')
    ax.set_xticklabels(created_date_count.index.astype(str), rotation=45, fontsize=8)
    ax.set_title('')
    st.pyplot(fig)

# Section for "Customer Credit Class Distribution" using Plotly Treemap
with col5:
    st.caption("Customer Credit Class Distribution")
    
    # Get the value counts for Customer Credit Class
    credit_class_dist = filtered_data['SFA_Credit_Class__c'].value_counts().reset_index()
    credit_class_dist.columns = ['Credit Class', 'Count']

    # Create the treemap using Plotly
    fig = px.treemap(credit_class_dist, 
                     path=['Credit Class'], 
                     values='Count', 
                     color='Count', 
                     color_continuous_scale='Blues',
                     title="Customer Credit Class Distribution")

    # Show the treemap in Streamlit
    st.plotly_chart(fig)

# --- Row 3: Bill Handling Code & Status Reason ---
col6, col7 = st.columns(2)

with col6:
    st.caption("Bill Handling Code Distribution")
    
    # Get the value counts for Bill Handling Code
    bill_handling_dist = filtered_data['SFA_Bill_Handling_Code__c'].value_counts().reset_index()
    bill_handling_dist.columns = ['Bill Handling Code', 'Count']

    # Create the treemap using Plotly
    fig = px.treemap(bill_handling_dist, 
                     path=['Bill Handling Code'], 
                     values='Count', 
                     color='Count', 
                     color_continuous_scale='Blues',
                     title="Bill Handling Code Distribution")

    # Show the treemap in Streamlit
    st.plotly_chart(fig)

with col7:
    st.caption("Status Reason")
    
    # Get the value counts for SFA_Status_Reason__c
    bill_handling_dist = filtered_data['SFA_Status_Reason__c'].value_counts()
    
    # Create the barplot
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted size for better label spacing
    sns.barplot(x=bill_handling_dist.index, y=bill_handling_dist.values, ax=ax, palette='Blues')
    
    # Adjust x-axis labels to make them more readable
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)  # Rotating 45 degrees for better visibility
    ax.set_title('')
    
    # Set axis labels for clarity
    ax.set_xlabel('Status Reason', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    
    # Display the plot
    st.pyplot(fig)
