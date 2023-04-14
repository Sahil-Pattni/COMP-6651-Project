# %%
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
from coloring.fit_first import fit_first
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
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'max_nodes' not in st.session_state:
        st.session_state['max_nodes'] = np.inf
# Set default option
if 'option' not in st.session_state:
    st.session_state['option'] = 'FirstFit'

for char in ['k', 'n', 'e', 'p']:
    if char not in st.session_state:
        st.session_state[char] = 0

placeholder = st.empty()
container = placeholder.container()



def show_graph(step: int) -> None:
    """
    Display a subgraph of the current graph.

    Parameters
    ----------
    step : int
        Number of nodes to show.
    """
    with container:
        nodes = range(step+1)
        # Show step number
        st.write(f'Step {step:,} | Nodes: {nodes} | Max: {len(st.session_state["G"].nodes)}')
        # Generate subgraph
        _G = st.session_state['G'].subgraph(nodes)
        # Generate appropriate colorings
        if st.session_state['option'] == 'FirstFit':
            _G = fit_first(_G)
        elif st.session_state['option'] == 'CBIP':
            # TODO: Implement CBIP
            pass

        # Generate pyvis graph
        PG = generate_pyvis_graph(_G, st.session_state['layout'])
        # Save graph to HTML
        PG.show("html/nx.html")
        # Display graph
        components.html(open("html/nx.html", "r").read(), height=750)



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
n = st.sidebar.number_input("Number of vertices", min_value=1, value=50)
st.session_state['n'] = n

# Input box for number of edges
e = st.sidebar.number_input("Number of edges", min_value=1,value=100)
st.session_state['e'] = e

# Input box for probability of edge creation
p = st.sidebar.number_input("Probability of edge creation", min_value=0.0, max_value=1.0, value=0.7)
st.session_state['p'] = p

# Button to generate graph
if st.sidebar.button("Generate Graph"):
    # Clear container
    placeholder = st.empty()
    container = placeholder.container()
    # Generate graph
    st.session_state['G'], st.session_state['layout'] = generate_k_colorable_graph(
        st.session_state['k'], 
        st.session_state['n'],
        st.session_state['p']
    )
    st.session_state['max_nodes'] = n
    st.write(f'Graph with {n} nodes and {e} edges.')
    # Reset step
    st.session_state['step'] = 1
    # Show complete graph
    show_graph(st.session_state['max_nodes'])


# --- MAIN --- #
# Button to go to next step
if st.session_state['step'] <= st.session_state['max_nodes']:
    if st.button("Next Step"):
        # Increment step
        st.session_state['step'] += 1
        print(f'Current step: {st.session_state["step"]}')
        show_graph(st.session_state['step'])
else:
    st.write("Done!")
    # Clear container
    container = container.empty()
    # Show complete graph
    show_graph(st.session_state['max_nodes'])



# # %%

# %%
