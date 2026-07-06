import streamlit as st
import numpy as np
import plotly.graph_objects as go

from subtract import subtract_C

# Configure Streamlit page
st.set_page_config(
    page_title="Substract Reference from Sample",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Upload files ---
st.markdown("#### Upload Files")

st.title("Interactive Reference Subtraction")

# Add CSS to style tab labels and reduce content font size
st.markdown("""
    <style>
        button[data-baseweb="tab"] {
            font-size: 16px !important;
            padding: 12px 24px !important;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 16px;
        }
        /* Reduce font size in tab content */
        .stTabs [role="tabpanel"] {
            font-size: 13px;
        }
        /* Reduce markdown and other text */
        [role="tabpanel"] p {
            font-size: 13px !important;
        }
        /* Reduce heading sizes */
        [role="tabpanel"] h2 {
            font-size: 18px !important;
            margin-top: 1rem !important;
            margin-bottom: 0.5rem !important;
        }
        [role="tabpanel"] h3 {
            font-size: 15px !important;
            margin-top: 0.8rem !important;
            margin-bottom: 0.4rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Add stop button in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🛑 Stop App", type="secondary"):
    st.success("👋 Thanks for using clever_substraction! Session ended.")
    st.stop()

col_sample, col_ref = st.columns(2)
with col_sample:
    sample_file = st.file_uploader(
        "Sample data file",
        type=None,
        key="sample_image",
    )

    tth_s, I_s = np.loadtxt(sample_file, unpack=True) if sample_file is not None else (None, None)

with col_ref:
    ref_file = st.file_uploader(
        "Reference data file",
        type=None,
        key="ref_image",
    )

    tth_ref, I_ref = np.loadtxt(ref_file, unpack=True) if ref_file is not None else (None, None)

percentile_value = st.slider(
    "Percentile de soustraction",
    min_value=0,
    max_value=100,
    value=5,
    step=1,
)

if sample_file is not None and ref_file is not None:
    tth, I = subtract_C(sample_file, ref_file, percentile=percentile_value, plot=False, save_output=False)
else:
    tth, I = None, None

# create a Plotly figure
fig = go.Figure()
# add the data to the figure
if tth_s is not None and I_s is not None:
    fig.add_trace(go.Scatter(x=tth_s, y=I_s, mode='lines', name='Sample Data'))
if tth_ref is not None and I_ref is not None:
    fig.add_trace(go.Scatter(x=tth_ref, y=I_ref, mode='lines', name='Reference Data'))
if tth is not None and I is not None:
    fig.add_trace(go.Scatter(x=tth, y=I, mode='lines', name='Subtracted Data'))

# update the layout of the figure
fig.update_layout(
    title="Sample / Reference / Subtracted",
    xaxis_title="2theta",
    yaxis_title="Intensity",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

if sample_file is None or ref_file is None:
    st.info("Upload both files to run subtraction.")


# add button to download the subtracted data
# add field to specify output filename

output_filename = st.text_input("Output Filename", value="subtracted_data.xy")


if tth is not None and I is not None:
    output_data = np.column_stack((tth, I))
    np.savetxt(output_filename, output_data)

    with open(output_filename, "rb") as f:
        st.download_button(
            label="Download Subtracted Data",
            data=f,
            file_name=output_filename,
            mime="text/plain",
        )