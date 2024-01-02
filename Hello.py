# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from PIL import Image



LOGGER = get_logger(__name__)

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
def run():
    st.set_page_config(
        page_title="Resume",
        page_icon="👋",
    )
    
st.write("# Welcome to My Portfolio  ! 👋")

st.write('''
# Supalert Sukrakarn, M.Sc. 
''')

st.latex(r'''
    G_{\mu\nu} = gT_{\mu\nu}
    ''')

image = Image.open('image.png')
st.image(image, width=250)

st.sidebar.success("Select a section above.")

st.markdown('## Summary', unsafe_allow_html=True)
st.info('''
    - Entry-level research scientist in theoretical physics and gravity/condensed matter theory duality expertise.
    - With a wealth of experience in both working and residing in diverse cultural environments.
    - test3.
    ''')

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #16A2CB;">
  <a class="navbar-brand" href="https://linkedin.com/in/sukrakarn" target="_blank">Supalert Sukrakarn</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="/">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#education">Education</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#work-experience">Work Experience</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#hand-on-academic-projects"> Hand on Academic projects</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

#####################
# Custom function for printing text
def txt(a, b):
  col1, col2 = st.columns([4,1])
  with col1:
    st.markdown(a)
  with col2:
    st.markdown(b)

def txt2(a, b):
  col1, col2 = st.columns([1,4])
  with col1:
    st.markdown(f'`{a}`')
  with col2:
    st.markdown(b)

def txt3(a, b):
  col1, col2 = st.columns([1,2])
  with col1:
    st.markdown(a)
  with col2:
    st.markdown(b)
  
def txt4(a, b, c):
  col1, col2, col3 = st.columns([1.5,2,2])
  with col1:
    st.markdown(f'`{a}`')
  with col2:
    st.markdown(b)
  with col3:
    st.markdown(c)

#####################
st.markdown('''
## Work Experience
''')

txt('**Theoretical Physics Research Scientist**, String and Manybodys Group, Faculty of Natural Sciences, Hanyang University, Republic of Korea',
'2023-2024')
st.markdown('''
- Conducted and published academic research that fulfills a way to understand solid-state physics which had been mysterious for  ` 20` years.
- Played a key role in the success of the group's groundbreaking research project on the physics frontier of topology, which resulted in significant funding from the Korean government.
- Optimized complex computations, an integrated approach was developed utilizing the programming languages `Wolfram Mathematica`, `Python`, and `Julia`. This resulted in a significant improvement, with numerical calculations being approximately  ` 1000` times faster than the original method.
- Develop numerical/analytical calculations and machine learning to solve systems of non-linear `3 and more ` coupled differential equations.
''')

#####################
st.markdown('''
## Education
''')

txt('**Master of Science** (Physics), *Hanyang University* , Republic of Korea',
'2021-2023')
st.markdown('''
- GPA: `4.44`
- Research thesis entitled `Symmetry Breaking Effect in Holographic Fermions `.
- Received Korean Government Scholarship (GKS) covering tuition and stipend for 3 years.
''')

txt('**Bachelors of Science** (Physics), *Mahidol University*, Thailand',
'2015-2019')
st.markdown('''
- GPA: `3.39`
- Research thesis entitled `Perturbative Quantum Gravity with Application in Dark Matter Annihilation`.
 - Best Senior Project Award, The 12th Senior Research Project Competition, organized by the Thai Physics Society.
''')

####################

#####################
st.markdown('''
## Hand on Academic projects
''')
txt4('ABCpred', 'A web server for the discovery of acetyl- and butyryl-cholinesterase inhibitors', 'http://codes.bio/abcpred/')



#####################
st.markdown('''
## Skills
''')
txt3('Programming', '`Python`, `R`, `Linux`')
txt3('Data processing/wrangling', '`SQL`, `pandas`, `numpy`')
txt3('Data visualization', '`matplotlib`, `seaborn`, `plotly`, `altair`, `ggplot2`')
txt3('Machine Learning', '`scikit-learn`')
txt3('Deep Learning', '`TensorFlow`')
txt3('Web development', '`Flask`, `HTML`, `CSS`')
txt3('Model deployment', '`streamlit`, `gradio`, `R Shiny`, `Heroku`, `AWS`, `Digital Ocean`')

#####################
