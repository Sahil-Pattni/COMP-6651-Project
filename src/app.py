# %%
from time import sleep, time
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
from coloring.fit_first import fit_first
from coloring.CBIP import cbip
from utils import generate_k_colorable_graph, generate_pyvis_graph
import numpy as np
# %%
# Set config
st.set_page_config(
        page_title="Online Coloring",
        page_icon="✅",
        layout="wide",
)


# --- GLOBAL VARIABLES --- #
if 'G' not in st.session_state:
    st.session_state['G'] = generate_k_colorable_graph(3, 10, 0.4)
if 'layout' not in st.session_state:
    st.session_state['layout'] = None
if 'df' not in st.session_state:
    st.session_state['df'] = None

# Set default option
if 'option' not in st.session_state:
    st.session_state['option'] = 'FirstFit'

for char in ['k', 'n', 'e', 'p']:
    if char not in st.session_state:
        st.session_state[char] = 0

placeholder = st.empty()
container = placeholder.container()



# --- SIDEBAR --- #
# Heading
st.sidebar.title("Graph Generator")
# Set options 
# Option to select the online coloring method
option = st.sidebar.selectbox(
    "Online Coloring Method",
    ("FirstFit", "CBIP")
)
st.session_state['option'] = option


# Input box for chromatic number
k = st.sidebar.number_input("Chromatic Number", min_value=1, max_value=4, value=2)
st.session_state['k'] = k

# Input box for number of nodes
n = st.sidebar.number_input("Number of vertices", min_value=1, value=10)
st.session_state['n'] = n

# Input box for number of edges
N = st.sidebar.number_input("Number of graphs to generate", min_value=1,value=1)
st.session_state['N'] = N

# Input box for probability of edge creation
p = st.sidebar.number_input("Probability of edge creation", min_value=0.0, max_value=1.0, value=0.7)
st.session_state['p'] = p

# Button to generate graph
if st.sidebar.button("Generate Graph"):
    start_time = time()
    # Clear container
    placeholder = st.empty()
    container = placeholder.container()
    with container:
        progress_bar = st.sidebar.progress(0)
        
        study_data = []

        for i in range(N):
            # Generate graph
            G = generate_k_colorable_graph(
                st.session_state['k'],
                st.session_state['n'],
                st.session_state['p']
            )

            color_fn = fit_first if st.session_state['option'] == 'FirstFit' else cbip
            
            for idx in range(2, st.session_state['n']+1):
                subgraph = G.subgraph(range(idx))
                colors = color_fn(subgraph)
                # Assign colors to graph
                for node in subgraph.nodes:
                    G.nodes[node]['group'] = colors[node]

            # Number of unqiue colors used
            colors = set([subgraph.nodes[x]['group'] for x in subgraph.nodes])
            num_colors = len(colors)


            # Update competitive ratio
            ratio = num_colors / k
            study_data.append((st.session_state['k'], st.session_state['n'], num_colors, ratio, st.session_state['N']))
            delta = study_data[-1][3] if len(study_data) >= 1 else 0
            ratios = [x[3] for x in study_data]

            # Update progress bar
            print(f'Progress: {i}/{N}')
            progress_bar.progress(i/N)

        # Show metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Avg. Competitive Ratio", value=f'{np.mean(ratios):,.2f}', delta=delta)
        with col2:
            st.metric(label="Colors Used", value=num_colors)

        # Show last result
        # Generate pyvis graph
        layout_scale = st.session_state['n'] * 15
        if k == 2:
            layout = nx.bipartite_layout(G, nx.bipartite.sets(G)[0], scale=layout_scale)
        else:
            layout = nx.multipartite_layout(G, 'group', scale=layout_scale*1.5)
        PG = generate_pyvis_graph(G, layout)
        # Save graph to HTML
        PG.show("html/nx.html")
        # Display graph
        components.html(open("html/nx.html", "r").read(), height=750)

        # Show data
        # Header
        st.header("Data")
        # Generate dataframe
        df = pd.DataFrame(study_data, columns=['k', 'n', 'colors_used', 'ratio', 'N'])
        # Show dataframe
        st.dataframe(df)

        end_time = time()
        st.write(f'Elapsed time: {end_time - start_time:,.3f} second(s)')
# # %%

## %%
