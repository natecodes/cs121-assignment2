import re
from urllib.parse import urlsplit, urljoin
from urllib.robotparser import RobotFileParser

from bs4 import BeautifulSoup

# question 1 - unique webpages
unique_urls = set()

# testing
all_urls = set()

# question 2 - longest page
longest_page = ["placeholder", 0]

# question 3 - 50 most common words
common_words = dict()

STOP_WORDS = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
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

# fetch the robots.txt
ICS_ROBOTS_TXT = RobotFileParser('https://www.ics.uci.edu/robots.txt')
CS_ROBOTS_TXT = RobotFileParser('https://www.cs.uci.edu/robots.txt')
STAT_ROBOTS_TXT = RobotFileParser('https://www.stat.uci.edu/robots.txt')
INF_ROBOTS_TXT = RobotFileParser('https://www.informatics.uci.edu/robots.txt')
ICS_ROBOTS_TXT.read()
CS_ROBOTS_TXT.read()
STAT_ROBOTS_TXT.read()
INF_ROBOTS_TXT.read()

count = 1
def scraper(url, resp):
    # out_file = open("Outa.txt", 'a')
    # global count
    # out_file.write(f'Scraper has run {count} times\n')
    # count += 1
    # out_file.close()

    links = extract_next_links(url, resp)
    # edge case where we didn't find any links
    if not links:
        return list()

    generate_answers()
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

    # check if response exists and it is successful
    # Detect and avoid dead URLs that return a 200 status but no data
    if url and resp.status >= 200 and resp.status <= 299 and resp.raw_response:

        # defragment and add the unique url
        unique_urls.add(url.partition('#')[0])
        all_urls.add(url)

        soup = BeautifulSoup(resp.raw_response.content, "lxml")

        # get all the text on the page
        web_text = soup.get_text(separator=' ', strip=True).lower()

        # remove all non-alpha characters
        web_text = re.sub('[^A-Za-z]+', ' ', web_text)

        # split by whitespace
        tokens = web_text.split()

        # question 2
        if len(tokens) > longest_page[1]:
            longest_page[0] = url
            longest_page[1] = len(tokens)

        # remove stop word tokens and bs tokens
        tokens_without_stop = [token for token in tokens if token not in STOP_WORDS and len(token) >= 2]

        # update the token dictionary - question 3
        for token in tokens_without_stop:
            if token in common_words:
                common_words[token] += 1
            else:
                common_words[token] = 1

        # scrape the links
        for link in soup.find_all('a'):
            href = link.get("href")
            if href and '#' in href:
                href = href.partition('#')[0]
            links.add(href)

    return list(links)

def is_valid(url: str) -> bool:

    # return False
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        # Empty/none URL
        if not url:
            return False

        url = url.lower()
        # don't use urlparse because of params / outdated format
        parsed = urlsplit(url)

        # we already visited the url
        # if url in unique_urls:
        #     return False

        # The url does not have http or https scheme
        if parsed.scheme not in {"http", "https"}:
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

        if '.pdf' in parsed.path or '/pdf/' in parsed.path:
            return False

        # The url is not part of ICS/CS/Inf/Stats
        if re.search(r"(\.ics\.uci\.edu)|(\.cs\.uci\.edu)|(\.informatics\.uci\.edu)|(\.stat\.uci\.edu)", parsed.netloc) == None:
            return False

        # check robots.txt extra credit
        if 'ics.uci.edu' in parsed.netloc:
            if not ICS_ROBOTS_TXT.can_fetch('*', url):
                return False
        elif 'cs.uci.edu' in parsed.netloc:
            if not CS_ROBOTS_TXT.can_fetch('*', url):
                return False
        elif 'stat.uci.edu' in parsed.netloc:
            if not STAT_ROBOTS_TXT.can_fetch('*', url):
                return False
        elif 'informatics.uci.edu' in parsed.netloc:
            if not INF_ROBOTS_TXT.can_fetch('*', url):
                return False

        # this was my manual implementation until I found the robotparser module...
        # if 'ics.uci.edu' in parsed.netloc:
        #     if parsed.path.startswith('/bin/') or parsed.path.startswith('/~mpufal/'):
        #         return False
        # elif 'cs.uci.edu' in parsed.netloc:
        #     if parsed.path.startswith('/wp-admin/'):
        #         if not 'wp-admin/admin-ajax.php' in parsed.path:
        #             return False
        # elif 'stat.uci.edu' in parsed.netloc:
        #     if parsed.path.startswith('/wp-admin/'):
        #         if not 'wp-admin/admin-ajax.php' in parsed.path:
        #             return False
        # elif 'informatics.uci.edu' in parsed.netloc:
        #     if parsed.path.startswith('/wp-admin/'):
        #         if not 'wp-admin/admin-ajax.php' in parsed.path:
        #             return False
        #     elif parsed.path.startswith('/research/'):
        #         if not '/research/labs-centers/' in parsed.path and \
        #             not '/research/areas-of-expertise/' in parsed.path and \
        #             not '/research/example-research-projects/' in parsed.path and \
        #             not '/research/phd-research/' in parsed.path and \
        #             not '/research/past-dissertations/' in parsed.path and \
        #             not '/research/masters-research/' in parsed.path and \
        #             not '/research/undergraduate-research/' in parsed.path and \
        #             not '/research/gifts-grants/' in parsed.path:
        #             return False

        # If it passes everything then it is valid so return true
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def generate_answers():
    q1_file = open("Question 1a.txt", "w")
    q2_file = open("Question 2a.txt", "w")
    q3_file = open("Question 3a.txt", "w")
    q4_file = open("Question 4a.txt", "w")

    q1_file.write(f"\n\nNumber of Unique URLs: {len(unique_urls)}\n\n")
    for url in unique_urls:
        q1_file.write(url + "\n")

    q1_file.write("\n\nALL URLS:\n\n")

    for url in all_urls:
        q1_file.write(url + "\n")

    q2_file.write(f"\n\nLongest page and number of words: {longest_page[0]} , {longest_page[1]}\n\n")
    q3_file.write("\n\n50 most common words in the entire set of pages crawled under these domains:\n")
    for word, freq in sorted(common_words.items(), key=lambda x: -x[1]):
        q3_file.write(f"{word} -> {freq}\n")
    q4_file.write("Subdomains in ics.uci.edu and number of unique pages: ")

    q1_file.close()
    q2_file.close()
    q3_file.close()
    q4_file.close()
