
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Salesforce 2024 Dashboard", layout="wide")

st.markdown("""
<style>
    body { overflow-y: hidden; }
    .block-container { padding-top: 0.2rem; padding-bottom: 0.2rem; }
    .main { height: 100vh; overflow: hidden; }
    .element-container { margin-bottom: 0.2rem !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("cleaned_dataset.xlsx")
    df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], errors='coerce')
    df['LastActivityDate_Opportunity'] = pd.to_datetime(df['LastActivityDate_Opportunity'], errors='coerce')
    df['CreatedDate_Month'] = df['CreatedDate'].dt.to_period('M').astype(str)
    df['SFA_Credit_Monitoring__c'] = df['SFA_Credit_Monitoring__c'].fillna(0)
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("Filters")
type_filter = st.sidebar.selectbox("Customer Type", ['All'] + sorted(df['Type'].dropna().unique().tolist()))
if type_filter != 'All':
    df = df[df['Type'] == type_filter]

# Title and KPIs
st.markdown("## Salesforce 2024 Dashboard")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customers", f"{df['Name'].nunique():,}")
latest_month = df['CreatedDate_Month'].max()
k2.metric(f"New Customers ({latest_month})", f"{df[df['CreatedDate_Month'] == latest_month]['Name'].nunique():,}")
total_credit = df['SFA_Credit_Monitoring__c'].sum()
k3.metric("Total Credit Value", f"{total_credit/1_000_000_000:.2f} B IDR")
avg_credit = df['SFA_Credit_Monitoring__c'].mean()
k4.metric("Avg Credit / Customer", f"{avg_credit:,.0f} IDR")

# Row 1: Credit by Type + Credit Class (Treemap) + Account Status (Bar)
r1c1, r1c2, r1c3 = st.columns(3)

with r1c1:
    st.caption("Credit Value by Customer Type")
    by_type = df.groupby('Type')['SFA_Credit_Monitoring__c'].sum().reset_index()
    fig1 = px.bar(by_type, x='Type', y='SFA_Credit_Monitoring__c', height=250)
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    st.caption("Credit Class Distribution (Treemap)")
    by_class = df['SFA_Credit_Class__c'].value_counts().reset_index()
    by_class.columns = ['Credit Class', 'Count']
    fig2 = px.treemap(by_class, path=['Credit Class'], values='Count', color='Count', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

with r1c3:
    st.caption("Account Status Distribution (Bar)")
    acc_status = df['SFA_Account_Status__c'].value_counts().reset_index()
    acc_status.columns = ['Status', 'Count']
    fig3 = px.bar(acc_status, x='Status', y='Count', color='Count', height=250)
    st.plotly_chart(fig3, use_container_width=True)

# Row 2: New Customers Trend + Communication Channel
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.caption("New Customers Over Time")
    new_month = df.groupby('CreatedDate_Month')['Name'].nunique().reset_index(name='New Customers')
    fig4 = px.line(new_month, x='CreatedDate_Month', y='New Customers', markers=True, height=250)
    st.plotly_chart(fig4, use_container_width=True)

with r2c2:
    st.caption("Communication Channel")
    ch_dist = df['SFA_Channel__c'].value_counts().reset_index()
    ch_dist.columns = ['Channel', 'Count']
    fig5 = px.bar(ch_dist, x='Channel', y='Count', height=250)
    st.plotly_chart(fig5, use_container_width=True)
