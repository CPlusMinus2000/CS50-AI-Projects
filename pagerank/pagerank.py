import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # Initialize empty model
    model = {}
    for pg in corpus:
        model[pg] = 0

    if corpus[page]:
        # If current page has links, calculate probabilities using them
        for link in corpus[page]:
            model[link] += damping_factor / len(corpus[page])
    
    else:
        # Set damping factor to 0
        damping_factor = 0
    
    for pg in corpus:
        model[pg] += (1 - damping_factor) / len(corpus)
    
    return model


def weighted_random_by_dct(dct):
    "Chooses a key from dct random using the values as probabilities."

    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initialize an empty dictionary of values
    ranks = {}
    for pg in corpus:
        ranks[pg] = 0
    
    # Get a random page, and add it to the ranks
    page = random.choice(list(corpus))
    ranks[page] += 1

    # Perform sampling n times
    for i in range(n):
        # Get the next page out of the transition model
        model = transition_model(corpus, page, damping_factor)
        page = weighted_random_by_dct(model)
        
        ranks[page] += 1
    
    for rank in ranks:
        ranks[rank] /= n
    
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Start by initializing the dictionary of pageranks to the default
    # as well as a dictionary of pagerank difference booleans
    ranks = rank_diffs = {}
    for pg in corpus:
        ranks[pg] = 1 / len(corpus)
        rank_diffs[pg] = False

    # Now, iteratively calculate pageranks until rank_diffs is all True
    while not all(diff for diff in rank_diffs.values()):
        newRanks = {}
        for pg in corpus:
            newRank = 0
            for p in [p for p in corpus if pg in corpus[p]]:
                newRank += ranks[p] / len(corpus[p])
            
            for p in [p for p in corpus if not corpus[p]]:
                newRank += ranks[p] / len(corpus)
            
            newRank = newRank * damping_factor + (1 - damping_factor) / len(corpus)
            rank_diffs[pg] = abs(ranks[pg] - newRank) <= 0.001
            newRanks[pg] = newRank
        
        ranks = newRanks
    
    return ranks


if __name__ == "__main__":
    main()
