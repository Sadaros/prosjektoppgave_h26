from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from itertools import count


class TicketKategorier(Enum): ...


class TicketStatus(Enum):
    aapen = "Åpen"
    lost = "Løst"


@dataclass
class Ticket:
    kategori: TicketKategorier
    problem_tittel: str
    problem_tekst: str
    status: TicketStatus = TicketStatus.aapen
    opprettet: datetime = field(default_factory=datetime.now)
    saksnummer: int = field(default_factory=count(1).__next__)


def main():
    ticket_liste: list[Ticket] = []

    print("=" * 24)
    print("IT-HELLDESK".center(24))
    print("=" * 24)

    while True:
        print("Meny:")
        print("1. Registrer sak")
        print("2. Liste over saker")
        print("3. Oppdater sak")
        print("4. Søk på sak")
        print("5. Avslutt")
        print()

        meny_valg = input("Valg:").strip().casefold()

        if meny_valg in ("1", "registrer"):
            ...
        elif meny_valg in ("2", "liste"):
            ...
        elif meny_valg in ("3", "oppdater"):
            ...
        elif meny_valg in ("4", "søk"):
            ...
        elif meny_valg in ("5", "avslutt"):
            break

        else:
            print("Ugyldig menyvalg.")
            continue


if __name__ == "__main__":
    main()
