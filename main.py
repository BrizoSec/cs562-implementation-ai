#!/usr/bin/env python3
"""
Family Tree Generator - CS 562 Graduate Version

This program generates a probabilistic family tree starting from two people
born in 1950, using real demographic data to simulate multiple generations
until 2120 or until no more children can be generated.

Graduate student requirements:
- Gender selection based on gender_name_probability.csv
- Single parents have 1 child fewer than partnered parents
"""

from core.generator import FamilyTreeGenerator
from ui.cli import FamilyTreeCLI


def main():
    """Main entry point for the family tree generator."""
    print("Reading files...")

    # Generate the family tree
    print("Generating family tree...")
    generator = FamilyTreeGenerator()
    tree = generator.generate()

    print(f"Generated tree with {tree.get_total_count()} people")

    # Start interactive CLI
    cli = FamilyTreeCLI(tree)
    cli.run()


if __name__ == '__main__':
    main()
