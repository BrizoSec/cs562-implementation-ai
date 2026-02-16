import random
from collections import deque
from typing import List, Optional, Tuple
from models.person import Person
from core.family_tree import FamilyTree
from core.person_factory import PersonFactory
from core.data_manager import DataManager


class FamilyTreeGenerator:
    """Main generation engine using BFS algorithm."""

    def __init__(self, seed: Optional[int] = None):
        self.factory = PersonFactory(seed)
        self.data_manager = DataManager()
        self.rng = random.Random(seed)
        self.tree = FamilyTree()

    def generate(self) -> FamilyTree:
        """Generate the complete family tree."""
        # Create two founders born in 1950
        founder1 = self.factory.create_founder()
        founder2 = self.factory.create_founder()

        self.tree.add_founder(founder1)
        self.tree.add_founder(founder2)

        # Determine if founders partner with each other
        decade = "1950s"
        marriage_rate = self.data_manager.get_marriage_rate(decade)

        if self.rng.random() < marriage_rate:
            founder1.partner = founder2
            founder2.partner = founder1

        # Initialize queue with founders
        queue = deque([founder1, founder2])

        # BFS generation
        while queue:
            person = queue.popleft()

            # Skip if person already has children
            if person.children:
                continue

            # Skip if person has no partner (single parent case handled in child calculation)
            # Actually, we allow single parents per graduate requirements
            # if person.partner is None:
            #     continue

            # Generate children for this person
            children = self._generate_children(person)

            for child in children:
                self.tree.add_person(child)

                # Add child to parent's children list
                person.children.append(child)
                if person.partner:
                    person.partner.children.append(child)

                # Determine if child finds a partner
                child_decade = child.get_birth_decade()
                marriage_rate = self.data_manager.get_marriage_rate(child_decade)

                if self.rng.random() < marriage_rate:
                    partner = self.factory.create_partner(child)
                    child.partner = partner
                    partner.partner = child
                    self.tree.add_person(partner)

                # Add child to queue for next generation
                queue.append(child)

        return self.tree

    def _generate_children(self, person: Person) -> List[Person]:
        """Generate children for a person."""
        # Calculate number of children
        num_children = self._calculate_num_children(person)

        if num_children <= 0:
            return []

        # Determine valid birth year range
        if person.partner:
            birth_years = self._distribute_birth_years(person, person.partner, num_children)
        else:
            # Single parent case
            birth_years = self._distribute_birth_years_single(person, num_children)

        # Create children
        children = []
        for year in birth_years:
            # Check year limit
            if year > 2120:
                break

            # Create child with both parents if partnered, otherwise single parent
            if person.partner:
                child = self.factory.create_child(person, person.partner, year)
            else:
                # Single parent - create a placeholder partner with compatible birth year
                # Partner must be age 25-45 when child is born
                partner_birth_min = year - 45
                partner_birth_max = year - 25
                partner_birth = self.rng.randint(partner_birth_min, partner_birth_max)

                temp_partner = Person(
                    id=-1,  # Dummy ID
                    first_name="Unknown",
                    last_name="Unknown",
                    gender="male" if person.gender == "female" else "female",
                    year_born=partner_birth,
                    year_died=None,
                    generation=person.generation
                )
                child = self.factory.create_child(person, temp_partner, year)

            children.append(child)

        return children

    def _calculate_num_children(self, person: Person) -> int:
        """Calculate number of children based on birth rate."""
        decade = person.get_birth_decade()
        base_rate = self.data_manager.get_birth_rate(decade)

        # Add random variation ±1.5
        variation = self.rng.uniform(-1.5, 1.5)
        children = base_rate + variation

        # Graduate requirement: single parents have 1 fewer child
        if person.partner is None:
            children -= 1

        return max(0, round(children))

    def _distribute_birth_years(self, parent1: Person, parent2: Person, num_children: int) -> List[int]:
        """Distribute birth years for children between two parents."""
        # Find valid range where both parents age 25-45 and alive
        # Start: both parents must be at least 25
        start = max(parent1.year_born + 25, parent2.year_born + 25)

        # End: both parents must be at most 45
        end = min(parent1.year_born + 45, parent2.year_born + 45)

        # Consider death years (children must be born before parents die)
        if parent1.year_died:
            end = min(end, parent1.year_died - 1)
        if parent2.year_died:
            end = min(end, parent2.year_died - 1)

        # Apply 2120 limit
        end = min(end, 2120)

        # Check if valid range exists
        if start > end:
            return []

        # Distribute children evenly across the range
        if num_children == 1:
            return [(start + end) // 2]

        birth_years = []
        if num_children > 1:
            interval = (end - start) / (num_children - 1)
            for i in range(num_children):
                year = int(start + i * interval)
                # Ensure year doesn't exceed end due to rounding
                year = min(year, end)
                birth_years.append(year)

        return birth_years

    def _distribute_birth_years_single(self, parent: Person, num_children: int) -> List[int]:
        """Distribute birth years for children of a single parent."""
        start = parent.year_born + 25
        end = parent.year_born + 45

        # Consider death year (children must be born before parent dies)
        if parent.year_died:
            end = min(end, parent.year_died - 1)

        # Apply 2120 limit
        end = min(end, 2120)

        # Check if valid range exists
        if start > end:
            return []

        # Distribute children evenly across the range
        if num_children == 1:
            return [(start + end) // 2]

        birth_years = []
        if num_children > 1:
            interval = (end - start) / (num_children - 1)
            for i in range(num_children):
                year = int(start + i * interval)
                # Ensure year doesn't exceed end due to rounding
                year = min(year, end)
                birth_years.append(year)

        return birth_years
