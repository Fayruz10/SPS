import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QSlider,
    QComboBox, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt

class SensorSignalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphic Visualization of Sensor Signals")
        self.setGeometry(100, 100, 1000, 800)

        # Layout setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Sensor selection
        self.sensor_label = QLabel("Select Sensor")
        self.layout.addWidget(self.sensor_label)
        self.sensor_selector = QComboBox()
        self.sensor_selector.addItems([
            "TTP223 Capacitive Touch",
            "Kamera RGB-D",
            "Myoware Muscle",
            "MTS Temposonics",
            "Parallax Ping"
        ])
        self.layout.addWidget(self.sensor_selector)

        # Noise controls
        self.noise_amplitude_label = QLabel("Noise Amplitude: 3.0")
        self.layout.addWidget(self.noise_amplitude_label)
        self.noise_amplitude_slider = QSlider(Qt.Horizontal)
        self.noise_amplitude_slider.setMinimum(1)
        self.noise_amplitude_slider.setMaximum(100)
        self.noise_amplitude_slider.setValue(30)
        self.noise_amplitude_slider.valueChanged.connect(self.update_noise_amplitude_label)
        self.layout.addWidget(self.noise_amplitude_slider)

        self.noise_frequency_label = QLabel("Noise Frequency (Hz): 5")
        self.layout.addWidget(self.noise_frequency_label)
        self.noise_frequency_slider = QSlider(Qt.Horizontal)
        self.noise_frequency_slider.setMinimum(1)
        self.noise_frequency_slider.setMaximum(50)
        self.noise_frequency_slider.setValue(5)
        self.noise_frequency_slider.valueChanged.connect(self.update_noise_frequency_label)
        self.layout.addWidget(self.noise_frequency_slider)

        # Signal operations
        self.signal_operations_label = QLabel("Signal Operations")
        self.layout.addWidget(self.signal_operations_label)
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_signals)
        self.button_layout.addWidget(self.add_button)

        self.multiply_button = QPushButton("Multiply")
        self.multiply_button.clicked.connect(self.multiply_signals)
        self.button_layout.addWidget(self.multiply_button)

        self.convolve_button = QPushButton("Convolve")
        self.convolve_button.clicked.connect(self.convolve_signals)
        self.button_layout.addWidget(self.convolve_button)

        self.dft_button = QPushButton("Calculate DFT")
        self.dft_button.clicked.connect(self.calculate_dft)
        self.button_layout.addWidget(self.dft_button)

        self.layout.addLayout(self.button_layout)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_signals)
        self.layout.addWidget(self.reset_button)

        # Initialize signals
        self.time = np.linspace(0, 2, 1000)
        self.sound_signal = np.sin(2 * np.pi * 10 * self.time)

        # Initialize result_signal before calling update_noise_signal
        self.result_signal = self.sound_signal

        # Plot setup
        self.figure, self.axs = plt.subplots(2, 2, figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Initialize noise signal and plot
        self.update_noise_signal()
        self.plot_signals()

    def update_noise_amplitude_label(self):
        self.noise_amplitude = self.noise_amplitude_slider.value() / 10
        self.noise_amplitude_label.setText(f"Noise Amplitude: {self.noise_amplitude:.1f}")
        self.update_noise_signal()

    def update_noise_frequency_label(self):
        self.noise_frequency = self.noise_frequency_slider.value()
        self.noise_frequency_label.setText(f"Noise Frequency (Hz): {self.noise_frequency}")
        self.update_noise_signal()

    def update_noise_signal(self):
        self.noise_amplitude = self.noise_amplitude_slider.value() / 10
        self.noise_frequency = self.noise_frequency_slider.value()
        self.noise_signal = self.noise_amplitude * np.sin(2 * np.pi * self.noise_frequency * self.time)
        self.plot_signals()

    def plot_signals(self):
        self.axs[0, 0].cla()
        self.axs[0, 0].plot(self.time, self.sound_signal, color='red')
        self.axs[0, 0].set_title("Original Signal")
        self.axs[0, 0].set_xlabel("Time [s]")
        self.axs[0, 0].set_ylabel("Amplitude [V]")

        self.axs[0, 1].cla()
        self.axs[0, 1].plot(self.time, self.noise_signal, color='black')
        self.axs[0, 1].set_title("Noise Signal")
        self.axs[0, 1].set_xlabel("Time [s]")
        self.axs[0, 1].set_ylabel("Amplitude [V]")

        self.axs[1, 0].cla()
        self.axs[1, 0].plot(self.time, self.result_signal, color='blue')
        self.axs[1, 0].set_title("Result of Operation")
        self.axs[1, 0].set_xlabel("Time [s]")
        self.axs[1, 0].set_ylabel("Amplitude [V]")

        self.axs[1, 1].cla()
        self.axs[1, 1].magnitude_spectrum(self.result_signal, Fs=1/(self.time[1]-self.time[0]), color='yellow')
        self.axs[1, 1].set_title("DFT Result")
        self.axs[1, 1].set_xlabel("Frequency [Hz]")
        self.axs[1, 1].set_ylabel("Amplitude")

        self.figure.tight_layout()
        self.canvas.draw()

    def add_signals(self):
        self.result_signal = self.sound_signal + self.noise_signal
        self.plot_signals()

    def multiply_signals(self):
        self.result_signal = self.sound_signal * self.noise_signal
        self.plot_signals()

    def convolve_signals(self):
        self.result_signal = np.convolve(self.sound_signal, self.noise_signal, mode='same')
        self.plot_signals()

    def calculate_dft(self):
        self.result_signal = np.abs(np.fft.fft(self.result_signal))
        self.plot_signals()

    def reset_signals(self):
        self.result_signal = self.sound_signal
        self.plot_signals()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SensorSignalApp()
    window.show()
    sys.exit(app.exec_())
