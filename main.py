#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os


def check_ssh_logins():
    # Ścieżka do systemowego pliku logów, gdzie SSH zapisuje próby dostępu
    log_path = "/var/log/auth.log"

    # Inicjalizacja liczników dla udanych i nieudanych logowań
    successful_logins = 0
    failed_logins = 0

    # Sprawdzenie, czy plik logów istnieje na dysku
    if not os.path.exists(log_path):
        # Zwracamy status UNKNOWN (3) jeśli brakuje źródła danych
        print("3 SSH_Login_Monitor - UNKNOWN: Log file not found")
        return

    # Otwarcie pliku w trybie bezpiecznym (automatyczne zamknięcie po odczycie)
    try:
        with open(log_path, "r") as file:
            for line in file:
                # Wyszukiwanie frazy świadczącej o poprawnym zalogowaniu
                if "Accepted password" in line:
                    successful_logins += 1
                # Wyszukiwanie frazy świadczącej o błędnym haśle
                elif "Failed password" in line:
                    failed_logins += 1
    except PermissionError:
        # Status UNKNOWN (3) jeśli wtyczka nie ma uprawnień administratora
        print("3 SSH_Login_Monitor - UNKNOWN: Permission denied reading auth.log")
        return

    # Domyślnie ustawiamy status OK (0)
    status_code = 0
    status_message = "OK"

    # Progi alarmowe: więcej niż 10 błędów to CRITICAL (2), cokolwiek poniżej to WARNING (1)
    if failed_logins > 10:
        status_code = 2
        status_message = "CRITICAL - Security alert: many failed logins!"
    elif failed_logins > 0:
        status_code = 1
        status_message = "WARNING - Failed login attempts detected"

    # Przygotowanie metryk (Performance Data), które CheckMK użyje do rysowania wykresów
    performance_data = f"success={successful_logins}|failed={failed_logins}"

    # Finalny komunikat wysyłany do agenta CheckMK
    # Format: <status> <nazwa_uslugi> <metryki> <tekst_dla_uzytkownika>
    print(
        f"{status_code} SSH_Login_Monitor {performance_data} {status_message}: Successful={successful_logins}, Failed={failed_logins}")


# Punkt wejścia programu
if __name__ == "__main__":
    check_ssh_logins()
