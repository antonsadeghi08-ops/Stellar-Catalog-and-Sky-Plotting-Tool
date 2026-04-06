# --- REDIGERA SPARADE KOORDINATER ---

def redigera_sparade_koordinater():
    try:
        with open("sparade_koordinater.txt", "r") as fil:
            rader = fil.readlines()
    except FileNotFoundError:
        print("Filen 'sparade_koordinater.txt' hittades inte.")
        return

    while True:
        namn_sök = input(
            "\nAnge namn på stjärna att redigera (eller tomt för att avsluta): ").strip()
        if namn_sök == "":
            break

        # Leta rad med det namnet
        index = None
        for i, rad in enumerate(rader):
            if rad.strip().startswith(namn_sök + ":"):
                index = i
                break

        if index is None:
            print(f"Stjärnan '{namn_sök}' hittades inte. Försök igen.")
            continue

        rad = rader[index].strip()
        print(f"\nNu redigerar du: {rad}")
        print("1. Ta bort")
        print("2. Byt namn")
        print("3. Göm namn vid rendering (lägg till/ta bort [hidden])")
        val = input("Välj alternativ (1/2/3): ").strip()

        if val == "1":
            rader.pop(index)
            print("Stjärnan togs bort.")

        elif val == "2":
            nytt_namn = input("Ange nytt namn: ").strip()
            delar = rad.split(":")
            if len(delar) > 1:
                koordinater = delar[1].strip()
                rader[index] = f"{nytt_namn}: {koordinater}\n"
                print("Namn ändrat.")
            else:
                print("Kunde inte byta namn, felaktigt format.")

        elif val == "3":
            if "[hidden]" in rad:
                # Ta bort [hidden]
                ny_rad = rad.replace(" [hidden]", "")
                rader[index] = ny_rad + "\n"
                print("Stjärnan visas nu vid rendering.")
            else:
                # Lägg till [hidden]
                rader[index] = rad + " [hidden]\n"
                print("Stjärnan göms vid rendering.")

        else:
            print("Ogiltigt val, ingen ändring.")

        fortsätt = input(
            "Vill du redigera fler stjärnor? (y/n): ").strip().lower()
        if fortsätt != "y":
            break

    # Skriv tillbaka filen
    with open("sparade_koordinater.txt", "w") as fil:
        fil.writelines(rader)

    print("\nRedigeringen klar!")

# Kör editorn


print("\n --- REDIGERA SPARADE KOORDINATER ---")

redigera_sparade_koordinater()
