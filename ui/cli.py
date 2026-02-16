from queries.query import FamilyTreeQuery
from core.family_tree import FamilyTree


class FamilyTreeCLI:
    """Command-line interface for family tree queries."""

    def __init__(self, tree: FamilyTree):
        self.tree = tree
        self.query = FamilyTreeQuery(tree)

    def run(self):
        """Run the interactive CLI menu."""
        while True:
            print("\n=== Family Tree Generator ===")
            print("1. Total number of people")
            print("2. People by decade")
            print("3. Duplicate names")
            print("4. Exit")

            try:
                choice = input("\n> ").strip()

                if choice == '1':
                    self._show_total_people()
                elif choice == '2':
                    self._show_people_by_decade()
                elif choice == '3':
                    self._show_duplicate_names()
                elif choice == '4':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _show_total_people(self):
        """Display total number of people."""
        total = self.query.get_total_people()
        print(f"\nThe tree contains {total} people total")

    def _show_people_by_decade(self):
        """Display people count by decade."""
        decade_counts = self.query.get_people_by_decade()

        print("\nPeople by decade:")
        for decade, count in decade_counts.items():
            print(f"{decade}: {count}")

    def _show_duplicate_names(self):
        """Display duplicate names."""
        duplicates = self.query.get_duplicate_names()

        if not duplicates:
            print("\nThere are no duplicate names")
        else:
            print(f"\nThere are {len(duplicates)} duplicate names:")
            for name in duplicates:
                print(f"* {name}")
