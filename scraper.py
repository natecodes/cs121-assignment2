import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# global vars to keep track of links
visited = set()

STOPWORDS = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
             "are", "aren't", "as", "at", " be", "because", "been", "before", "being", "below",
             "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't",
             "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from",
             "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
             "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
             "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not",
             "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
             "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
             "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
             "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
             "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
             "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
             "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
             "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
             "for", "use", "our", "meet", "can", "also", "be", "na", "using", "will", "many", "based", "new", "title",
             "show", "may", "says", "reply", "read"}


def scraper(url, resp):
    links = extract_next_links(url, resp)
    if not links:
        # edge case where we didn't find any links
        return list()
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    links = set()
    if is_valid(url):

        if resp.status >= 200 and resp.status <= 200 and resp.raw_response:
            # we can actually parse the response since it exists
            soup = BeautifulSoup(resp.raw_response.content, "lxml")
            # web_text = soup.get_text()
            # tokens = tokenize(url, resp)

            for link in soup.find_all('a'):
                href = link.get("href")
                if "#" in href:
                    href = href.partition('#')[0]


                # href = urljoin(url, href, allow_fragments=False)

                links.add(href)


                # # check if link found is valid before adding it
                # if is_valid(href):
    return list(links)

# def scrape(url):

def tokenize(url, resp):
    # https://stackoverflow.com/questions/46057942/how-to-get-the-text-tokens-when-using-beautifulsoup
    soup = BeautifulSoup(resp.raw_response.content, "lxml")
    tokens = soup.stripped_strings
    return tokens

def is_valid(url: str) -> bool:
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        # Empty/none URL
        if not url:
            return False

        parsed = urlparse(url)

        # The url does not have http or https scheme
        if parsed.scheme not in set(["http", "https"]):
            return False

        # The url points to a file and not a webpage
        if re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        # The url is not part of ICS/CS/Inf/Stats
        if re.search(r"(\.ics\.uci\.edu)|(\.cs\.uci\.edu)|(\.informatics\.uci\.edu)|(\.stat\.uci\.edu)", parsed.netloc.lower()) == None:
            return False

        # If it passes everything then it is valid so return true
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise
