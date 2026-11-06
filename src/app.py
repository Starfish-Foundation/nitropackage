import os
import requests
import rich
from cliSupport import *
from rich import print
import platform
import getpass
from cliSupport import handle_cli
from Downloader import *
import socket

hostname = socket.gethostname()
username = getpass.getuser()

print(r""" [bright_green]
   _   __ __ _  __ ___  ___  __   _   __ _____
  / \,' // // |/ // _/ / o |/ / ,' \ / //_  _/
 / \,' // // || // _/ / _,'/ /_/ o |/ /  / /  
/_/ /_//_//_/|_//___//_/  /___/|_,'/_/  /_/   
""")
while True:
  input_type = f"[bright_green]{username}@[bright)green]{hostname} ->"
  command, args = handle_cli(input_type, "help")

  if command == "mploit":
    # Sprawdzenie, czy podano jakąkolwiek podkomendę
    if not args:
      print("[-] Błąd: Brak podkomendy. Wpisz 'mploit help', aby uzyskać pomoc.")
      continue  # Wracamy na początek pętli while True

    subcommand = args[0]

    if subcommand == "run":
      # Sprawdzenie, czy podano nazwę paczki do dodania
      if len(args) < 2:
        print("[-] Błąd: Brakuje argumentu. Użycie: mploit add <nazwa_paczki>")
        continue

      package_name = args[1]
      try:
        print(f"[*] Trwa instalowanie/ładowanie paczki: {package_name}...")
        load_and_run_package(package_name)
        print(f"[+] Sukces: Paczka '{package_name}' została załadowana.")
      except FileNotFoundError:
        print(f"[-] Błąd: Nie znaleziono pliku lub paczki '{package_name}'.")
      except Exception as e:
        print(f"[-] Błąd krytyczny podczas ładowania paczki '{package_name}': {e}")

    elif subcommand == "rm":
      # Sprawdzenie argumentów dla usuwania
      if len(args) < 2:
        print("[-] Błąd: Brakuje argumentu. Użycie: mploit rm <nazwa_paczki>")
        continue

      package_name = args[1]
      print(
          f"[*] Trwa usuwanie paczki: {package_name} (funkcja do"
          " zaimplementowania)"
      )
      # Tutaj logika usuwania...

    elif subcommand == "help":
      print("mploit - tool for installing minecraft exploits (not cheats!)")
      print("  help      -> shows this text")
      print("  run <pkg> -> install package")
      print("  rm <pkg>  -> remove package")

    else:
      print(
          f"[-] Błąd: Nieznana podkomenda '{subcommand}'. Wpisz 'mploit help'."
      )