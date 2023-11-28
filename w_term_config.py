BUTTON_CONFIG = [
    ("Connect", "#f97316", "on_connect_serial_button_clicked", "connect_button"),
    ("Edit Connection", "#f97316", "on_connection_edit_button_clicked", "connection_edit_button"),
    ("Load Plot", "#22c55e", "load_plot_clicked", "load_plot_button"),
    ("Save Terminal", "#0ea5e9", "save_terminal_clicked", "save_terminal_button"),
    ("Clear", "#64748b", "clear_clicked", "clear_terminal_button"),
]

CONNECT_BUTTON_CONFIG = [
    ("Connect", "#22c55e"),
    ("Disconnect", "#ef4444"),
]

CONNECTION_EDIT_WINDOW_SAVE_BUTTON = ("Save Connection", "#22c55e")

COMMAND_CONFIG = [("List", "#0f172a", "send_command_clicked", "list"),
                  ("PWM", "#0f172a", "send_command_clicked",
                   '"SpgParkClarke;rec reset;rec title SpgParkClarke;rec 0 10 0.25 0.1;ch fUd 1;ch fUq 1;ch fSinPhi '
                   '2;ch fCosPhi 2;ch fUa 3;ch fUb 3;ch fU1 4;ch fU2 4;ch fU3 4;ch fM1 5;ch fM2 5;ch fM3 5;ch fMean '
                   '5;ch fPwm1 6;ch fPwm2 6;ch fPwm3 6;ch iCcr1 7;ch iCcr2 7;ch iCcr3 7;limits 1 0 0 [V];limits 2 0 0 '
                   '[+-1];limits 3 0 0 [V];limits 4 0 0 [V];limits 5 0 0 [+-0.5];limits 6 0 0 [0..1];limits 7 0 0 ['
                   '0..PWMMAX];s;'),
                  ("Send", "#0f172a", "send_command_clicked", ""),
                  ("Send", "#0f172a", "send_command_clicked", ""),
                  ("Send", "#0f172a", "send_command_clicked", ""),
                  ("Send", "#0f172a", "send_command_clicked", "")]

BAUD_RATES = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400,
              460800, 500000, 576000, 921600, 1000000]

BIT_RATE = [{"title": "5", "variable": 5}, {"title": "6", "variable": 6},
            {"title": "7", "variable": 7}, {"title": "8", "variable": 8}, ]

PARITY = [{"title": "None", "variable": "N"}, {"title": "Even", "variable": "E"},
          {"title": "Odd", "variable": "O"}, {"title": "Mark", "variable": "M"},
          {"title": "Space", "variable": "S"}]

STOP_BITS = [{"title": "1", "variable": 1}, {"title": "1.5", "variable": 1.5},
             {"title": "2", "variable": 2}]
