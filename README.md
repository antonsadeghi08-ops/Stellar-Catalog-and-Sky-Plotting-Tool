# Stellar-Catalog-and-Sky-Plotting-Tool

> **Note:** This is a **hobby project** made for learning and experimentation.  
> It is **not intended for scientific accuracy or professional use**.
> The sky plotter has some problems, and im not familiar enough with Matplotlib to fix them

---

## Overview

This project is a collection of small Python scripts for working with astronomical coordinates.

It allows you to:
- Convert between **Alt-Azimuth** and **J2000 (RA/Dec)**  
- Store your own **star catalog locally**  
- Visualize stars in the sky  
- Edit and manage saved observations  

Everything is built in a simple, modular way, mainly for me to learn how to do math in python

---

## Purpose

This project was created to:
- Learn about **astronomical coordinate systems**
- Practice **Python programming**
- Experiment with **data visualization**

---

## Features

- Coordinate conversion (Alt-Az ↔ J2000)
- Save coordinates to a local file
- Edit catalog entries (rename, delete, hide)
- Multiple input formats:
  - Decimal degrees
  - HMS (hours/minutes/seconds)
  - Raw `.txt` row input
- Plot stars in:
  - J2000 (RA/Dec)
  - Alt-Azimuth (observer-based)

---

## Project Structure


>1k_ritare.py # Plotting the sky
>2k_observationell_input.py # Coordinate conversion
>3k_manuell_input.py # Manual input (degrees / HMS)
>4k_editor.py # Edit saved stars
>5k_rad_input.py # Import from text rows
>sparade_koordinater.txt # Local star catalog
>README.md


---

## Installation

Make sure you have Python 3 installed.

Install dependencies:

```bash
pip install numpy matplotlib
