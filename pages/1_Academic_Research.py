import streamlit as st
import time
import numpy as np
from scipy.integrate import odeint
import streamlit as st
from streamlit.hello.utils import show_code
from PIL import Image


def xSHM(x, t):
    k= 10000
    m = 1
    return [x[1],-x[0]*k/m]

def xdamp(x, t):
    k= 10000
    m = 1
    b = 15
    return [x[1],-x[0]*k/m - x[1]*b]

def OS(xEOM):
    t = np.arange(0, 0.25+0.25/100, 0.25/100)
    x = odeint(xEOM, [0, 1], t).T[0]
    return x

t = np.arange(0, 0.25+0.25/100, 0.25/100)

def plotting(OS):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.array([[OS[0]]])
    chart = st.line_chart(last_rows)

    for i in range(1, len(t)):
        new_rows = np.array([[OS[i]]])
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.005)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run", key=f"button_{OS}")

tab1, tab2, tab3 = st.tabs(["Gravity/Condensed Matter Theorey Duality", "Dog", "Owl"])

with tab1:

    st.markdown("# Physics Research Interests")

    st.markdown('''
        In theoretical physics, there are a number of mysteriouse questions in gravity and quantum physics. Famous physicists, Albert Einstein, Stephen Hawking, \
        Richard Feynman and others also spent their entire life to unify gravity and elementary particle (quantum physics)''')
    st.markdown(''' The main problem is that the gravity and quantum physics are builded up by differences of fundamental. We now end-up with unification of theories\
            unified theory. The unification is well known as `gauge/gravity duality`. The theories have been developing for 20s years, we now have elementary-particle\
                /gravity duality, fluid-dynamics/gravity duality, Condensed Matter Physics/gravity duality. All of them are simply called `Holographic Principle`''')
    st.markdown('''Holography is a principle that state that weakly interacting classical gravitational gravity in $n+1$ dimensions is equivelent to strongly coupling quantum theory.\
        in $n$ dimensions. Now it is natural to be asked by people "why we need this". The answer is very simple, it is because we cannot \
                solve strongly coupling quantum systems easily, while strongly coupling quantum systems have several extraordinary properties and features, which\
                    might become a part of next generation tenmologies. For example, `superconductivity, Mott insulator, Weyl semimetals, flat-band`, and so-on''')

    st.title('What is the most fundamental concept in theoretical physics?')
    st.markdown(''' There are number of branches of theoretical physics. However, the most basic which every physics studied should to know is Lagrangian and Hamiltion \
                    mechanics. What we done in a simple word is applying calculus of variations to optimize an dynamical variable called Action $(S)$, \
                    in physical principle everythings in the universe in classical level (non-quantum) will behave along the lowest-action path.\
                    every formula in physics on high-school or college are derived by this principle. The result that we perform the optimization is called Euler-Lagrange equations:
                ''')
    st.latex(r'''
        \begin{align}
        \delta S = \int d^nx \delta\mathcal{L} \quad \Rightarrow\quad  \frac{\partial \mathcal{L}}{dx}-\frac{d}{dt}\frac{\partial \mathcal{L}}{d\dot{x}} &= 0
        \end{align}
        ''')
    st.markdown('''where $\mathcal{L}  = $ kinetic energy - potential energy. So I will show you a simple example, spring osillation. So that $\mathcal{L} = \\frac{1}{2}m\dot{x}^2 - \\frac{1}{2}kx^2$\
                by plugging-in $\mathcal{L}$ in Euler-Lagrange equations, we obtain ''')

    st.latex(r''' 
        \begin{align}
        \frac{\partial \mathcal{L}}{dx}-\frac{d}{dt}\frac{\partial \mathcal{L}}{d\dot{x}} \quad=\quad m\ddot{x} - kx \quad=\quad 0
        \end{align}
    ''')
    st.sidebar.markdown("# Equations of motion")

    col1, col2 = st.columns(2)

    with col1:
        st.info(''' So, we obtain a **_differential equation_** called **_Equation of motions:_**  $\displaystyle\ddot{x} - \\frac{k}{m}x = 0$''')
        plotting(OS(xSHM))
    with col2:
        st.info(''' We are also able to modify our model by adding damping, which the **_equation of motions is given:_** $\displaystyle\ddot{x} - \
            \\frac{k}{m}x-b\dot{x} = 0$''')
        plotting(OS(xdamp))


    st.markdown(''' On can see that the periodic moving appears in the solution of spring system which is well known. However, this simple classical physics\
                calculation have been discovered for almost 300 years and it is still working well. So, How is this simple concept applied in modern theoretical physics?''')

    st.title('''How do we study strongly correlated fermions coupled systems via gravity?''')

    st.markdown(''' In this site, I will show just only very very simple concept of my work. If one want to see the full detail please visit , https://doi.org/10.48550/arXiv.2311.01897 ''')

    st.markdown(''' By the way, following the same concept of the least action principle $\delta S = 0$, we can investigate how particle behave, that is most important \
                concept. And of course, the model to describe the system is more uniqe and complicated.''')

    st.latex(r'''
        \begin{align}
        S_{total} &= S_\psi +S_{bdy}+S_{g,\Phi} +S_{int},\\
        S_\psi &= \int d^{5}x \sum_{j=1}^2 \sqrt{-g}~ \bar\psi^{(j)}\Big(\frac1{2} \Gamma^M({\overrightarrow{D}_M-\overleftarrow{D}_M})-m^{(j)}\Big)\psi^{(j)}, \\
        S_{g,\Phi} &= \int d^{5}x \sqrt{-g}\Big(R-2\Lambda + |D_M\Phi_I|^2-m^2_{\Phi}|\Phi|^2\Big),\\
        S_{bdy} &= \frac{i}{2} \int_{bdy} d^4x \sqrt{-h} \Big(\bar{\psi}^{(1)}\psi^{(1)}\pm \bar{\psi}^{(2)}\psi^{(2)}\Big),\\
        S_{int} &= \int d^{5}x \sqrt{-g} \Big(\bar\psi^{(1)}\Phi\cdot\Gamma \psi^{(2)}+h.c \Big)
        \end{align}
        ''')

    st.markdown(''' From these actions, we can derive equation of motions and apply Holographic principle. The main information we extracted from this model is\
    a mathematical object so called **_Green's function_**. In mathematical sence, the Green's function is just a tool to solve differential\
    equation. In holography, we can get the **_boundary Green's function_** which is theoretically physical world. The brief derivation is shown as follow:''')

    st.latex(r''' 
     \begin{align}
    S_{total}^{(\mathbb{Q})}\Big|_{bdy}&= \frac{1}{2} \int_{bdy} d^4x \Big(\xi_S^{\dagger}\Gamma_{bdy}\xi_C + h.c\Big)^{(\mathbb{Q})},\\
    &=  \frac{1}{2} \int_{bdy}d^4x ( \xi_S^{\dagger} \Gamma_{bdy}\mathbb{C} \mathbb{S} ^{-1} \xi_S +h.c)^{(\mathbb{Q})},\\
    &= \frac{1}{2} \int_{bdy}d^4x (\xi_S^{\dagger} \mathbb{G} \xi_S+h.c)^{(\mathbb{Q})}.
    \end{align}
    ''')
    st.latex(r''' \begin{align}
    \mathbb{G}^{(SS)} &=  -(\sigma_0 \otimes \sigma_2)\mathbb{C} \mathbb{S} ^{-1},\quad
    \mathbb{G}^{(SA)}&= -(\sigma_3 \otimes \sigma_2)\mathbb{C} \mathbb{S} ^{-1}.
    \end{align} 
    ''')
    
    st.markdown('''In physical sence, the Green's function contains the information showing how particles correlate to each other. \
    To show the properties of the matter, we can calculate **_Spectral functions_**, which is define as imaginary part of the Green's function''')

    st.markdown(''' the boundary Green's function can be defined as follow''')

    st.latex(r'''A(\omega,k) = \text{Tr}[\text{Im}(\mathbb{G}(\omega,k))]''')

    st.markdown(''' So, the main question is how can we calculate the Green's function? The answer is conceptually simple, we just apply the least-action principle to find\
    the saddle point of the action to get the system of equations of motion. After solving the system of equations of motion, we can apply the Holographic principle \
    and calculate the Green's functions. However, the calculation is really **_non-trivial_** due to complexity of the system of differential equations and most of researh\
    in gauge/gravity duality usully done by numerical calculation approch.

    Lovely!, my team and I can find the way to get analytic results! Simply speaking, we get the exact formula of all spectral functions. This result reduce time \
        we use to solve the spectral function from ` hours / 1 set of parameter ` to `half second`. Additionally, the exact formulas are intutive \
            and can tell use everything that have been hidden in numerical results.''')

    st.header('Realization of Various Dimensional Flat-Bands')            

    st.markdown(''' By considering all tensor types of interaction, We found the pole-type singularity Green's functions. \
            After considering and classification symmetry, various dimensional flat bands are realized as follows: ''')

    st.latex(r'''
    \begin{align*}
    \text{Tr}\mathbb{G}_{M_0}^{(SS)} &= 4\omega\frac{\sqrt{\boldsymbol{k}^2-\omega^2 +M_0^2}}{\boldsymbol{k}^2-\omega^2 -i\epsilon},\\
    \text{Tr}\mathbb{G}_{B_{x}^{(0)}}^{(SA)}  &= \frac{2\omega}{b}\Big[\frac{ (b+k_x)\sqrt{(b - k_x)^2 +\boldsymbol{k}_\perp^2-\omega^2} +(b-k_x)\sqrt{(b + k_x)^2 +\boldsymbol{k}_\perp^2-\omega^2} }{\boldsymbol{k}_\perp^2 - \omega^2 - i \epsilon}\Big],\\
    \text{Tr}\mathbb{G}_{B_{xy}^{(-1)}}^{(SS)}  &= \frac{2\omega}{b}\Big[\frac{ (b+|\boldsymbol{k}_\perp|)\sqrt{(b - |\boldsymbol{k}_\perp|)^2 +k_z^2-\omega^2} +(b-|\boldsymbol{k}_\perp|)\sqrt{(b + |\boldsymbol{k}_\perp|)^2 +k_z-\omega^2} }{k_z^2 - \omega^2-i\epsilon}\Big],\\
    \text{Tr}\mathbb{G}_{B_{tu}^{(-1)}}^{(SA)} &= -\frac{2}{b}\Big[\frac{ (b+|\boldsymbol{k}|)\sqrt{(b-|\boldsymbol{k}|)^2-\omega^2}+(b-|\boldsymbol{k}|)\sqrt{(b+|\boldsymbol{k}|)^2-\omega^2} }{\omega+ i\epsilon}\Big].
    \end{align*} ''')

    st.markdown(''' The Trace of the Green's function is quite complicated and hard to say what is going on in our fermions systems.\
        the best way to communicate and send the message to the world is **_Visualization_**. We consider the imaginary part of the trace and then we can clearly\
        see the spectral functions:''')


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("pictures/scalarSSw2.png")

    with col2:
        st.image("pictures/BxSAw0.png")

    with col3:
        st.image("pictures/BxySSw0.png")

    with col4:
        st.image("pictures/BtuSAw0.png")

    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("pictures/ScaledBxySS1.png")

    with col2:
        st.image("pictures/ScaledBxySS2.png")
    
    with col3:
        st.image("pictures/BxyAdS4(thin).png")

    with col4:
        st.image("pictures/BxyAdS5(thin).png")
     
    url = "https://science.org/doi/10.1126/sciadv.aau0059"
    st.info(''' One of the evidences of our theoretical prediction by gravity/condensed matter is Extremely flat band in bilayer graphene:
            check out this: [doi/10.1126/sciadv.aau0059](%s)''' % url) 
    st.image(
            "https://science.org/cms/10.1126/sciadv.aau0059/asset/d226a0df-05e6-4552-ba57-cca54bf06eb3/assets/graphic/aau0059-f1.jpeg")


    st.header('Realization of Various Dimensional Gap/Semi-Metals')    

    st.markdown(''' No just only pole type Green's function, we also discover **_Branch-cut_** types Green's function which is common type Green's function\
        appearing in conformal field theory. This type of Green's function show the typical feature of strongly correlated systems. We found that this types of \
        Green's function can generate gap in various dimension (so far people accept that scalar interaction can generate the gap in holography), which fulfill the AdS/CFT correspondence dictionary.\
        The example of Green's function are given as follows''')        

    st.latex(r'''
    \begin{align*}
    \text{Tr}\mathbb{G}_{M_0}^{(SA)} &= \frac{4\omega}{\sqrt{\boldsymbol{k}^2-\omega^2+M_0^2}},\\
    \text{Tr}\mathbb{G}_{B_{t}^{(0)}}^{(SS)} &= 2\Big(\frac{b+\omega}{\sqrt{\boldsymbol{k}^2-(b+\omega)^2}}-\frac{b-\omega}{\sqrt{\boldsymbol{k}^2-(b-\omega)^2}}\Big),\\
    \text{Tr}\mathbb{G}_{B_{tu}^{(-1)}}^{(SS)} &= \frac{2\omega}{\sqrt{(b-|\boldsymbol{k}|)^2-\omega^2}}+\frac{2\omega}{\sqrt{(b+|\boldsymbol{k}|)^2-\omega^2}},\\
    \text{Tr}\mathbb{G}_{B_{x}^{(0)}}^{(SS)} &=  \frac{2\omega}{\sqrt{(b-k_x)^2+\boldsymbol{k}_\perp^2 -\omega^2}}+\frac{2\omega}{\sqrt{(b+k_x)^2+\boldsymbol{k}_\perp^2 -\omega^2}},\\
    \text{Tr}\mathbb{G}_{B_{xy}^{(-1)}}^{(SA)} &= \frac{2\omega}{\sqrt{(b-|\boldsymbol{k}|)^2+k_z^2 -\omega^2}}+\frac{2\omega}{\sqrt{(b+|\boldsymbol{k}|)^2+k_z^2 -\omega^2}}.
    \end{align*} ''')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("pictures/BxSSw0.png")

    with col2:
        st.image("pictures/BuxSAw1.png")

    with col3:
        st.image("pictures/BxySAw1.png")

    with col4:
        st.image("pictures/BtSSw1.png")

    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("pictures/ScaledBxySA1.png")

    with col2:
        st.image("pictures/ScaledBxySA2.png")
    
    with col3:
        st.image("pictures/AdS4Scalar.png")

    with col4:
        st.image("pictures/AdS4BxSSsur.png")

    st.markdown(''' The most important realizations of these types of Green's function are superconducting gap and Weyl semi-metals ''')
with tab2:
    st.markdown(''' From this setup and we have **_16_** types of interaction, 2 of scalars, 8 of vectors, and 6 of tensors, including quantization types, we have \
                32 spectral functions which contain different symmetry and features.''')
    st.image('ClassifiedTable.png', output_format="PNG")
