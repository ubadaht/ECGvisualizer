import numpy as np
from scipy import signal
from scipy.io import loadmat
import pandas as pd

def load_ecg_data(file_bytes):
    """Load ECG data from .mat file"""
    try:
        # Load the data from bytes
        import io
        mat_data = loadmat(io.BytesIO(file_bytes))

        # Extract the ECG signal (assuming it's stored in a variable named 'ECG' or similar)
        ecg_signal = None
        for key in mat_data.keys():
            if isinstance(mat_data[key], np.ndarray) and len(mat_data[key].shape) <= 2:
                ecg_signal = mat_data[key].flatten()
                break

        if ecg_signal is None:
            raise ValueError("No suitable ECG data found in the file")

        # Create time array assuming 250 Hz sampling rate (common for ECG)
        time = np.arange(len(ecg_signal)) / 250.0

        return time, ecg_signal
    except Exception as e:
        raise Exception(f"Error loading ECG data: {str(e)}")

def apply_filter(signal_data, filter_type, cutoff_freq=50, order=4):
    """Apply different types of filters to the ECG signal"""
    # Sampling frequency (assumed 250 Hz)
    fs = 250.0
    nyquist = fs / 2

    normalized_cutoff = cutoff_freq / nyquist

    if filter_type == "lowpass":
        b, a = signal.butter(order, normalized_cutoff, btype='low')
    elif filter_type == "highpass":
        b, a = signal.butter(order, normalized_cutoff, btype='high')
    elif filter_type == "bandpass":
        b, a = signal.butter(order, [0.5/nyquist, normalized_cutoff], btype='band')
    else:
        return signal_data

    return signal.filtfilt(b, a, signal_data)

def calculate_statistics(signal_data):
    """Calculate basic statistics of the ECG signal"""
    stats = {
        "Mean": np.mean(signal_data),
        "Std Dev": np.std(signal_data),
        "Min": np.min(signal_data),
        "Max": np.max(signal_data),
        "Range": np.ptp(signal_data)
    }
    return stats

def compute_dft(signal_data, fs=250.0):
    """Compute the Discrete Fourier Transform of the signal"""
    n = len(signal_data)
    frequencies = np.fft.fftfreq(n, d=1/fs)
    dft = np.fft.fft(signal_data)
    magnitude = np.abs(dft)

    # Only return positive frequencies (up to Nyquist frequency)
    positive_freq_mask = frequencies >= 0
    return frequencies[positive_freq_mask], magnitude[positive_freq_mask]