import contextlib
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import hashlib


class PlotEvaluator:
    def __init__(self, ui):
        self.ui = ui

    def evaluate_plot(self, data):
        print(data)

        plot_data = json.loads(data)
        if "Text" in plot_data["type"]:
            pass  # TODO: Implement Text Plot
        elif "Result" in plot_data["type"]:
            pass  # TODO: Implement Result Plot
        elif "XT-Plot" in plot_data["type"]:
            self.plot_xt_graph(self, plot_data)
        elif "Bode-Plot" in plot_data["type"]:
            self.plot_bode_graph(self, plot_data)
        else:
            self.ui.append_to_console("Error: No Plot found in data")

    @staticmethod
    def plot_xt_graph(self, plot_data):
        default_length = len(plot_data["xyData"][1]) - 1

        def validate_field(key, default):
            try:
                value = plot_data[key]
                if isinstance(value, list):
                    return value
                else:
                    return [value] * default_length
            except Exception:
                return [default] * default_length

        m_names = validate_field("ySignals", "")
        m_window = validate_field("pDiagram", list(range(1, len(plot_data["xyData"][1]))) if max(
            validate_field("pDiagram", 0)) == 0 else validate_field("pDiagram", 0))
        m_scale = validate_field("xyScale", 0)
        m_offset = validate_field("xyOffset", 0)
        m_min = validate_field("pLimits", 0)[0]
        m_max = validate_field("pLimits", 0)[1]
        m_ylabel = validate_field("yLabel", "")
        m_xlabel = validate_field("xLabel", "")
        m_title = validate_field("pTitle", "")

        values = [list(i) for i in zip(*plot_data["xyData"])]

        if (len(values[0])) > 1:
            matplotlib.use('QtAgg')
            plt.figure("wTerm | XT-Plot (" + str(hashlib.md5(str(plot_data).encode()).hexdigest()) + ")")
            plt.clf()
            mplstyle.use('fast')
            plt.subplots_adjust(top=0.95, bottom=0.05, left=0.07, right=0.95, hspace=0.1)

            if m_scale[0] == 0.0:
                x_value = values[0]
            else:
                x_value = [m_scale[0] * (x - m_offset[0]) for x in values[0]]

            for i, y_value in enumerate(values[1:]):
                if m_scale[i + 1] != 0.0:
                    y_value = [m_scale[i + 1] * (x - m_offset[i + 1]) for x in values[i + 1]]
                if m_window[i] > 0:
                    ax = plt.subplot(max(m_window), 1, m_window[i])
                    if m_min[m_window[i] - 1] != m_max[m_window[i] - 1]:
                        plt.ylim(m_min[m_window[i] - 1], m_max[m_window[i] - 1])
                    if m_names[i] == "":
                        plt.plot(x_value, y_value)
                    else:
                        plt.plot(x_value, y_value, label=m_names[i])
                        plt.legend(loc='upper right', shadow=True)
                    plt.grid(True)
                    if m_ylabel[m_window[i] - 1] != "":
                        plt.ylabel(m_ylabel[m_window[i] - 1])
                    if max(m_window) != m_window[i]:
                        plt.setp(ax.get_xticklabels(), visible=False)
            plt.subplot(max(m_window), 1, max(m_window))
            if m_xlabel[0] != "":
                plt.xlabel(m_xlabel[0])
            plt.subplot(max(m_window), 1, 1)
            if m_title[0] != "":
                plt.title(m_title[0])
            plt.show(block=False)

            self.ui.append_to_console("Opened XT-Plot in another window")

            # try:
            #     if self.metering.state() == "normal": self.metering.focus()
            # except Exception:
            #     self.metering = tk.Toplevel(self)
            # self.metering.title('Window Title')
            # self.sText = tk.Text(self.metering, font=self.meteringFont, width=60, height=20, bg="ivory")
            # self.msg_text = ""
            # for i in range(len(m_names)):
            #     self.msg_text += f"{m_names[i]:<20} = {values[i + 1][0]:>12} {m_ylabel[i]:<10}\n"
            #
            # self.sText.insert(tk.END, self.msg_text)
            # self.sText.grid(row=0, column=0)

            # if (self.StartIsRunning == True):
            #     time.sleep(0.02)
            #     # self.sendData('s\n\r')

    @staticmethod
    def plot_bode_graph(self, plot_data):
        try:
            default_length = len(plot_data["xyData"][1]) - 1

            def validate_field(key, default):
                try:
                    value = plot_data[key]
                    if isinstance(value, list):
                        return value
                    else:
                        return [value] * default_length
                except Exception:
                    return [default] * default_length

            m_names = validate_field("ySignals", "")
            m_window = validate_field("pDiagram", list(range(1, len(plot_data["xyData"][1]))) if max(
                validate_field("pDiagram", 0)) == 0 else validate_field("pDiagram", 0))
            m_scale = validate_field("xyScale", 0)
            m_offset = validate_field("xyOffset", 0)
            m_min = validate_field("pLimits", 0)[0]
            m_max = validate_field("pLimits", 0)[1]
            m_ylabel = validate_field("yLabel", "")
            m_xlabel = validate_field("xLabel", "")
            m_title = validate_field("pTitle", "")

            values = [list(i) for i in zip(*plot_data["xyData"])]
            frequency = np.array(values[0])
            fgIndex = np.arange(0, int((len(values) - 1) / 2))
            ref = np.zeros([len(fgIndex), len(values[0])], dtype=complex)
            plt.figure("wTerm | Bode-Plot (" + str(hashlib.md5(str(plot_data).encode()).hexdigest()) + ")")
            plt.clf()
            with contextlib.suppress(Exception):
                for index in fgIndex:
                    ref[index] = np.array(values[2 * index + 1]) + 1j * np.array(values[2 * index + 2])
                normierung = m_window.index(0)
                if (normierung == 0):
                    norm = ref[0]
                    for index in fgIndex[1:]:
                        np.divide(ref[index], norm, out=ref[index])
            try:
                for index in fgIndex:
                    if (m_window[index] != 0):
                        ax1 = plt.subplot(2, 1, 1)
                        plt.plot(frequency, np.abs(ref[index]), label=m_names[index])
                        ax1.set_yscale("log", base=10)
                        ax1.set_xscale("log", base=10)
                        ax1.grid(visible=True, which='major', color='y', linestyle='-')
                        ax1.grid(visible=True, which='minor', color='y', linestyle='--')
                        ax1.set_ylabel("Gain")
                        plt.legend(loc='upper right', shadow=True)
                        ax2 = plt.subplot(2, 1, 2)
                        plt.plot(frequency, np.angle(ref[index], deg=True), label=m_names[index], linestyle='-')
                        ax2.set_xscale("log", base=10)
                        ax2.grid(visible=True, which='major', color='y', linestyle='-')
                        ax2.grid(visible=True, which='minor', color='y', linestyle='--')
                        ax2.set_ylabel("Phase [DEG]")
                        plt.legend(loc='upper right', shadow=True)
                        plt.show(block=False)

                        self.ui.append_to_console("Opened Bode-Plot in another window")

                        plt.subplot(2, 1, 2)
                        if (m_xlabel[0] != ""):
                            plt.xlabel(m_xlabel[0])
                        plt.subplot(2, 1, 1)
                        if (m_title[0] != ""):
                            plt.title(m_title[0])
            except Exception:
                print("BodePlot Something was wrong")

        except Exception as e:
            print(f"Bode Plot Wrong JSON Data ({e})")
