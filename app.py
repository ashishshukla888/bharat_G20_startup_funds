import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout='wide',page_title = 'Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')

#df['year'] = df['date'].dt.year

df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_overall_analysis():
    st.title('Load Overall Analysis')
    
    # total invested amount 
    total = round(df['amount'].sum())
    
    # max amount infused in a startup
    max_funding = round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])
    
    # mean amount infused in a startup
    mean_funds = round(df.groupby('startup')['amount'].sum().mean())
    
    # total funded startups
    num_startup = round(df['startup'].nunique())
    
    
    col1,col2,col3,col4 = st.columns(4)
    
    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('MAX',str(max_funding) + ' Cr')
    with col3:
        st.metric('AVG',str(mean_funds) + ' Cr')
    with col4:
        st.metric('Funded startup',num_startup)
        
    st.header('MOM Graph')
    selected_option = st.selectbox('Select type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str')+ '-' + temp_df['year'].astype('str')
    fig5,ax5 = plt.subplots()
    ax5.bar(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig5)
    
        
    
def load_investor_details(investor):
    st.title(investor)
    # load the recent five investment of the investor
    last_five_df = df[df['inverstor'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_five_df)
    
    col1,col2 = st.columns(2)
    
    with col1:
        
        #biggest investment
        big_series = df[df['inverstor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        #st.dataframe(big_series)
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    
    with col2:
        vertical_series = df[df['inverstor'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Invested In')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
        
    col3,col4 = st.columns(2)
    
    with col3:
        
        #stage wise investment
        stage_investor = df[df['inverstor'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage Investor')
        fig2,ax2 = plt.subplots()
        ax2.pie(stage_investor,labels=stage_investor.index,autopct="%0.01f%%")
        st.pyplot(fig2)
    
    with col4:
        # city wise investment
        city_investor = df[df['inverstor'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Wise Investment')
        fig3,ax3 = plt.subplots()
        ax3.pie(city_investor,labels=city_investor.index,autopct="%0.01f%%")
        st.pyplot(fig3)
        
    df['year'] = df['date'].dt.year
    year_series = df[df['inverstor'].str.contains(investor)].groupby('year')['amount'].sum()
    #.plot(kind='line')
    st.subheader('year on year analysis')
    fig4,ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)
    
        
    
#st.dataframe(df)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overa all analysis','Startup','Funding'])

if option == 'Overa all analysis':
    #st.title('Overall Analysis')
#     btn0 = st.sidebar.button('show Overall analysis')
#     if btn0:
      load_overall_analysis()
    
elif option == 'Startup':
    st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('find startup details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('select startup',sorted(set(df['inverstor'].str.split(',').sum())))
    btn2 = st.sidebar.button('find investor details')
    if btn2: # to check weather the button has been pressed or not 
        load_investor_details(selected_investor)
        
    #st.title('Investor Analysis') 