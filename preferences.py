import json


class Preferences:
    SESSION_CONFIG_FILE = "session_config.json"

    def get_session_config(self):
        try:
            with open(self.SESSION_CONFIG_FILE, "r") as config_file:
                connection_details = json.load(config_file)

            serial_device = connection_details["serial_device"]
            baud_rate = connection_details["baud_rate"]

            return {"serial_device": serial_device, "baud_rate": baud_rate}

        except FileNotFoundError:
            return None
        except Exception as e:
            print(e)
