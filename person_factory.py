import random
import pandas as pd
from person import Person
from utils import year_to_decade_label, clamp_int, evenly_spaced_years, ceil_to_int


class PersonFactory:
    """
    Loads input files and generates people, spouses,
    and children according to birth/marriage rates and name distributions.
    """
    

    def __init__(
        self,
        birth_and_marriage_path,
        first_names_path,
        life_expectancy_path,
        last_names_path,
        rank_to_probability_path,
        max_birth_year=2120,
    ):
        self.max_birth_year = max_birth_year

        birth_df = pd.read_csv(birth_and_marriage_path)
        first_df = pd.read_csv(first_names_path)
        life_df = pd.read_csv(life_expectancy_path)
        last_df = pd.read_csv(last_names_path)
        rank_df = pd.read_csv(rank_to_probability_path, header=None)

        self._validate_birth_and_marriage(birth_df)
        self._validate_first_names(first_df)
        self._validate_life_expectancy(life_df)
        self._validate_last_names(last_df)
        self._validate_rank_prob(rank_df)

        self.birth_rate_by_decade = self._build_rate_map(birth_df, "birth_rate")
        self.marriage_rate_by_decade = self._build_rate_map(birth_df, "marriage_rate")

        self.first_names_by_decade = self._build_first_names_undergrad(first_df)
        self.life_expectancy_by_year = self._build_life_expectancy(life_df)
        self.last_names_by_decade = self._build_last_names(last_df, rank_df)

    # Validation Methods
    def _validate_birth_and_marriage(self, df):
        required = {"decade", "birth_rate", "marriage_rate"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"birth_and_marriage_rates.csv missing columns: {missing}")

    def _validate_first_names(self, df):
        required = {"decade", "name", "frequency"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"first_names.csv missing columns: {missing}")

    def _validate_life_expectancy(self, df):
        required = {"Year", "Period life expectancy at birth"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"life_expectancy.csv missing columns: {missing}")

    def _validate_last_names(self, df):
        required = {"Decade", "LastName", "Rank"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"last_names.csv missing columns: {missing}")

    def _validate_rank_prob(self, df):
        if df.shape[0] < 1 or df.shape[1] < 30:
            raise ValueError("rank_to_probability.csv must have at least 1 row and 30 columns")

    """Lookup Methods"""
    def _build_rate_map(self, df, col_name):
        rates = {}
        for _, row in df.iterrows():
            rates[row["decade"]] = float(row[col_name])
        return rates

    def _build_first_names_undergrad(self, df):
        grouped = df.groupby(["decade", "name"], as_index=False)["frequency"].sum()

        out = {}
        for decade, sub in grouped.groupby("decade"):
            out[decade] = (sub["name"].tolist(), sub["frequency"].tolist()) # Code from https://stackoverflow.com/questions/61596613/is-there-any-difference-between-listarray-and-array-tolist-in-python?utm_source=chatgpt.com
        return out

    def _build_life_expectancy(self, df):
        out = {}
        for _, row in df.iterrows():
            out[int(row["Year"])] = float(row["Period life expectancy at birth"])
        return out

    def _build_last_names(self, last_df, rank_df):
        probs = [float(x) for x in rank_df.iloc[0].tolist()[:30]] # Code from https://stackoverflow.com/questions/61596613/is-there-any-difference-between-listarray-and-array-tolist-in-python?utm_source=chatgpt.com

        rank_to_weight = {}
        rank = 1
        while rank <= 30:
            rank_to_weight[rank] = probs[rank - 1]
            rank += 1

        out = {}
        for decade, sub in last_df.groupby("Decade"):
            names = sub["LastName"].tolist() # Code from https://stackoverflow.com/questions/61596613/is-there-any-difference-between-listarray-and-array-tolist-in-python?utm_source=chatgpt.com
            ranks = sub["Rank"].tolist()

            weights = []
            for r in ranks:
                weights.append(rank_to_weight.get(int(r), 0.0))

            out[decade] = (names, weights)

        return out

    # Sampling Helper Methods
    def _get_decade_bucket(self, year_born, table, table_name):
        decade = year_to_decade_label(year_born)
        if decade not in table:
            raise ValueError(f"No {table_name} data for decade '{decade}' (year {year_born})")
        return decade

    def sample_first_name(self, year_born):
        decade = self._get_decade_bucket(year_born, self.first_names_by_decade, "first_names")
        names, weights = self.first_names_by_decade[decade]
        return random.choices(names, weights=weights, k=1)[0] # Code from https://stackoverflow.com/questions/66297512/please-assist-in-understanding-random-choices-weighting

    def sample_spouse_last_name(self, year_born):
        decade = self._get_decade_bucket(year_born, self.last_names_by_decade, "last_names")
        names, weights = self.last_names_by_decade[decade]
        return random.choices(names, weights=weights, k=1)[0] # Code from https://stackoverflow.com/questions/66297512/please-assist-in-understanding-random-choices-weighting

    def get_birth_rate(self, year_born):
        decade = self._get_decade_bucket(year_born, self.birth_rate_by_decade, "birth_rate")
        return self.birth_rate_by_decade[decade]

    def get_marriage_rate(self, year_born):
        decade = self._get_decade_bucket(year_born, self.marriage_rate_by_decade, "marriage_rate")
        return self.marriage_rate_by_decade[decade]

    def sample_year_died(self, year_born):
        year = clamp_int(year_born, 1950, self.max_birth_year)
        if year not in self.life_expectancy_by_year:
            raise ValueError(f"No life expectancy data for year {year}")

        base = self.life_expectancy_by_year[year]
        lifespan = int(round(base + random.uniform(-10, 10)))
        if lifespan < 0:
            lifespan = 0
        return year_born + lifespan

    # Person Generation Methods
    def create_person(self, year_born, last_name):
        first_name = self.sample_first_name(year_born)
        year_died = self.sample_year_died(year_born)
        return Person(year_born, first_name, last_name, year_died)

    def maybe_create_partner(self, person):
        if person.partner is not None:
            return person.partner

        if random.random() >= self.get_marriage_rate(person.year_born):
            return None

        spouse_birth = clamp_int(person.year_born + random.randint(-10, 10), 1950, self.max_birth_year)
        spouse_last = self.sample_spouse_last_name(spouse_birth)
        spouse = self.create_person(spouse_birth, spouse_last)

        person.partner = spouse
        spouse.partner = person
        return spouse

    def compute_num_children(self, parent_birth_year):
        base = self.get_birth_rate(parent_birth_year)
        value = base + random.uniform(-1.5, 1.5) # Code from https://stackoverflow.com/questions/7217595/how-to-generate-highly-uniform-random-number-in-python
        n = ceil_to_int(value)
        if n < 0:
            n = 0
        return n

    def generate_children_for(self, person):
        if person.children_generated:
            return []

        partner = person.partner

        elder_birth = person.year_born
        if partner is not None:
            elder_birth = min(person.year_born, partner.year_born)

        start_year = elder_birth + 25
        end_year = elder_birth + 45

        num_children = self.compute_num_children(person.year_born)
        child_years = evenly_spaced_years(start_year, end_year, num_children)

        children = []
        for y in child_years:
            if y > self.max_birth_year:
                continue

            if partner is None:
                child_last = person.last_name
            else:
                child_last = random.choice([person.last_name, partner.last_name])

            children.append(self.create_person(y, child_last))

        person.children.extend(children)
        if partner is not None:
            partner.children.extend(children)

        person.children_generated = True
        if partner is not None:
            partner.children_generated = True

        return children

