def ange_j2000_grader():
    ra_str = input("Ange RA i grader (decimaler), t.ex. 138.349: ").strip()
    dec_str = input("Ange Dec i grader (decimaler), t.ex. 40.431: ").strip()
    try:
        ra_deg = float(ra_str)
        dec_deg = float(dec_str)
    except ValueError:
        raise ValueError(
            "Felaktigt format för grader. Ange decimaler")
    return ra_deg, dec_deg


def ange_j2000_hms():
    print("Ange RA i formatet hh.mm.ss:")
    ra_str = input("RA: ").strip()
    ra_parts = ra_str.split(".")
    if len(ra_parts) != 3:
        raise ValueError("RA måste vara i formatet hh.mm.ss")
    ra_h = int(ra_parts[0])
    ra_m = int(ra_parts[1])
    ra_s = float(ra_parts[2])
    ra_deg = 15 * (ra_h + ra_m / 60 + ra_s / 3600)

    print("Ange Dec i formatet dd.mm.ss:")
    dec_str = input("Dec: ").strip()
    dec_parts = dec_str.split(".")
    if len(dec_parts) != 3:
        raise ValueError("Dec måste vara i formatet dd.mm.ss")
    dec_d = int(dec_parts[0])
    dec_m = int(dec_parts[1])
    dec_s = float(dec_parts[2])
    dec_deg = dec_d + dec_m / 60 + dec_s / 3600

    return ra_deg, dec_deg


def spara_koordinater_j2000(ra_deg, dec_deg, namn):
    with open("sparade_koordinater.txt", "a", encoding="utf-8") as fil:
        fil.write(f"{namn}: RA={ra_deg:.6f}°, Dec={dec_deg:.6f}°\n")
    print(
        f"\nKoordinater sparade som '{namn}' i grader (decimaler) i filen.\n")


# --- KÖRNING ---

print("\n--- SPARA KOORDINATER MANUELLT ---\n")
namn = input("Namnge objektet: ").strip()

format_val = input(
    "Vill du mata in koordinater i grader (g) eller timmar/minuter/sekunder (h)? ").strip().lower()

try:
    if format_val == "g":
        ra_deg, dec_deg = ange_j2000_grader()
    elif format_val == "h":
        ra_deg, dec_deg = ange_j2000_hms()
    else:
        raise ValueError("Ogiltigt val för formatet.")
    spara_koordinater_j2000(ra_deg, dec_deg, namn)
except ValueError as e:
    print(f"\nFel: {e}")
