# AI Assignment 01 - Kids in the Yard

This version was generated using generative AI. For the comparison portion of the project I compared this against 
my implementation. 

## Notes 
- Used a mix of Claude and Gemini for generating

## AI Usage Guide (Claude based README)

The AI actually generated the following usage guide which is super helpful, albeit long-winded. 

----------

# Family Tree Generator - Usage Guide

## Overview

This is a probabilistic family tree generator that simulates multiple generations starting from two people born in 1950, using real demographic data from CSV files.

## Running the Program

```bash
python3 main.py
```

## Features

### Graduate Requirements Implemented
✅ Gender selection based on `gender_name_probability.csv`
✅ Single parents have 1 child fewer than partnered parents

### Demographic Rules
- **Starting point**: 2 people born in 1950
- **End condition**: Year 2120 or no more children possible
- **Parent age constraints**: Children born when parents are 25-45 years old
- **Marriage**: Probabilistic based on decade-specific marriage rates
- **Birth rate**: Varies by decade with ±1.5 random variation
- **Names**: Weighted selection from historical frequency data
- **Life expectancy**: Based on birth year with ±10 year variation

## Interactive Queries

Once the tree is generated, you can run queries:

1. **Total number of people**: Shows total count in the tree
2. **People by decade**: Shows how many people were born in each decade
3. **Duplicate names**: Shows which full names appear more than once
4. **Exit**: Quit the program

## Project Structure

```
├── main.py                    # Entry point
├── models/
│   └── person.py             # Person dataclass
├── core/
│   ├── data_manager.py       # CSV data loader (singleton)
│   ├── person_factory.py     # Person creation logic
│   ├── family_tree.py        # Tree container
│   └── generator.py          # BFS generation engine
├── queries/
│   └── query.py              # Query methods
├── ui/
│   └── cli.py                # Command-line interface
└── [CSV files]               # Demographic data
```

## Data Files

The program uses these CSV files (already provided):
- `life_expectancy.csv` - Life expectancy by year (1950-2120)
- `first_names.csv` - 1,765 names with frequencies by decade/gender
- `gender_name_probability.csv` - Gender probabilities by decade
- `last_names.csv` - 30 last names per decade with rankings
- `rank_to_probability.csv` - Probability weights for name rankings
- `birth_and_marriage_rates.csv` - Birth/marriage rates by decade

## Example Output

```
Reading files...
Generating family tree...
Generated tree with 144 people

=== Family Tree Generator ===
1. Total number of people
2. People by decade
3. Duplicate names
4. Exit

> 1
The tree contains 144 people total

> 2
People by decade:
1950s: 2
1970s: 3
1980s: 5
...

> 3
There are 8 duplicate names:
* James Smith
* Mary Johnson
* ...
```

## Performance

- **Generation time**: 1-5 seconds
- **Tree size**: Highly variable due to randomness (typically 40-300 people)
- **Generations**: Usually 5-7 generations
- **Memory usage**: < 50MB

## Algorithm

The generator uses a BFS (Breadth-First Search) approach:

1. Create 2 founders born in 1950
2. Determine if they partner (based on marriage rate)
3. Process each person in generation order:
   - Calculate number of children (with -1 penalty for single parents)
   - Distribute birth years evenly in parent's age 25-45 range
   - For each child, determine if they find a partner
   - Add children to queue for next generation
4. Continue until year 2120 or no more children possible

## Validation

All generated trees satisfy:
- ✅ All people born between 1950-2120
- ✅ All children born when parents age 25-45
- ✅ All children have exactly 2 parents (or 1 parent + placeholder for single parents)
- ✅ Death year ≥ birth year for all people
- ✅ Single parents have fewer children than partnered parents
