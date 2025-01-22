from .datacollector import DataCollector
import matplotlib.pyplot as plt
import numpy as np

class GraphicGenerator:
    """
    A graphic render to plot data
    """
    def __init__(self) -> None:
        self.dataCollectors: tuple[DataCollector]

    def add_on_plot(
        self, plot_label: str,
        color: str, 
        x_column: tuple[float, float], 
        y_column_name: str, 
        y_standard_deviation: bool, 
        dc: tuple[DataCollector], 
        default_diff: DataCollector | None = None) -> None:
        """
        Will add data on plot selected

        Args:
            plot_label (required): Name of plot
            color: Color of the plot
            x_column (required): Tuple with initial value of x, step
            y_column_name (required): Name of y column on DataCollector
            dataCollectors (required): Is a tuple with all DataCollector to be analyzed
            y_standard_deviation (optional): If True, the standard deviation will be used
            dc (required): Tuple with all DataCollectors
            default_diff (optional): Pass the network without black holes to compare, if None don't affect the result
        """
        y_points = []
        if dc:
            self.dataCollectors = dc

        temp_error_bar: list = []

        default_arithmetic_mean = 0 if default_diff == None else default_diff.arithmetic_Mean(y_column_name)[y_column_name]
        for dataCollector in self.dataCollectors:
            arithmetic_mean = dataCollector.arithmetic_Mean(y_column_name)[y_column_name]
            y_points.append(default_arithmetic_mean - arithmetic_mean)

            dataCollector.standard_Deviation(y_column_name)
            
            if y_standard_deviation:
                temp_error_bar.append(dataCollector.standard_deviations[y_column_name])

        x_points = []
        temp_x = x_column[0]
        for i in range(0, len(y_points)):
            x_points.append(temp_x)
            temp_x += x_column[1]

        x_points = np.array(x_points)
        y_points = np.array(y_points)

        plt.plot(x_points, y_points, label=plot_label, color=color, marker='.')

        if y_standard_deviation:
            error_bar: np.ndarray = np.array(temp_error_bar)
            plt.errorbar(x_points, y_points, yerr=error_bar, fmt='.', color=color)

    def show_plot(self, title: str, x_label: str, y_label: str, pdf_file: str = '', grid: bool = True) -> None:
        """
        Will show especific plot selected

        Args:
            title (required): Title of plot, if None will don't have title
            x_label (required): Label of x axis
            y_label (required): Label of y axis
            pdf_file (optional): Name of pdf file, if don't want save as pdf, pdf_file = ""
            grid (optional): Add a grid on the plot if is True
        """
        if title != None:
            plt.title(title)

        plt.legend()
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        if grid:
            plt.grid(True, linestyle='--', color='gray', alpha=0.5)

        if pdf_file != '':
            plt.savefig(fname=pdf_file, format='pdf', bbox_inches="tight", pad_inches=0.1)

        plt.show()