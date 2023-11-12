import streamlit as st
import pandas as pd
from utils.app_utils_functions import clean_new_campaign_data, clean_contact_df, recommend, preproces_df

# Streamlit UI
st.title('Post a csv file and get recommendations')

# make it possible to input a csv file
uploaded_file = st.file_uploader("Choose a file")

# if a file is uploaded
if uploaded_file is not None:
    # read the file
    df = pd.read_csv(uploaded_file)
    # clean the dataframe
    df_clean = pd.DataFrame()
    try:
        df_clean = clean_new_campaign_data(df)
    except Exception as e:
        error_type = e.__getattribute__('__class__').__name__
        if error_type == 'KeyError':
            st.write(f"{error_type}: {e} not found in the csv file")
        else:
            st.write(f"{error_type}: {e}")
    # display the dataframe
    if df_clean.empty:
        st.write('Something went wrong, please check the error message above')
    else:
        st.write(df)
        # type a campaign id to give recommendations for
        campaign_id = st.text_input("Enter a campaign ID for recommendation")
        if campaign_id:
            try:
                df_clean = df_clean[df_clean['campagne_campagne_id'] == campaign_id]
                if df_clean.empty:
                    st.write('Campaign ID not found')
                else:
                    top_n = st.text_input('How many recommendations do you want?', value=10)
                    # make sure the input is a number
                    try:
                        top_n = int(top_n)
                    except:
                        st.write('Please enter a number')
                        top_n = 10
                    # get the hulp dataframe
                    df_hulp = preproces_df()
                    # turn df_clean which is only 1 row into a dataframe, into a string
                    df_clean = df_clean.to_string(header=False, index=False, index_names=False)
                    # get the recommendations
                    response_list = recommend(df_hulp, df_clean, top_n=top_n)
                    # turn into dataframe
                    response_df = pd.DataFrame(response_list)
                    # rename columns
                    response_df.rename(columns={0: 'contact_contactpersoon_id', 1: 'marketing_pressure'}, inplace=True)
                    # getting other information about the contact persons
                    response_df = clean_contact_df(response_df['contact_contactpersoon_id'], df_hulp)
                    # display the response
                    st.write('Recommended contact persons')
                    st.write(response_df)
            except Exception as e:
                st.write('Something went wrong, please try again\n', e)

   

