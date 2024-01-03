import streamlit as st

st.markdown("# Physics Research Interests")

st.sidebar.markdown("# Gravity/Condensed Matter Theorey Duality")

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

st.title('How I study strongly correlated quantum systems via gravity')
st.markdown(''' What we done in a simple word is applying calculus of variations to optimize an dynamical variable called Action, \
                in physical principle everythings in the universe in classical level (non-quantum) will behave along the lowest-action path.\
                every formula in physics on high-school or college are derived by this principle  ''')


st.latex(r'''
    \begin{align}
    S_{total} &= S_\psi +S_{bdy}+S_{g,\Phi} +S_{int},\\
    S_\psi &= \int d^{5}x \sum_{j=1}^2 \sqrt{-g}~ \bar\psi^{(j)}\Big(\frac1{2} \Gamma^M({\overrightarrow{D}_M-\overleftarrow{D}_M})-m^{(j)}\Big)\psi^{(j)}, \\
    S_{g,\Phi} &= \int d^{5}x \sqrt{-g}\Big(R-2\Lambda + |D_M\Phi_I|^2-m^2_{\Phi}|\Phi|^2\Big),\\
    S_{bdy} &= \frac{i}{2} \int_{bdy} d^4x \sqrt{-h} \Big(\bar{\psi}^{(1)}\psi^{(1)}\pm \bar{\psi}^{(2)}\psi^{(2)}\Big),\\
    S_{int} &= \int d^{5}x \sqrt{-g} \Big(\bar\psi^{(1)}\Phi\cdot\Gamma \psi^{(2)}+h.c \Big)
    \end{align}
    ''')

