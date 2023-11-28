import json
import os


class Preferences:
    CONFIG_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "\\config\\"
    SESSION_CONFIG_FILE_PATH = CONFIG_FOLDER + ".session.config.json"

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
