import csv
from pathlib import Path
from typing import Dict, List, Tuple


class DataManager:
    """Singleton class to load and manage demographic data from CSV files."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.base_path = Path(__file__).parent.parent / 'data'

        # Data structures
        self.life_expectancy: Dict[int, float] = {}
        self.first_names: Dict[Tuple[str, str], List[Tuple[str, float]]] = {}
        self.gender_probabilities: Dict[str, Dict[str, float]] = {}
        self.last_names: Dict[str, List[Tuple[str, int]]] = {}
        self.rank_probabilities: List[float] = []
        self.birth_rates: Dict[str, float] = {}
        self.marriage_rates: Dict[str, float] = {}

        self._load_all_data()

    def _load_all_data(self):
        """Load all CSV files."""
        self._load_life_expectancy()
        self._load_first_names()
        self._load_gender_probabilities()
        self._load_last_names()
        self._load_rank_probabilities()
        self._load_birth_and_marriage_rates()

    def _load_life_expectancy(self):
        """Load life expectancy data."""
        path = self.base_path / 'life_expectancy.csv'
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = int(row['Year'])
                expectancy = float(row['Period life expectancy at birth'])
                self.life_expectancy[year] = expectancy

    def _load_first_names(self):
        """Load first names with frequencies by decade and gender."""
        path = self.base_path / 'first_names.csv'
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name']
                decade = row['decade']
                gender = row['gender']
                frequency = float(row['frequency'])

                key = (decade, gender)
                if key not in self.first_names:
                    self.first_names[key] = []
                self.first_names[key].append((name, frequency))

    def _load_gender_probabilities(self):
        """Load gender probabilities by decade."""
        path = self.base_path / 'gender_name_probability.csv'
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row['decade']
                gender = row['gender']
                probability = float(row['probability'])

                if decade not in self.gender_probabilities:
                    self.gender_probabilities[decade] = {}
                self.gender_probabilities[decade][gender] = probability

    def _load_last_names(self):
        """Load last names by decade with ranks."""
        path = self.base_path / 'last_names.csv'
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row['Decade']
                last_name = row['LastName']
                rank = int(row['Rank'])

                if decade not in self.last_names:
                    self.last_names[decade] = []
                self.last_names[decade].append((last_name, rank))

    def _load_rank_probabilities(self):
        """Load rank-to-probability mappings."""
        path = self.base_path / 'rank_to_probability.csv'
        with open(path, 'r') as f:
            # This CSV has no header, just comma-separated probabilities in one line
            content = f.read().strip()
            probabilities = content.split(',')
            for prob_str in probabilities:
                prob = float(prob_str)
                self.rank_probabilities.append(prob)

    def _load_birth_and_marriage_rates(self):
        """Load birth and marriage rates by decade."""
        path = self.base_path / 'birth_and_marriage_rates.csv'
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row['decade']
                birth_rate = float(row['birth_rate'])
                marriage_rate = float(row['marriage_rate'])
                self.birth_rates[decade] = birth_rate
                self.marriage_rates[decade] = marriage_rate

    def get_life_expectancy(self, year: int) -> float:
        """Get life expectancy for a given year."""
        # Find closest year in data
        if year in self.life_expectancy:
            return self.life_expectancy[year]
        # Fallback to nearest year
        closest_year = min(self.life_expectancy.keys(), key=lambda y: abs(y - year))
        return self.life_expectancy[closest_year]

    def get_first_names(self, decade: str, gender: str) -> List[Tuple[str, float]]:
        """Get list of (name, frequency) tuples for a decade and gender."""
        key = (decade, gender)
        if key in self.first_names:
            return self.first_names[key]
        # Fallback to nearest decade
        available_decades = sorted(set(d for d, g in self.first_names.keys() if g == gender))
        if not available_decades:
            return []
        decade_num = int(decade[:-1])
        closest_decade = min(available_decades, key=lambda d: abs(int(d[:-1]) - decade_num))
        return self.first_names.get((closest_decade, gender), [])

    def get_gender_probabilities(self, decade: str) -> Dict[str, float]:
        """Get gender probabilities for a decade."""
        if decade in self.gender_probabilities:
            return self.gender_probabilities[decade]
        # Fallback to nearest decade
        available_decades = sorted(self.gender_probabilities.keys())
        if not available_decades:
            return {'male': 0.5, 'female': 0.5}
        decade_num = int(decade[:-1])
        closest_decade = min(available_decades, key=lambda d: abs(int(d[:-1]) - decade_num))
        return self.gender_probabilities[closest_decade]

    def get_last_names(self, decade: str) -> List[Tuple[str, float]]:
        """Get list of (name, probability) tuples for a decade."""
        if decade not in self.last_names:
            # Fallback to nearest decade
            available_decades = sorted(self.last_names.keys())
            decade_num = int(decade[:-1])
            decade = min(available_decades, key=lambda d: abs(int(d[:-1]) - decade_num))

        names_ranks = self.last_names[decade]
        # Apply rank probabilities
        result = []
        for name, rank in names_ranks:
            if 1 <= rank <= len(self.rank_probabilities):
                prob = self.rank_probabilities[rank - 1]
                result.append((name, prob))
        return result

    def get_birth_rate(self, decade: str) -> float:
        """Get birth rate for a decade."""
        if decade in self.birth_rates:
            return self.birth_rates[decade]
        # Fallback to nearest decade
        available_decades = sorted(self.birth_rates.keys())
        decade_num = int(decade[:-1])
        closest_decade = min(available_decades, key=lambda d: abs(int(d[:-1]) - decade_num))
        return self.birth_rates[closest_decade]

    def get_marriage_rate(self, decade: str) -> float:
        """Get marriage rate for a decade."""
        if decade in self.marriage_rates:
            return self.marriage_rates[decade]
        # Fallback to nearest decade
        available_decades = sorted(self.marriage_rates.keys())
        decade_num = int(decade[:-1])
        closest_decade = min(available_decades, key=lambda d: abs(int(d[:-1]) - decade_num))
        return self.marriage_rates[closest_decade]
