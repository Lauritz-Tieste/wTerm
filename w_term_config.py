BUTTON_CONFIG = [
    ("Save Setup", "#ef4444", "save_setup_clicked"),
    ("Start Plot", "#22c55e", "start_plot_clicked"),
    ("Load Plot", "#22c55e", "load_plot_clicked"),
    ("Save Plot", "#22c55e", "save_plot_clicked"),
    ("Save Terminal", "#0ea5e9", "save_terminal_clicked"),
    ("Clear", "#64748b", "clear_clicked"),
    ("Help", "#64748b", "help_clicked"),
]

CONNECT_BUTTON_CONFIG = [
    ("Connect", "#22c55e"),
    ("Disconnect", "#ef4444"),
]

CONNECTION_EDIT_BUTTON = ("Edit Connection", "#22c55e")

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
