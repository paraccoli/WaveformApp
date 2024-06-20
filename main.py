import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class RealTimeWaveformPlotter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("リアルタイム波形表示")
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.plot_widget = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.plot_widget)

        self.combined_plot = self.plot_widget.addPlot(row=0, col=0, colspan=2, title="Combined Waveforms")
        self.combined_plot.addLegend()

        self.individual_plots = []
        for i in range(3):
            plot = self.plot_widget.addPlot(row=1, col=i, title=f"Waveform {i+1}")
            self.individual_plots.append(plot)

        self.start_stop_button = QtWidgets.QPushButton("Start")
        self.start_stop_button.clicked.connect(self.start_stop)
        self.layout.addWidget(self.start_stop_button)

        self.sample_rate_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sample_rate_slider.setRange(1, 100)
        self.sample_rate_slider.setValue(50)
        self.sample_rate_slider.valueChanged.connect(self.update_sample_rate)
        self.layout.addWidget(self.sample_rate_slider)

        self.combined_curves = []
        self.individual_curves = [[] for _ in range(3)]
        self.data = []
        self.colors = ['r', 'g', 'b']
        self.labels = ['Wave 1', 'Wave 2', 'Wave 3']
        for i in range(3):
            data = np.zeros(100)
            self.data.append(data)
            curve = self.combined_plot.plot(data, pen=self.colors[i], name=self.labels[i])
            self.combined_curves.append(curve)
            individual_curve = self.individual_plots[i].plot(data, pen=self.colors[i])
            self.individual_curves[i].append(individual_curve)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        else:
            self.timer.start()
            self.start_stop_button.setText("Stop")

    def update_sample_rate(self, value):
        self.timer.setInterval(value)

    def update_plot(self):
        for i in range(len(self.combined_curves)):
            data = self.data[i]
            data[:-1] = data[1:]
            data[-1] = np.random.normal()
            self.combined_curves[i].setData(data)
            self.individual_curves[i][0].setData(data)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    plotter = RealTimeWaveformPlotter()
    plotter.show()
    app.exec_()
