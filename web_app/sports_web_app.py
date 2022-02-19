import streamlit as st

import json
import os
import pandas as pd
import numpy as np

import networkx as nx
from pyvis.network import Network
import itertools

####################################################################

times = ['Monday 9:00','Monday 14:00','Monday 18:00',
         'Tuesday 9:00','Tuesday 14:00','Tuesday 18:00',
         'Wednesday 9:00','Wednesday 14:00','Wednesday 18:00',
         'Thursday 9:00','Thursday 14:00','Thursday 18:00',
         'Friday 9:00','Friday 14:00','Friday 18:00']

####################################################################

def read_json_to_df(filename):
    
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    
    for key in list(data):
        if not key:
            del data[key]
        else:
            data[key] = ['Yes' if time in data[key] else 'No' for time in times]
    
    dataframe = pd.DataFrame(data.values(), columns=times, index=data.keys())

    return dataframe

def availablilities_to_json(filename):
    
    with st.sidebar.form(key='availability-details'):
        name = st.text_input("What's your name?")
        slots = st.multiselect('What times are you free?', times)
        submit_availabilities = st.form_submit_button('Submit')

    if os.path.getsize(filename) != 0:
        file = open(filename,"r")
        data = json.load(file)
        file.close()
        data[name] = slots
    else:
        data = {name: slots}

    file = open(filename,"w")
    json.dump(data, file)
    file.close()

####################################################################

st.set_page_config(page_title='Rowing matcher', layout='wide')

with st.sidebar.form(key='page-selection'):
    page = st.selectbox('Page', ['','Schedules','Solver'])
    submit_page = st.form_submit_button('Submit')

####################################################################


if page == '':
    
    st.title('Welcome!')
    st.write("This is the rowing match website. Please enter your availabilities on the 'Schedules' tab.")


if page == 'Schedules':

    st.title('Schedules')
    st.write('Please enter your name, and select the times you are avaiable on the left. The table below will then be updated accordingly.')
    
    availablilities_to_json("schedules.json")

    df = read_json_to_df("schedules.json")

    st.write('Rower availabilities:')
    st.dataframe(df)


if page == 'Solver':

    st.title('Solver')
    
    df = read_json_to_df("schedules.json")
    
    slots = []
    
    for time in df.columns:
        X = df[df[time] == 'Yes'].index
        Y = list(itertools.combinations(X,2))
        Z = [y + (time,) for y in Y]
        slots += Z

    slots_df = pd.DataFrame(slots, columns=['Rower 1','Rower 2','Time'])

    G = nx.from_pandas_edgelist(slots_df, 'Rower 1', 'Rower 2')
    matchings = nx.algorithms.matching.maximal_matching(G)
    matchings_df = pd.DataFrame(matchings, columns=['Rower 1','Rower 2'])

    match_times = []
    for match in matchings:
        times = []
        df3 = df.loc[match,:]
        for time in df.columns:
            if df3[time].nunique() == 1:
                if df3[time].unique() == 'Yes':
                    times.append(time)
        match_times.append(times)

    matchings_df['times'] = match_times

    st.write('Matches:')
    st.dataframe(matchings_df)
    
    matched = list(matchings_df['Rower 1']) + list(matchings_df['Rower 2'])
    unmatched = list(set(df.index) - set(matched))
    unmatched_df = pd.DataFrame(unmatched)
    
    st.write('Unallocated:')
    st.write(unmatched_df, columns=['Rower'])