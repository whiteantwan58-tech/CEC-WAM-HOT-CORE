# Add this inside psi_panel function, after the bonding curve chart
st.markdown("### Combined HEI Core Formula")
st.latex(r"I_a = \lim_{t \to \infty} \left[ \int (S \cdot T) \, d\Phi \cdot (\Psi \cdot G) \right]")

# Live calculation (conceptual)
psi_value = 1.61803  # placeholder from your formulas
g_constant = 6.67430e-11
core_value = psi_value * g_constant * 1.61803  # simplified demo

st.metric("Core HEI Convergence Value", f"{core_value:.8f}", "Optimized")