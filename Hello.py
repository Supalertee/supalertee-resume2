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

image = Image.open('image.png')
st.image(image, width=250)

st.sidebar.success("Select a section above.")

st.markdown('## Summary', unsafe_allow_html=True)
st.info('''
    - Entry-level research scientist in theoretical physics and gravity/condensed matter theory duality expertise.
    - With a wealth of experience in both working and residing in diverse cultural environments.
    - test3.
    ''')



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
## Hand on Academic projects
''')
txt4('ABCpred', 'A web server for the discovery of acetyl- and butyryl-cholinesterase inhibitors', 'http://codes.bio/abcpred/')
txt4('AutoWeka', 'An automated data mining software based on Weka', 'http://www.mt.mahidol.ac.th/autoweka/')
txt4('ACPred', 'A computational tool for the prediction and analysis of anticancer peptides','http://codes.bio/acpred/')
txt4('BioCurator', 'A web server for curating ChEMBL bioactivity data', 'http://codes.bio/biocurator/')
txt4('CryoProtect', 'A web server for classifying antifreeze proteins from non-antifreeze proteins','http://codes.bio/cryoprotect/')
txt4('ERpred', 'A web server for the prediction of subtype-specific estrogen receptor antagonists', 'http://codes.bio/erpred')
txt4('HCVpred', 'A web server for predicting the bioactivity of Hepatitis C virus NS5B inhibitors', 'http://codes.bio/hemopred/')
txt4('HemoPred', 'A web server for predicting the hemolytic activity of peptides', 'http://codes.bio/hemopred/')
txt4('iQSP', 'A sequence-based tool for the prediction and analysis of quorum sensing peptides', 'http://codes.bio/iqsp/')
txt4('Meta-iAVP', 'A sequence-based meta-predictor for improving the prediction of antiviral peptides', 'http://codes.bio/meta-iavp/')
txt4('osFP', 'A web server for predicting the oligomeric state of fluorescent proteins', 'http://codes.bio/osfp/')
txt4('PAAP', 'A web server for predicting antihypertensive activity of peptides', 'http://codes.bio/paap/')
txt4('PepBio', 'A web server for predicting the bioactivity of host defense peptide', 'http://codes.bio/pepbio')
txt4('PyBact', 'Open source software written in Python for bacterial identification', 'https://sourceforge.net/projects/pybact/')
txt4('TargetAntiAngio', 'A sequence-based tool for the prediction and analysis of anti-angiogenic peptides','http://codes.bio/targetantiangio/')
txt4('ThalPred', 'Development of decision model for discriminating Thalassemia trait and Iron deficiency anemia','http://codes.bio/thalpred/')
txt4('THPep', 'A web server for predicting tumor homing peptides','http://codes.bio/thpep/')


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
