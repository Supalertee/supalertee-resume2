import streamlit as st
import time
import numpy as np
from scipy.integrate import odeint
import streamlit as st
from streamlit.hello.utils import show_code


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

st.info(''' So, we obtain a **_differential equation_** called **_Equation of motions:_**  $\displaystyle\ddot{x} - \\frac{k}{m}x = 0$''')


plotting(OS(xSHM))

st.info(''' We are also able to modify our model by adding damping, which the **_equation of motions is given:_** $\displaystyle\ddot{x} - \
        \\frac{k}{m}x-b\dot{x} = 0$''')

plotting(OS(xdamp))

st.markdown(''' On can see that the periodic moving appears in the solution of spring system which is well known. However, this simple classical physics\
            calculation have been discovered for almost 300 years and it is still working well. So, How is this simple concept applied in modern theoretical physics?''')

st.sidebar.markdown("# Gravity/Condensed Matter Theorey Duality")

st.title('How do we study strongly correlated quantum systems via gravity?')

st.markdown(''' By following the same concept of the least action principle $\delta S = 0$, we can investigate how particle behave, that is most important \
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

