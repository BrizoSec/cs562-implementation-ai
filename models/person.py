from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Person:
    """Represents a person in the family tree."""
    id: int
    first_name: str
    last_name: str
    gender: str
    year_born: int
    year_died: Optional[int]
    generation: int
    parent1: Optional['Person'] = None
    parent2: Optional['Person'] = None
    partner: Optional['Person'] = None
    children: list['Person'] = field(default_factory=list)

    def is_alive(self, year: int) -> bool:
        """Check if person is alive in a given year."""
        if year < self.year_born:
            return False
        if self.year_died is None:
            return True
        return year < self.year_died

    def can_have_children(self, year: int) -> bool:
        """Check if person can have children in a given year (age 25-45)."""
        age = year - self.year_born
        return 25 <= age <= 45 and self.is_alive(year)

    def get_birth_decade(self) -> str:
        """Get the decade of birth (e.g., '1950s')."""
        decade_start = (self.year_born // 10) * 10
        return f"{decade_start}s"

    def get_full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Person(id={self.id}, name={self.get_full_name()}, born={self.year_born}, gen={self.generation})"
