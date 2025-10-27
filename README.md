# Installation Data Generator
A Python utility for generating realistic synthetic installation records for Brazilian addresses, simulating the lifecycle of service installations over time.

---

## Overview
This tool creates synthetic installation data based on a list of addresses (e.g., from CNEFE or a similar source).
Each address can have one or more installations throughout time, with realistic creation and deletion timestamps that follow a consistent chronological lifecycle.

It’s ideal for testing, data simulations, and temporal modeling in energy, telecom, or utilities systems.

---

## Features

* **Chronological Consistency** — createdAt and deletedAt timestamps always follow a realistic lifecycle (no overlaps or reversals)

* **Realistic Multiplicity** — most addresses have only one installation, but a small fraction represent multiple sequential or concurrent ones

* **Time Dynamics** — deletions and re-installations are separated by random gaps (0–360 days)

* **Probabilistic Distributions**

    * ~85% of addresses → 1 installation

    * ~10% → 2–3 installations

    * ~5% → 3–20 installations (e.g., multi-unit buildings)

* **Brazilian Localization** — compatible with pt_BR locale and CNEFE-like address structures

---

## Usage

### Basic Generation
```python
from pathlib import Path
from installation_generator import (
    load_addresses,
    generate_installation_records,
    save_installations_to_csv,
)

csv_path = Path("data/15_PA.csv.sample")
output_path = Path("data/installations.csv")

# Generate one installations data
addresses = load_addresses(csv_path)
installations = generate_installation_records(addresses)
save_installations_to_csv(installations, output_path)