class FamilyTree:
    """
    Represents the full family tree structure.
    Uses a factory to create people and expand descendents.
    """


    def __init__(self, factory):
        self.factory = factory
        self.roots = []
        self.people = []

    def initialize_roots(self):
        """Create the two initial root people (both born in 1950)."""
        year = 1950
        last1 = self.factory.sample_spouse_last_name(year)
        last2 = self.factory.sample_spouse_last_name(year)

        p1 = self.factory.create_person(year, last1)
        p2 = self.factory.create_person(year, last2)

        self.roots = [p1, p2]
        self.people = [p1, p2]

    def generate(self):
        """Generate the family tree by iterating through the list of known people.
        For each person:
          1) maybe create a partner
          2) generate children (even if no partner)
        """
        if not self.roots:
            self.initialize_roots()

        i = 0
        while i < len(self.people):
            person = self.people[i]

            spouse = self.factory.maybe_create_partner(person)
            if spouse is not None and spouse not in self.people:
                self.people.append(spouse)

            children = self.factory.generate_children_for(person)
            for child in children:
                self.people.append(child)

            i += 1

    def total_people(self):
        """Return the total number of people in the tree."""
        return len(self.people)

    def count_by_decade(self):
        """
        Return a dict mapping decade-start year (int) to number of people born
        in that decade. The dict is returned in sorted decade order.
        """
        counts = {}
        for p in self.people:
            decade = (p.year_born // 10) * 10  
            counts[decade] = counts.get(decade, 0) + 1

        return dict(sorted(counts.items()))

    def duplicate_full_names(self):
        """
        Return a dict mapping duplicated full names to when they occur.
        Only names that appear 2+ times.
        """
        counts = {}
        for p in self.people:
            name = p.full_name()
            counts[name] = counts.get(name, 0) + 1

        dups = {}
        for name, cnt in counts.items():
            if cnt >= 2:
                dups[name] = cnt

        return dups
