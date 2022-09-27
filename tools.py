from datetime import datetime


def log_command(command, user):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open('log.txt', 'a') as f:
        f.write(dt_string + ": " + "user " + user + " executed command " + command + "\n")