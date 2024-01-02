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
        page_title="Hello",
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
