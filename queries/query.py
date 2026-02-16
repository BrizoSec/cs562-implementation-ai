from typing import Dict, List
from collections import defaultdict, Counter
from core.family_tree import FamilyTree


class FamilyTreeQuery:
    """Provides query interface for the family tree."""

    def __init__(self, tree: FamilyTree):
        self.tree = tree

    def get_total_people(self) -> int:
        """Get total number of people in the tree."""
        return self.tree.get_total_count()

    def get_people_by_decade(self) -> Dict[str, int]:
        """Get count of people born in each decade."""
        decade_counts = defaultdict(int)

        for person in self.tree.get_all_people():
            decade = person.get_birth_decade()
            decade_counts[decade] += 1

        # Sort by decade
        sorted_decades = sorted(decade_counts.items(), key=lambda x: int(x[0][:-1]))
        return dict(sorted_decades)

    def get_duplicate_names(self) -> List[str]:
        """Get list of names that appear more than once."""
        name_counter = Counter()

        for person in self.tree.get_all_people():
            full_name = person.get_full_name()
            name_counter[full_name] += 1

        # Find duplicates
        duplicates = [name for name, count in name_counter.items() if count > 1]
        return sorted(duplicates)
