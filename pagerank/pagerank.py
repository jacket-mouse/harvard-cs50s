import os
import random
import re
import sys
import pdb
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
            if link in pages  # link必须是corpus里的一员，否则不会添加到集合中
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
    results = dict()
    all_page = set(corpus.keys())# set
    link_page = corpus[page] # set
    sum_all_page = len(all_page)
    sum_link_page = len(link_page)
    if sum_link_page == 0:
        extra_p = 0
        base_p = 1 / sum_all_page
    else:
        extra_p = damping_factor / sum_link_page
        base_p = (1 - damping_factor) / sum_all_page
    for page in all_page:
        results[page] = base_p
        if page in link_page:
            results[page] = results[page] + extra_p
    return results
    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    cur_page = ""
    all_pages = list(corpus)
    results = dict()
    for page in all_pages:
        results[page] = 0
    for i in range(n):
        if i == 0: # random
            cur_page = random.choice(all_pages)
            results[cur_page]  = results[cur_page] + 1
        else:
            cur_model = transition_model(corpus, cur_page, damping_factor)
            # 利用概率进行选择
            cur_page = random.choices(population=list(cur_model.keys()), weights=list(cur_model.values()))[0]
            results[cur_page] = results[cur_page] + 1
    for page in results:
        results[page] = results[page] / SAMPLES
    return results


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # while flag:
    #     flag = False
    #     newrank = {}
    #     for p in pagerank.keys():
    #         x = sum([pagerank[i] / numlinks[i] for i in pagerank.keys() if p in corpus[i] and numlinks[i] > 0])
    #         newrank[p] = (1 - damping_factor) / N + damping_factor * x
    #         if abs(newrank[p] - pagerank[p]) > 1e-3:
    #             flag = True
    #     for p in pagerank.keys():
    #         pagerank[p] = newrank[p]

    N = len(corpus)
    numlinks = {p:len(corpus[p]) for p in corpus.keys()}
    pagerank = dict.fromkeys(corpus.keys(), 1/N)
    while True:
        flag = True
        for page in pagerank.keys():
            cur_pagerank = pagerank[page]
            sum = 0
            for lp in pagerank.keys():
                if page in corpus[lp]:
                    sum += pagerank[lp] / numlinks[lp]
            pagerank[page] = (1 - damping_factor) / N + damping_factor * sum
            if abs(cur_pagerank - pagerank[page]) > 0.001: flag = False
        if flag == True: break
    return pagerank

if __name__ == "__main__":
    main()
