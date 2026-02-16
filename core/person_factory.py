import random
from typing import Optional
from models.person import Person
from core.data_manager import DataManager


class PersonFactory:
    """Factory class for creating Person instances with randomized attributes."""

    def __init__(self, seed: Optional[int] = None):
        self.data_manager = DataManager()
        self.rng = random.Random(seed)
        self.next_id = 1

    def create_founder(self) -> Person:
        """Create a founder person born in 1950."""
        year_born = 1950
        decade = "1950s"

        # Select gender using gender probabilities
        gender = self._select_gender(decade)

        # Select first name
        first_name = self._select_first_name(decade, gender)

        # Select last name
        last_name = self._select_last_name(decade)

        # Calculate death year
        year_died = self._calculate_death_year(year_born)

        person = Person(
            id=self.next_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            year_born=year_born,
            year_died=year_died,
            generation=0
        )

        self.next_id += 1
        return person

    def create_child(self, parent1: Person, parent2: Person, year_born: int) -> Person:
        """Create a child from two parents."""
        decade = f"{(year_born // 10) * 10}s"

        # Select gender
        gender = self._select_gender(decade)

        # Select first name
        first_name = self._select_first_name(decade, gender)

        # Inherit last name from parent1 (arbitrary choice)
        last_name = parent1.last_name

        # Calculate death year
        year_died = self._calculate_death_year(year_born)

        # Generation is one more than parents
        generation = parent1.generation + 1

        person = Person(
            id=self.next_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            year_born=year_born,
            year_died=year_died,
            generation=generation,
            parent1=parent1,
            parent2=parent2
        )

        self.next_id += 1
        return person

    def create_partner(self, person: Person) -> Person:
        """Create a partner for a person (born within ±10 years)."""
        # Partner born within ±10 years, but not after 2120
        year_offset = self.rng.randint(-10, 10)
        year_born = min(person.year_born + year_offset, 2120)
        decade = f"{(year_born // 10) * 10}s"

        # Select gender (opposite of person for simplicity, though not required)
        gender = self._select_gender(decade)

        # Select first name
        first_name = self._select_first_name(decade, gender)

        # Select last name (independent, not inherited)
        last_name = self._select_last_name(decade)

        # Calculate death year
        year_died = self._calculate_death_year(year_born)

        # Partner is same generation
        generation = person.generation

        partner = Person(
            id=self.next_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            year_born=year_born,
            year_died=year_died,
            generation=generation
        )

        self.next_id += 1
        return partner

    def _select_gender(self, decade: str) -> str:
        """Select gender based on decade probabilities."""
        probs = self.data_manager.get_gender_probabilities(decade)
        return self.rng.choices(
            ['male', 'female'],
            weights=[probs['male'], probs['female']],
            k=1
        )[0]

    def _select_first_name(self, decade: str, gender: str) -> str:
        """Select first name using weighted probabilities."""
        items = self.data_manager.get_first_names(decade, gender)
        if not items:
            # Fallback if no names available
            return "Unknown"

        names, weights = zip(*items)
        return self.rng.choices(names, weights=weights, k=1)[0]

    def _select_last_name(self, decade: str) -> str:
        """Select last name using rank probabilities."""
        items = self.data_manager.get_last_names(decade)
        if not items:
            # Fallback if no names available
            return "Unknown"

        names, weights = zip(*items)
        return self.rng.choices(names, weights=weights, k=1)[0]

    def _calculate_death_year(self, year_born: int) -> Optional[int]:
        """Calculate death year based on life expectancy."""
        life_expectancy = self.data_manager.get_life_expectancy(year_born)

        # Add random variation ±10 years
        variation = self.rng.uniform(-10, 10)
        death_year = int(year_born + life_expectancy + variation)

        # Don't return death year beyond 2120 (they might still be alive)
        if death_year > 2120:
            return None

        return death_year
