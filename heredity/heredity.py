import csv
import itertools
import sys

from operator import mul
from functools import reduce

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    
    with open(filename) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    def pass_down(genes, passing):
        """
        Computes the probability that a person will or won't pass the gene 
        dictated by 'passing' based on that person's number of genes.
        """

        if genes == 2 and passing or genes == 0 and not passing:
            return 1 - PROBS["mutation"]
        elif genes == 2 and not passing or genes == 0 and passing:
            return PROBS["mutation"]
        elif genes == 1:
            return 0.5
        
    
    # Initialize set of probabilities, then calculate all
    probabilities = set()
    for name in people:
        if people[name]["mother"] is people[name]["father"] is None:
            # No recorded parents; use PROBS table to calculate
            genes = 2 if name in two_genes else 1 if name in one_gene else 0
            probabilities.add(PROBS["gene"][genes] * 
                                PROBS["trait"][genes][name in have_trait])

        else:
            # Perform calculation based on parent probabilities
            # First calculate gene probability
            mother = people[name]["mother"]
            father = people[name]["father"]
            mg = 2 if mother in two_genes else 1 if mother in one_gene else 0
            fg = 2 if father in two_genes else 1 if father in one_gene else 0
            geneChance = 0

            if name in two_genes:
                geneChance = pass_down(mg, True) * pass_down(fg, True)
            elif name in one_gene:
                geneChance = (
                    pass_down(mg, True) * pass_down(fg, False) +
                    pass_down(mg, False) * pass_down(fg, True)
                )
            else:
                geneChance = pass_down(mg, False) * pass_down(fg, False)
            
            # Then calculate trait probability
            genes = 2 if name in two_genes else 1 if name in one_gene else 0
            traitChance = PROBS["trait"][genes][name in have_trait]
            probabilities.add(geneChance * traitChance)
    
    return reduce(mul, probabilities, 1)
                

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    # Iterate over all people, adding p to the relevant dictionary values
    for person in probabilities:
        genes = 2 if person in two_genes else 1 if person in one_gene else 0
        
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        for category in probabilities[person]:
            total = sum(probabilities[person][category].values())

            for value in probabilities[person][category]:
                probabilities[person][category][value] /= total


if __name__ == "__main__":
    main()
