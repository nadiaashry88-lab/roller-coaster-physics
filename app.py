
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Roller Coaster Physics", layout="wide")

st.title("🎢 Roller Coaster Physics Simulator")
st.write("Grade 12 Physics Project | Mechanics, Energy and Forces")
st.info("Ideal model: friction and air resistance are ignored.")

st.sidebar.header("Simulation Settings")
mass = st.sidebar.slider("Coaster mass (kg)", 100, 2000, 500, 50)
height = st.sidebar.slider("Starting height (m)", 5, 60, 30)
initial_speed = st.sidebar.slider("Initial speed (m/s)", 0.0, 15.0, 0.0, 0.5)
radius = st.sidebar.slider("Circular dip radius (m)", 5, 30, 10)

g = 9.81
heights = np.linspace(height, 0, 30)

# 1. Conservation of mechanical energy
speed = np.sqrt(initial_speed**2 + 2*g*(height-heights))

# 2. Gravitational potential energy
pe = mass * g * heights

# 3. Kinetic energy
ke = 0.5 * mass * speed**2
total_energy = pe + ke

# 4. Centripetal acceleration
ac = speed**2 / radius

# Bottom of circular dip
bottom_speed = np.sqrt(initial_speed**2 + 2*g*height)
bottom_ac = bottom_speed**2 / radius

# 5. Newton's second law: net radial force = mass * acceleration
net_radial_force = mass * bottom_ac

# 6. Normal force at the bottom: N = m(g + v^2/r)
normal_force = mass * (g + bottom_ac)

# 7. Apparent load factor
load_factor = normal_force / (mass * g)

st.header("Key Results")
c1, c2, c3 = st.columns(3)
c1.metric("Bottom speed", f"{bottom_speed:.2f} m/s")
c2.metric("Speed", f"{bottom_speed*3.6:.2f} km/h")
c3.metric("Centripetal acceleration", f"{bottom_ac:.2f} m/s²")

c4, c5, c6 = st.columns(3)
c4.metric("Net radial force", f"{net_radial_force:,.0f} N")
c5.metric("Normal force", f"{normal_force:,.0f} N")
c6.metric("Load factor", f"{load_factor:.2f} g")

st.header("Simulation Results Table")
results = pd.DataFrame({
    "Height (m)": heights,
    "Speed (m/s)": speed,
    "Speed (km/h)": speed * 3.6,
    "Potential Energy (J)": pe,
    "Kinetic Energy (J)": ke,
    "Total Energy (J)": total_energy,
    "Centripetal Acceleration (m/s²)": ac
})
st.dataframe(results.round(2), use_container_width=True)

st.header("1. Speed vs Height")
fig1, ax1 = plt.subplots()
ax1.plot(heights, speed, marker="o")
ax1.set_xlabel("Height (m)")
ax1.set_ylabel("Speed (m/s)")
ax1.grid(True)
st.pyplot(fig1)
plt.close(fig1)

st.header("2. Energy Transformation")
fig2, ax2 = plt.subplots()
ax2.plot(heights, pe, label="Potential Energy")
ax2.plot(heights, ke, label="Kinetic Energy")
ax2.plot(heights, total_energy, label="Total Mechanical Energy")
ax2.set_xlabel("Height (m)")
ax2.set_ylabel("Energy (J)")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)
plt.close(fig2)

st.header("3. Speed vs Centripetal Acceleration")
fig3, ax3 = plt.subplots()
ax3.plot(speed, ac, marker="o")
ax3.set_xlabel("Speed (m/s)")
ax3.set_ylabel("Centripetal acceleration (m/s²)")
ax3.grid(True)
st.pyplot(fig3)
plt.close(fig3)

st.header("Energy Conservation Check")
initial_energy = mass*g*height + 0.5*mass*initial_speed**2
st.write(f"Initial energy: {initial_energy:,.2f} J")
st.write(f"Bottom energy: {total_energy.iloc[-1]:,.2f} J")

st.download_button(
    "Download results as CSV",
    data=results.to_csv(index=False).encode("utf-8"),
    file_name="roller_coaster_results.csv",
    mime="text/csv"
)

st.caption("Educational simulation only; not a real-ride safety assessment.")
