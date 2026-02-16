from typing import List
from models.person import Person


class FamilyTree:
    """Container class for managing the family tree structure."""

    def __init__(self):
        self.founders: List[Person] = []
        self.all_people: List[Person] = []

    def add_founder(self, person: Person):
        """Add a founder to the tree."""
        self.founders.append(person)
        self.all_people.append(person)

    def add_person(self, person: Person):
        """Add a person to the tree."""
        self.all_people.append(person)

    def get_all_people(self) -> List[Person]:
        """Get all people in the tree."""
        return self.all_people

    def get_founders(self) -> List[Person]:
        """Get the founder persons."""
        return self.founders

    def get_total_count(self) -> int:
        """Get total number of people in the tree."""
        return len(self.all_people)
