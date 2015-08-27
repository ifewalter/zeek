import urlparse
import uuid
import bs4
from BeautifulSoup import Comment


class Container:
    def __init__(self):
        #data = dict()
        self.hasData = False

        self.title = None
        self.author = None
        self.content = None
        self.date = None
        self.domain = None
        self.random = None


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def scrape(url, bs):
    # for testing - this is scrapping article titles from www.nytimes.com
    container = Container()
    domain = urlparse.urlsplit(url)[1].split(':')[0]
    container.author = domain

    container.random = my_random_string(6)

    container.domain = domain
    # extracting data from NYTimes

    container.title = bs.title.string

    # kill all script and style elements
    for script in bs(["script", "style", "meta", "title"]):
        script.extract()    # rip it out

    # get text

    comments = bs.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]

    content_text = bs.get_text()

    print content_text

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in content_text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    container.content = '\n'.join(chunk for chunk in chunks if chunk)
    container.content = content_text
    return container
