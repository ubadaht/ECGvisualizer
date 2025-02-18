
```markdown
# ECG Data Visualization

This is a basic interactive tool to visualize and analyze ECG (electrocardiogram) data using Streamlit and Plotly. The app allows users to upload ECG data in `.mat` file format, apply filters, visualize the time-domain and frequency-domain representations of the ECG signal, and view basic signal statistics.

## Features

- Upload ECG data in `.mat` format.
- Apply various signal filters (lowpass, highpass, bandpass).
- Visualize ECG signal in the time domain.
- Visualize the frequency spectrum of the ECG signal (using DFT).
- Display signal statistics (mean, standard deviation, min, max, range).
- Customize plot appearance (line color, width, grid visibility).

## Requirements

- Python 3.7 or higher
- Streamlit
- Plotly
- NumPy
- SciPy

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ubadaht/ECGvisualizer.git
cd ECG-Data-Visualization
```

### 2. Install dependencies

It’s recommended to use a virtual environment for your project. You can set up a virtual environment and install the dependencies as follows:

```bash
python -m venv env
source env/bin/activate  # For Windows, use `env\Scripts\activate`
pip install -r requirements.txt
```

Alternatively, you can install the necessary packages manually:

```bash
pip install streamlit plotly numpy scipy
```

### 3. Run the app

After the dependencies are installed, you can run the app with the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server, and you can access the app in your web browser at `http://localhost:8501`.

## Usage

1. **Upload ECG Data**: Click on the file uploader in the sidebar and select a `.mat` file containing ECG data.
2. **Signal Processing**: Choose the filter type (lowpass, highpass, or bandpass) and set the cutoff frequency to process the ECG signal.
3. **Visualization**: The app will display:
   - A time-domain plot of the ECG signal.
   - A frequency-domain plot (DFT) of the ECG signal.
4. **Plot Customization**: Customize the plot appearance (line color, width, grid visibility) through the sidebar options.
5. **Signal Statistics**: View basic statistics such as mean, standard deviation, min, max, and range of the ECG signal.

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, please create an issue or submit a pull request.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for building interactive web apps with Python.
- [Plotly](https://plotly.com/python/) for interactive data visualizations.
- [NumPy](https://numpy.org/) and [SciPy](https://www.scipy.org/) for numerical computing and signal processing.
