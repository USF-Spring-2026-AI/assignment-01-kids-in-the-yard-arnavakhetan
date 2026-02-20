class Person:
    """
    Represents a single person in the family tree.
    Each person is assigned a unique incremental ID.
    """


    next_id = 1

    def __init__(self, year_born, first_name, last_name, year_died):
        """
        Assign a unique ID to each person.
        Create basic identity information and family relationships.
        """
        self.id = Person.next_id
        Person.next_id += 1

        self.year_born = int(year_born)
        self.first_name = first_name
        self.last_name = last_name
        self.year_died = int(year_died)

        self.partner = None
        self.children = []
        self.children_generated = False

    def full_name(self):
        """Return the person's full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """
        String representation.
        Shows ID, name, birth/death years, partner ID, and number of children.
        """
        partner_id = None
        if self.partner is not None:
            partner_id = self.partner.id

        return (
            f"Person(id={self.id}, name='{self.full_name()}', "
            f"born={self.year_born}, died={self.year_died}, "
            f"partner={partner_id}, children={len(self.children)})"
        )