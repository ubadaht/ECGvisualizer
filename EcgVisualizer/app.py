import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils import load_ecg_data, apply_filter, calculate_statistics, compute_dft

# Page configuration
st.set_page_config(
    page_title="ECG Data Visualization",
    page_icon="❤️",
    layout="wide"
)

# Title and description
st.title("Interactive ECG Data Visualization")
st.markdown("""
This tool allows you to visualize and analyze ECG data. Upload your .mat file to get started.
""")

# Sidebar controls
st.sidebar.header("Controls")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload ECG Data (.mat file)", type=["mat"])

if uploaded_file is not None:
    try:
        # Load the data
        time, ecg_signal = load_ecg_data(uploaded_file.read())

        # Filtering options
        st.sidebar.subheader("Signal Processing")
        filter_type = st.sidebar.selectbox(
            "Filter Type",
            ["none", "lowpass", "highpass", "bandpass"]
        )

        if filter_type != "none":
            cutoff_freq = st.sidebar.slider(
                "Cutoff Frequency (Hz)",
                1, 125, 50
            )
            filtered_signal = apply_filter(ecg_signal, filter_type, cutoff_freq)
        else:
            filtered_signal = ecg_signal

        # Visualization options
        st.sidebar.subheader("Visualization")
        window_size = st.sidebar.slider(
            "Time Window (seconds)",
            1, int(max(time)),
            min(10, int(max(time)))
        )

        # Plot customization
        st.sidebar.subheader("Plot Customization")
        line_color = st.sidebar.color_picker("Line Color", "#00FF00")
        line_width = st.sidebar.slider("Line Width", 1, 5, 2)
        show_grid = st.sidebar.checkbox("Show Grid", True)

        # Create time domain plot
        fig_time = go.Figure()

        fig_time.add_trace(go.Scatter(
            x=time,
            y=filtered_signal,
            mode='lines',
            name='ECG Signal',
            line=dict(color=line_color, width=line_width)
        ))

        # Update time domain layout
        fig_time.update_layout(
            title="ECG Waveform (Time Domain)",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude (mV)",
            showlegend=True,
            hovermode='x unified',
            xaxis=dict(
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='LightGrey',
                range=[0, window_size]
            ),
            yaxis=dict(
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='LightGrey'
            ),
            plot_bgcolor='white'
        )

        # Compute and plot DFT
        frequencies, magnitude = compute_dft(filtered_signal)

        # Create frequency domain plot
        fig_freq = go.Figure()

        fig_freq.add_trace(go.Scatter(
            x=frequencies,
            y=magnitude,
            mode='lines',
            name='Frequency Spectrum',
            line=dict(color=line_color, width=line_width)
        ))

        # Update frequency domain layout
        fig_freq.update_layout(
            title="ECG Frequency Spectrum",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude",
            showlegend=True,
            hovermode='x unified',
            xaxis=dict(
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='LightGrey',
                range=[0, 125]  # Display up to Nyquist frequency
            ),
            yaxis=dict(
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='LightGrey',
                type='log'  # Use log scale for better visualization
            ),
            plot_bgcolor='white'
        )

        # Display the plots one after another
        st.plotly_chart(fig_time, use_container_width=True)
        st.plotly_chart(fig_freq, use_container_width=True)

        # Signal statistics
        st.subheader("Signal Statistics")
        stats = calculate_statistics(filtered_signal)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Mean", f"{stats['Mean']:.2f}")
        with col2:
            st.metric("Std Dev", f"{stats['Std Dev']:.2f}")
        with col3:
            st.metric("Min", f"{stats['Min']:.2f}")
        with col4:
            st.metric("Max", f"{stats['Max']:.2f}")
        with col5:
            st.metric("Range", f"{stats['Range']:.2f}")

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    # Display placeholder
    st.info("Please upload a .mat file containing ECG data to begin visualization.")

    # Example plot placeholder
    t = np.linspace(0, 2*np.pi, 1000)
    y = np.sin(t)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t,
        y=y,
        mode='lines',
        name='Example Signal',
        line=dict(color="#00FF00", width=2)
    ))

    fig.update_layout(
        title="Example Waveform (Upload data to see actual ECG)",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        showlegend=False,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)