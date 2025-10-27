import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("pt_BR")


def random_past_datetime(max_years: int = 5):
    """Generate a random datetime within the last `max_years` years."""
    return fake.date_time_between(start_date=f"-{max_years}y", end_date="now")


def generate_installation_timestamps(start_time: datetime | None = None) -> tuple:
    """Generate createdAt and deletedAt timestamps.

    Args:
        start_time (datetime | None): Optional minimum creation time.
    Returns:
        (createdAt, deletedAt)
    """
    created_at = start_time or random_past_datetime(max_years=5)

    deleted_at = None
    if random.random() < 0.2:
        # offset between 20 and 1800 days (favoring longer lifespans)
        offset_days = int(random.triangular(20, 1800, 360))
        deleted_at = created_at + timedelta(days=offset_days)
        if deleted_at > datetime.now():
            deleted_at = None

    if deleted_at and deleted_at <= created_at:
        deleted_at = None

    return created_at, deleted_at


def load_addresses(csv_path: Path) -> pd.DataFrame:
    """Load address data from CSV."""
    df = pd.read_csv(csv_path)
    return df.fillna("")


def sample_installation_count() -> int:
    """Return a realistic number of installations per address.

    - ~85% of addresses: 1 installation
    - ~10% of addresses: 2 installations
    - ~1% of addresses: 3 installations
    """
    r = random.random()
    if r < 0.85:
        return 1
    elif r < 0.95:
        return random.randint(2, 3)
    else:
        return random.randint(3, 20)  # like buildings


def generate_installation_records(addresses: pd.DataFrame) -> list[dict]:
    """Generate fake installations with realistic lifecycles."""
    records = []

    for _, row in addresses.iterrows():
        n_installations = sample_installation_count()

        # Start the lifecycle somewhere in the past few years
        current_time = random_past_datetime(max_years=5)

        for _ in range(n_installations):
            created_at, deleted_at = generate_installation_timestamps(current_time)

            record = {
                "addressId": (
                    int(row["ID_ENDERECO"])
                    if str(row["ID_ENDERECO"]).isdigit()
                    else None
                ),
                "estado": row["ESTADO"],
                "municipio": row["MUNICIPIO"],
                "distrito": row["DISTRITO"],
                "subdistrito": row["SUBDISTRITO"],
                "bairro": row["BAIRRO"],
                "cep": row["CEP"],
                "tipoLogradouro": row["TIPO_LOGRADOURO"],
                "rua": row["RUA"],
                "numero": row["NUMERO"],
                "complemento": row["COMPLEMENTO"],
                "latitude": row["LATITUDE"],
                "longitude": row["LONGITUDE"],
                "createdAt": created_at.isoformat(),
                "deletedAt": deleted_at.isoformat() if deleted_at else None,
            }
            records.append(record)

            # If deleted, next installation happens after a short gap (0–30 days)
            if deleted_at:
                current_time = deleted_at + timedelta(days=random.randint(0, 360))
            else:
                # Active installation means no further replacements
                break

    return records


def save_installations_to_csv(records: list[dict], filename: Path) -> None:
    """Save installation records to CSV."""
    Path(filename).parent.mkdir(exist_ok=True)
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    csv_path = Path("data/15_PA.csv.sample")
    output_path = Path("data/installations.csv")

    addresses = load_addresses(csv_path)
    installations = generate_installation_records(addresses)
    save_installations_to_csv(installations, output_path)
