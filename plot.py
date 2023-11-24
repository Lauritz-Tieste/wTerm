class PlotEvaluator:
    def evaluate_plot(self, data):
        print(data)

        evaluation_dict = {
            "Text": self.plot_text,
            "Result": self.plot_result,
            "XT-Plot": self.plot_xt_graph,
            "Bode-Plot": self.plot_bode,
        }

        for condition, func in evaluation_dict.items():
            if condition.encode() in data:
                func()

    @staticmethod
    def plot_text():
        print("Plot Text")  # TODO: Implement

    @staticmethod
    def plot_result():
        print("Plot Result")  # TODO: Implement

    @staticmethod
    def plot_xt_graph():
        print("Plot XT Graph")  # TODO: Implement

    @staticmethod
    def plot_bode():
        print("Plot Bode")  # TODO: Implement
