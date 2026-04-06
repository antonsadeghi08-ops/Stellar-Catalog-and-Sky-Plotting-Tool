# Spara koordinater för att kopiera in från inaktiva txt-filer


def ange_j2000_grader():
    rad = input("Ange txt-rad: ").strip()

    try:
        namn, rest = rad.split(":", 1)
        delar = rest.split(",")
        ra_str = delar[0].split("=")[1].replace("°", "").strip()
        dec_str = delar[1].split("=")[1].replace("°", "").strip()

        ra_deg = float(ra_str)
        dec_deg = float(dec_str)
        namn = namn.strip()

    except (ValueError, IndexError):
        raise ValueError(
            "Felaktigt format. Exempel: Pollux: RA=116.329167°, Dec=28.026111°")

    return namn, ra_deg, dec_deg


def spara_koordinater_j2000(ra_deg, dec_deg, namn):
    with open("sparade_koordinater.txt", "a", encoding="utf-8") as fil:
        fil.write(f"{namn}: RA={ra_deg:.6f}°, Dec={dec_deg:.6f}°\n")
    print(
        f"\nKoordinater sparade som '{namn}' i grader (decimaler) i filen.\n")


# --- KÖRNING ---

print("\n--- SPARA KOORDINATER MANUELLT , TXT-FORMAT ---\n")

namn, ra_deg, dec_deg = ange_j2000_grader()

print(f"{namn}: RA = {ra_deg} , Dec = {dec_deg}")

spara_koordinater_j2000(ra_deg, dec_deg, namn)
