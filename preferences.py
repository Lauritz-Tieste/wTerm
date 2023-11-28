import json
import os


class Preferences:
    CONFIG_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\config\\"
    SESSION_CONFIG_FILE_PATH = CONFIG_FOLDER + ".session.config.json"
    W_TERM_CONFIG_FILE_PATH = CONFIG_FOLDER + ".w_term.config.json"

    def save_session_config(self, connection_details):
        try:
            with open(self.SESSION_CONFIG_FILE_PATH, "w") as config_file:
                json.dump(connection_details, config_file)
        except FileNotFoundError:
            os.mkdir(self.CONFIG_FOLDER)
            self.save_session_config(connection_details)
        except Exception as e:
            print(e)
            return None

    def get_session_config(self):
        try:
            with open(self.SESSION_CONFIG_FILE_PATH, "r") as config_file:
                connection_details = json.load(config_file)

            serial_device = connection_details["serial_device"]
            baud_rate = connection_details["baud_rate"]

            return {"serial_device": serial_device, "baud_rate": baud_rate}

        except FileNotFoundError:
            return None
        except Exception as e:
            print(e)

    def save_w_term_config(self, w_term_config):
        try:
            with open(self.W_TERM_CONFIG_FILE_PATH, "w") as config_file:
                json.dump(w_term_config, config_file)
        except FileNotFoundError:
            os.mkdir(self.CONFIG_FOLDER)
            self.save_w_term_config(w_term_config)
        except Exception as e:
            print(e)
            return None

    def get_w_term_config(self):
        try:
            with open(self.W_TERM_CONFIG_FILE_PATH, "r") as config_file:
                w_term_config = json.load(config_file)
            return w_term_config
        except FileNotFoundError:
            return None
        except Exception as e:
            print(e)
            return None

    def get_button_config(self, button_name):
        button_box_config = self.get_w_term_config().get("button_box_buttons")
        for button_config in button_box_config:
            if button_config.get("name") == button_name:
                return button_config

    def get_button_state_config(self, button_name, state):
        button_config = self.get_button_config(button_name)
        for button_state_config in button_config.get("states"):
            if button_state_config.get("state_name") == state:
                print("button_name: " + button_name + ", state: " + state + ", button_state_config: " + str(
                    button_state_config))

                return button_state_config
