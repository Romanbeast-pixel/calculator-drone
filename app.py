import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

# --- Page setup ---
icon_path = Path(__file__).parent / "drone_icon.png"
drone_img_path = Path(__file__).parent / "drone.png"   # <-- realistic drone image

st.set_page_config(
    page_title="Drone Design Calculator",
    page_icon=str(icon_path),
    layout="wide"
)

# --- Calculator ---
def quadcopter_calculator(prop_diameter_inch, drone_weight_g, thrust_per_motor_g):
    prop_size_mm = prop_diameter_inch * 25.4
    arm_length_mm = (prop_size_mm * 1.1) / 2
    diag_frame_size = arm_length_mm * 2
    center_plate = arm_length_mm * 0.72
    total_diag = diag_frame_size + center_plate

    rotor_count = 4
    total_thrust = thrust_per_motor_g * rotor_count
    twr = total_thrust / drone_weight_g if drone_weight_g > 0 else 0

    return {
        "Propeller Diameter (mm)": f"{round(prop_size_mm):,}",
        "Arm Length (mm)": f"{round(arm_length_mm):,}",
        "Diagonal Frame (mm)": f"{round(diag_frame_size):,}",
        "Center Plate (mm)": f"{round(center_plate):,}",
        "Total Diagonal (mm)": f"{round(total_diag):,}",
        "Total Thrust (g)": f"{round(total_thrust):,}",
        "Thrust-to-Weight Ratio": f"{round(twr):,}"
    }

# --- UI ---
st.title("Drone Design Calculator")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔧 Inputs")
    prop_diameter = st.number_input("Propeller Diameter (inches)", min_value=1.0, value=10.0)
    drone_weight = st.number_input("Drone Weight (g)", min_value=100, value=1500)
    thrust_per_motor = st.number_input("Thrust per Motor (g)", min_value=100, value=1000)
    calculate = st.button("🚀 Calculate")

with col2:
    st.subheader("📊 Results")
    if calculate:
        results = quadcopter_calculator(prop_diameter, drone_weight, thrust_per_motor)
        df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
        st.table(df)

        # --- Drone Image with Annotations ---
        img = mpimg.imread(drone_img_path)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.imshow(img)
        ax.axis("off")

        # Example annotations (coordinates need adjusting for your drone.png)
        ax.annotate(f"Prop Dia: {results['Propeller Diameter (mm)']}",
                    xy=(450,120), xytext=(550,120),
                    arrowprops=dict(facecolor="red", arrowstyle="->"),
                    fontsize=10, color="red")

        ax.annotate(f"Arm Len: {results['Arm Length (mm)']}",
                    xy=(250,250), xytext=(50,250),
                    arrowprops=dict(facecolor="blue", arrowstyle="->"),
                    fontsize=10, color="blue")

        ax.annotate(f"Diag: {results['Diagonal Frame (mm)']}",
                    xy=(450,450), xytext=(500,500),
                    arrowprops=dict(facecolor="green", arrowstyle="->"),
                    fontsize=10, color="green")

        ax.annotate(f"TWR: {results['Thrust-to-Weight Ratio']}",
                    xy=(250,250), xytext=(350,350),
                    arrowprops=dict(facecolor="orange", arrowstyle="->"),
                    fontsize=10, color="orange")

        ax.annotate(f"Thrust: {results['Total Thrust (g)']}",
                    xy=(120,450), xytext=(50,500),
                    arrowprops=dict(facecolor="purple", arrowstyle="->"),
                    fontsize=10, color="purple")

        st.pyplot(fig)

    else:
        st.info("Enter your inputs and click **Calculate** to see results.")

st.markdown("---")
st.caption("⚡ Built with Streamlit")
