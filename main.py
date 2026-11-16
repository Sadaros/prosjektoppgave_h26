from dataclasses import dataclass
from enum import Enum


class TicketKategorier(Enum): ...


@dataclass
class Ticket:
    saksnummer: int
    kategori: TicketKategorier
    problem_tittel: str
    problem_tekst: str


def main():
    pass


if __name__ == "__main__":
    main()
