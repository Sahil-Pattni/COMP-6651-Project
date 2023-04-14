# COMP 6651 Project
### Authors: Sahil Pattni, Pablo Ilabaca Parra
---

## Project Description
This project is an empirical study into the relation between the number of vertices in a graph and the average competitive ratio using both the FitFirst and CBIP algorithms.

## Project Structure
The project is structured as follows:
The `src` directory contains all the implementation logic for this project. The `tests` directory holds unit tests used to verify the program's correctness.

## Running the Project
The study of the FitFirst algorithm can be found in the `FitFirst_Study.ipynb` notebook.

The study of the CBIP algorithm can be found in the `CBIP_Study.ipynb` notebook.

Currently, the visualizer can be run from the root directory of this project via the command:
`streamlit run src/app.py`. By the end of the project, this will be replaced with a link to the website on Streamlit.


## Running the tests
The tests can be run from the root directory of this project via the command:
`python -m unittest discover tests`.