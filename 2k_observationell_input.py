# Omvandling av astronomiska koordinater

from datetime import datetime, timezone
import numpy as np

# --- INPUTS ---


def ange_koordinater():
    print("\nAnge 'F' om i Falun, 'E' om i Eslöv")
    koordinater_str = input("Koordinater [Lat , Long]:")

    if koordinater_str == "F":
        lat = 60.6065
        long = 15.6355
    elif koordinater_str == "E":
        lat = 55.88352
        long = 13.44818
    else:
        koordinater_parts = koordinater_str.split(",")
        lat = koordinater_parts[0]
        long = koordinater_parts[1]

    print(f"Din position är [{lat}°, {long}°")
    return lat, long


def ange_tid():
    val = input("\nAnvänd nuvarande tid? (y/n): ").lower().strip()
    if val == "n":
        år = int(input("Ange år (YYYY): "))
        månad = int(input("Ange månad (MM): "))
        dag = int(input("Ange dag (DD): "))
        timme = int(input("Ange timme (UTC, 0–23): "))
        minut = int(input("Ange minut (00–59): "))
    else:
        nu = datetime.now(timezone.utc)
        år = nu.year
        månad = nu.month
        dag = nu.day
        timme = nu.hour
        minut = nu.minute

    print(f"\nTid (UTC): {år}-{månad:02d}-{dag:02d} {timme:02d}:{minut:02d}")
    return år, månad, dag, timme, minut


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


def ange_alt_azimut():
    print("Ange koordinater [Azimut, altitud] (deg.deg , deg.deg)")
    k_aa = input().split(",")
    if len(k_aa) != 2:
        raise ValueError("Fel format")
    azimut = float(k_aa[0])
    alt = float(k_aa[1])

    return azimut, alt,


def ange_j2000():
    print("Koordinater: (hh.mm.ss , deg.arcmin.arcsec)]")
    k_j2000_str = input("Ange [ra, dec]: ")
    k_j2000_str_split = k_j2000_str.split(",")
    dec_str = k_j2000_str_split[1]
    dec_parts = dec_str.split(".")
    if len(dec_parts) != 3:
        raise ValueError("RA måste vara i formatet hh.mm.ss")
    dec_deg_d = int(dec_parts[0])
    dec_arcmin = int(dec_parts[1])
    dec_arcsec = float(dec_parts[2])

    dec_deg = dec_deg_d + (dec_arcmin / 60) + (dec_arcsec / 3600)

    ra_str = k_j2000_str_split[0]
    ra_parts = ra_str.split(".")
    if len(ra_parts) != 3:
        raise ValueError("RA måste vara i formatet hh.mm.ss")
    ra_h = int(ra_parts[0])
    ra_m = int(ra_parts[1])
    ra_s = float(ra_parts[2])

    ra_deg = 15 * (ra_h + (ra_m / 60) + (ra_s / 3600))

    return ra_deg, dec_deg


def format_ra(ra_deg):
    ra_total_sec = ra_deg * 240
    h = int(ra_total_sec // 3600)
    m = int((ra_total_sec % 3600) // 60)
    s = ra_total_sec % 60
    return f"{h:02d}h {m:02d}m {s:05.2f}s"


def format_dec(dec_deg):
    sign = "+" if dec_deg >= 0 else "-"
    dec_deg_abs = abs(dec_deg)
    d = int(dec_deg_abs)
    m = int((dec_deg_abs - d) * 60)
    s = (dec_deg_abs - d - m / 60) * 3600
    return f"{sign}{d:02d}° {m:02d}′ {s:04.1f}″"


def välj_input_koordinatsystem():
    while True:
        print("För alt-Azimut, ange [a]. För J2000, ange [j].\n")
        i = input("Ange val: ").lower().strip()

        if i == "a":
            az, alt = ange_alt_azimut()
            return i, (az, alt)
        elif i == "j":
            ra, dec = ange_j2000()
            return i, (ra, dec)
        else:
            print("Felaktig input. Försök igen.\n")

# --- OMVANDLINGAR ---


def aa_to_j2000(azimut, alt, lat, lst):
    az = np.radians(azimut)
    alt = np.radians(alt)
    lat = np.radians(lat)

    dec = np.arcsin(np.sin(alt) * np.sin(lat) +
                    np.cos(alt) * np.cos(lat) * np.cos(az))

    H = np.arccos((np.sin(alt) - np.sin(lat) * np.sin(dec)) /
                  (np.cos(lat) * np.cos(dec)))
    if np.sin(az) > 0:
        H = 2 * np.pi - H

    ra = np.radians(lst) - H
    ra = ra % (2 * np.pi)

    return np.degrees(ra), np.degrees(dec)


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

# --- SPARA KOORDINATERNA ---


def spara_koordinater_j2000(ra, dec, namn):
    with open("sparade_koordinater.txt", "a") as fil:
        fil.write(f"{namn}: RA={ra:.6f}°, Dec={dec:.6f}°\n")
    print(f"Koordinater sparade som '{namn}' i filen sparade_koordinater.txt")

# --- FRÅGESTÄLLNING ---


print("\n\n--- OMVANDLING AV ASTRONOMISKA KOORDINATER ---")

print("Ange dina nuvarande koordinater:")

lat, long = ange_koordinater()
år, månad, dag, timme, minut = ange_tid()
lst = beräkna_lst(år, månad, dag, timme, minut, long)

print(f"Lokal Siderisk Tid (LST): {lst:.3f}°")

print("\nVilket system har du data för?")

val, data = välj_input_koordinatsystem()

if val == "a":
    print("\n vill du omvandla till J-2000?")
    svar = input("y/n: ")
    while True:
        if svar == "y":
            az, alt = data
            ra, dec = aa_to_j2000(az, alt, lat, lst)
            print("\nKOORDINATER I J-2000:")
            print(f"RA: {ra:.3f}°, Dec: {dec:.3f}°")

            spara = input(
                "Vill du spara koordinaterna? (y/n): ").lower().strip()
            if spara == "y":
                namn = input("Ange ett namn för koordinaterna: ")
                spara_koordinater_j2000(ra, dec, namn)
            break
        elif svar == "n":
            print("Fel svar försök igen")
        else:
            print("huh?")
elif val == "j":
    print("\n vill du omvandla till Alt-azimut?")
    svar = input("y/n: ")
    while True:
        if svar == "y":
            ra, dec = data
            az, alt = j2000_to_aa(ra, dec, lat, lst)
            print("\nKOORDINATER I Alt-azimut:")
            print(f"Azimut: {az:.2f}°, Altitud: {alt:.2f}°\n")

            spara = input(
                "Vill du spara koordinaterna? (y/n): ").lower().strip()
            if spara == "y":
                namn = input("Ange ett namn för koordinaterna: ")
                spara_koordinater_j2000(ra, dec, namn)

            break
        elif svar == "n":
            print("Fel svar försök igen")
        else:
            print("huh?")
            break
