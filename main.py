from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from itertools import count
from typing import Optional, Protocol


class TicketKategorier(Enum):
    MASKINVARE = "Maskinvare"
    PROGRAMVARE = "Programvare"
    NETTVERK = "Nettverk"
    SKRIVER = "Skriver"
    ANNET = "Annet"


class TicketStatus(Enum):
    AAPEN = "Åpen"
    UNDER_BEHANDLING = "Under Behandling"
    LOST = "Løst"


@dataclass
class Ticket:
    navn: str
    kategori: TicketKategorier
    problem_tittel: str
    problem_tekst: str
    status: TicketStatus = TicketStatus.AAPEN
    opprettet: str = ""
    saksnummer: Optional[int] = None

    def __post_init__(self):
        if not self.opprettet:
            self.opprettet = datetime.now().isoformat(timespec="seconds")

    def __str__(self) -> str:
        linjer = [
            f"Sak #{self.saksnummer or 'Ukjent'}",
            f"|{self.status.value}|",
            f"Registrert av: {self.navn}"
            f"Opprettet: {self.opprettet or 'Ukjent'}"
            f"Problem: {self.problem_tittel}",
            f"Beskrivelse: {self.problem_tekst}",
        ]
        return "\n".join(linjer)


class TicketRepo(Protocol):
    def registrer_ticket(self, ticket: Ticket) -> Ticket: ...
    def hent_ticket(self, saksnummer: int) -> Optional[Ticket]: ...
    def alle_tickets(self) -> list[Ticket]: ...
    def oppdater_ticket(self, ticket: Ticket) -> None: ...
    def slett_ticket(self, saksnummer: int) -> bool: ...


class IMinneRepo:
    def __init__(self):
        self._tickets: dict[int, Ticket] = {}
        self._counter = count(1)

    def registrer_ticket(self, ticket: Ticket) -> Ticket:
        if ticket.saksnummer is None:
            ticket.saksnummer = next(self._counter)
        self._tickets[ticket.saksnummer] = ticket
        return ticket

    def hent_ticket(self, saksnummer: int) -> Optional[Ticket]:
        return self._tickets.get(saksnummer)

    def alle_tickets(self) -> list[Ticket]:
        return list(self._tickets.values())

    def oppdater_ticket(self, ticket: Ticket) -> None:
        if ticket.saksnummer not in self._tickets:
            raise KeyError(
                f"Ticket med saksnummer {ticket.saksnummer} eksisterer ikke."
            )
        self._tickets[ticket.saksnummer] = ticket

    def slett_ticket(self, saksnummer: int) -> bool:
        return self._tickets.pop(saksnummer, None) is not None


def meny(repo: TicketRepo):

    print("=" * 24)
    print("IT-HELLDESK".center(24))
    print("=" * 24)
    print()

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
            registrer_ny_ticket(repo)
        elif meny_valg in ("2", "liste"):
            vis_alle_tickets(repo)
        elif meny_valg in ("3", "oppdater"):
            ...
        elif meny_valg in ("4", "søk"):
            ...
        elif meny_valg in ("5", "avslutt"):
            break
        else:
            print("Ugyldig menyvalg.")
            continue


def vis_alle_tickets(repo: TicketRepo):
    tickets = repo.alle_tickets()
    if not tickets:
        print("Ingen henvendelser registrert.")
        return
    for t in tickets:
        print(t)


def krev_ikke_tom_tekst(ledetekst: str, feilmelding: str) -> str:
    while True:
        verdi = input(ledetekst).strip()
        if not verdi:
            print(feilmelding)
            continue
        return verdi


def registrer_ny_ticket(repo: TicketRepo):
    print("--- Registrer ny henvendelse ---")

    navn = krev_ikke_tom_tekst("Ditt navn: ", "Navn kan ikke være tomt.")
    kategori = velg_kategori()
    tittel = krev_ikke_tom_tekst(
        "Beskrivende tittel på problem: ", "Tittel kan ikke vøre tom."
    )
    tekst = krev_ikke_tom_tekst(
        "Beksrivelse på henvendelse: ", "Beskrivelse kan ikke være tom."
    )

    ny = Ticket(
        navn=navn,
        kategori=kategori,
        problem_tittel=tittel,
        problem_tekst=tekst,
    )
    lagret = repo.registrer_ticket(ny)
    print(f"Opprettet henvendelse med saksnummer {lagret.saksnummer}")


def velg_kategori() -> TicketKategorier: ...


def main() -> None:
    repo: TicketRepo = IMinneRepo()
    meny(repo)


if __name__ == "__main__":
    main()
