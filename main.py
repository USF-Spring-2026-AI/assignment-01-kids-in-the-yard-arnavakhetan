import os
from person_factory import PersonFactory
from family_tree import FamilyTree


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Code from https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam

def main():
    print("Reading files...")
    try: 
        factory = PersonFactory( # Code from https://stackoverflow.com/questions/43287860/dirs-os-path-joinbase-dir-myfolder-templates-nameerror-name-os
            birth_and_marriage_path=os.path.join(BASE_DIR, "birth_and_marriage_rates.csv"),
            first_names_path=os.path.join(BASE_DIR, "first_names.csv"),
            life_expectancy_path=os.path.join(BASE_DIR, "life_expectancy.csv"),
            last_names_path=os.path.join(BASE_DIR, "last_names.csv"),
            rank_to_probability_path=os.path.join(BASE_DIR, "rank_to_probability.csv"),
            max_birth_year=2120,
        )
    except FileNotFoundError as e:
        print("Error: Missing required file.")
        print(e)
        return

    print("Generating family tree...")
    tree = FamilyTree(factory)
    tree.generate()

    while True:
        print("Are you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")
        choice = input("> ").strip().upper()

        if choice == "T":
            print(f"The tree contains {tree.total_people()} people total")

        elif choice == "D":
            by_decade = tree.count_by_decade()
            for decade_start, count in by_decade.items():
                print(f"{decade_start}: {count}")

            print("[Remainder not shown]")

        elif choice == "N":
            dups = tree.duplicate_full_names()
            print(f"There are {len(dups)} duplicate names in the tree:")
            for name in dups.keys():
                print(f"* {name}")

        elif choice == "Q":
            break

        else:
            print("Invalid option. Enter T, D, N, or Q.")


if __name__ == "__main__":
    main()
