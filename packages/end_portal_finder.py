import math


def find_stronghold():
  print("=== KALKULATOR STRONGHOLDA MINECRAFT ===")
  print(
      "Podaj dane z dwóch różnych rzutów (współrzędne X, Z oraz kąt yaw z"
      " F3).\n"
  )

  # Pobieranie danych pierwszego rzutu
  print("--- Rzut 1 ---")
  x1 = float(input("Podaj X gracza 1: "))
  z1 = float(input("Podaj Z gracza 1: "))
  yaw1 = float(input("Podaj kąt yaw 1 (z ekranu F3): "))

  # Pobieranie danych drugiego rzutu
  print("\n--- Rzut 2 ---")
  x2 = float(input("Podaj X gracza 2: "))
  z2 = float(input("Podaj Z gracza 2: "))
  yaw2 = float(input("Podaj kąt yaw 2 (z ekranu F3): "))

  # Konwersja kątów yaw na radiany i wektory kierunkowe w Minecrafcie
  rad1 = math.radians(yaw1)
  rad2 = math.radians(yaw2)

  dx1 = -math.sin(rad1)
  dz1 = math.cos(rad1)

  dx2 = -math.sin(rad2)
  dz2 = math.cos(rad2)

  # Wyznacznik układu równań (metoda Cramera)
  D = dz1 * dx2 - dx1 * dz2

  if abs(D) < 1e-6:
    print(
        "\nBłąd: Rzuty są równoległe lub zrobione z tego samego miejsca!"
        " Zrób rzuty bardziej prostopadle do siebie."
    )
    return

  # Obliczanie współczynnika t dla pierwszej prostej
  t = (dx2 * (z2 - z1) - dz2 * (x2 - x1)) / D

  # Wyznaczenie współrzędnych twierdzy
  stronghold_x = x1 + t * dx1
  stronghold_z = z1 + t * dz1

  print("\n----------------------------------------")
  print(f"Szacowane współrzędne Strongholda:")
  print(f"X = {round(stronghold_x)}")
  print(f"Z = {round(stronghold_z)}")
  print("----------------------------------------")


if __name__ == "__main__":
  find_stronghold()
