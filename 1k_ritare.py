from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
import re

# --- KONSTANTER ---
LAT_FALUN = 60.6065
LONG_FALUN = 15.6355
FILNAMN = "sparade_koordinater.txt"

# --- HJÄLPFUNKTIONER ---


def julian_date(år, månad, dag, timme=0, minut=0):
    if månad <= 2:
        år -= 1
        månad += 12
    A = int(år / 100)
    B = 2 - A + int(A / 4)
    jd_day = int(365.25 * (år + 4716)) + \
        int(30.6001 * (månad + 1)) + dag + B - 1524.5
    jd_frac = (timme + minut / 60) / 24
    return jd_day + jd_frac


def beräkna_lst(år, månad, dag, timme, minut, longitud):
    jd = julian_date(år, månad, dag, timme, minut)
    T = jd - 2451545.0
    gst = 280.46061837 + 360.98564736629 * T
    lst = gst + float(longitud)
    return lst % 360


def j2000_to_aa(ra, dec, lat, lst):
    ra = np.radians(ra)
    dec = np.radians(dec)
    lat = np.radians(lat)
    lst = np.radians(lst)

    H = (lst - ra) % (2 * np.pi)

    alt = np.arcsin(np.sin(dec) * np.sin(lat) +
                    np.cos(dec) * np.cos(lat) * np.cos(H))

    az = np.arccos((np.sin(dec) - np.sin(alt) * np.sin(lat)) /
                   (np.cos(alt) * np.cos(lat)))
    if np.sin(H) > 0:
        az = 2 * np.pi - az

    return np.degrees(az), np.degrees(alt)


def läs_koordinater_fil(filnamn):
    koordinater = []
    try:
        with open(filnamn, "r", encoding="utf-8") as fil:
            for rad in fil:
                if not rad.strip():
                    continue

                # Normalisera: ta bort BOM och “konstiga” mellanslag
                rad = rad.replace("\ufeff", "") \
                         .replace("\u00A0", " ") \
                         .replace("\u202F", " ")

                # Dela bara på första ":" för att få namn och resten
                if ":" not in rad:
                    continue
                namn, rest = rad.split(":", 1)

                hidden = "[hidden]" in rad

                # Plocka ut de första två numeriska värdena (RA, Dec)
                # Hanterar t.ex. "RA=356.051°, Dec=56.861°" oavsett extra tecken
                nums = re.findall(r"[-+]?\d+(?:[.,]\d+)?", rest)
                if len(nums) < 2:
                    print(
                        f"Varning: kunde inte tolka RA/Dec för '{namn.strip()}'; hoppar över.")
                    continue

                # Byt ev. decimal-komma till punkt och konvertera
                ra = float(nums[0].replace(",", "."))
                dec = float(nums[1].replace(",", "."))

                namn_clean = namn.strip().replace("[hidden]", "").strip()
                koordinater.append((namn_clean, ra, dec, hidden))

    except FileNotFoundError:
        print(f"Filen '{filnamn}' hittades inte. Ingen data att visa.")
    return koordinater


def plotta_himmel_j2000(koordinater):
    fig, (ax_pos, ax_neg) = plt.subplots(
        1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))
    fig.suptitle("Himlavalv: J2000 (RA/Dec)")

    # --- Positiva deklinationer ---
    ax_pos.set_title("Deklination ≥ 0°")
    ax_pos.set_theta_zero_location("N")  # RA=0° på toppen
    ax_pos.set_theta_direction(1)        # Medurs: RA ökar åt höger
    ax_pos.set_rlim(0, 90)               # r=0 vid nordpolen
    ax_pos.set_rlabel_position(135)

    # --- Negativa deklinationer ---
    ax_neg.set_title("Deklination < 0°")
    ax_neg.set_theta_zero_location("N")
    ax_neg.set_theta_direction(1)
    ax_neg.set_rlim(0, 90)
    ax_neg.set_rlabel_position(135)

    for namn, ra, dec, hidden in koordinater:
        ra_rad = np.radians(ra)
        color = "red" if dec < 0 else "blue"

        if dec >= 0:
            r = 90 - dec  # r=0 vid polen
            ax_pos.plot(ra_rad, r, "o", color=color)
            if not hidden:
                ax_pos.text(ra_rad, r, namn, fontsize=8, color=color)
        else:
            r = 90 + abs(dec)  # för att separera från polen
            ax_neg.plot(ra_rad, r, "o", color=color)
            if not hidden:
                ax_neg.text(ra_rad, r, namn, fontsize=8, color=color)

    plt.show()


def plotta_himmel_altaz(koordinater, lat, lst):
    fig, (ax_pos, ax_neg) = plt.subplots(
        1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))
    fig.suptitle("Himlavalv: Alt-Az (Azimut/Altitud)")

    ax_pos.set_title("Altitud ≥ 0°")
    ax_pos.set_theta_zero_location("N")
    ax_pos.set_theta_direction(-1)
    ax_pos.set_rlim(0, 90)
    ax_pos.set_rlabel_position(135)

    ax_neg.set_title("Altitud < 0°")
    ax_neg.set_theta_zero_location("N")
    ax_neg.set_theta_direction(-1)
    ax_neg.set_rlim(90, 180)
    ax_neg.set_rlabel_position(135)

    for namn, ra, dec, hidden in koordinater:
        az, alt = j2000_to_aa(ra, dec, lat, lst)
        az_rad = np.radians(az)

        if alt >= 0:
            alt_plot = 90 - alt
            ax_pos.plot(az_rad, alt_plot, "o")
            if not hidden:
                ax_pos.text(az_rad, alt_plot, namn, fontsize=8)
        else:
            alt_plot = abs(alt) + 90
            ax_neg.plot(az_rad, alt_plot, "o", color="red")
            if not hidden:
                ax_neg.text(az_rad, alt_plot, namn, fontsize=8, color="red")

    plt.show()

# --- HUVUDPROGRAM ---


print("\n\n--- RITA STJÄRNHIMMEL FRÅN SPARADE KOORDINATER ---\n")

nu = datetime.now(timezone.utc)
år = nu.year
månad = nu.month
dag = nu.day
timme = nu.hour
minut = nu.minute

lst = beräkna_lst(år, månad, dag, timme, minut, LONG_FALUN)
print(f"Tid: {år}-{månad:02d}-{dag:02d} {timme:02d}:{minut:02d} UTC")
print(f"Lokal Siderisk Tid (LST) i Falun: {lst:.3f}°")

koordinater = läs_koordinater_fil(FILNAMN)

if not koordinater:
    print("Inga sparade koordinater att visa.")
else:
    print("\nVilket/vilka himlavalv vill du visa?")
    print("a: Endast Alt-Az")
    print("j: Endast J2000")
    print("b: Båda")

    val = input("Ange val (a/j/b): ").lower()

    if val == "a":
        plotta_himmel_altaz(koordinater, LAT_FALUN, lst)
    elif val == "j":
        plotta_himmel_j2000(koordinater)
    elif val == "b":
        plotta_himmel_altaz(koordinater, LAT_FALUN, lst)
        plotta_himmel_j2000(koordinater)
    else:
        print("Felaktigt val, visar J2000 som standard.")
        plotta_himmel_j2000(koordinater)
