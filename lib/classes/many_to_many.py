class Article:
    # List to keep track of all articles
    all = []

    def __init__(self, author, magazine, title):
        # Initialize an article with author, magazine, and title
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self.author = author  # Set the author of the article
        self.magazine = magazine  # Set the magazine of the article
        self._title = title  # Set the title of the article (this cannot be changed later)
        
        magazine._articles.append(self)  # Add the article to the magazine's article list
        author._articles.append(self)  # Add the article to the author's article list
        Article.all.append(self)  # Add the article to the global list of articles

    @property
    def title(self):
        # Get the title of the article
        return self._title

    @title.setter
    def title(self, value):
        # Prevent changing the title after initialization
        raise AttributeError("Title cannot be changed after initialization")


class Author:
    def __init__(self, name):
        # Initialize the author with a name
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author's name must be a non-empty string")
        self._name = name  # Set the author's name
        self._articles = []  # Initialize an empty list to hold the author's articles

    @property
    def name(self):
        # Get the author's name
        return self._name

    @name.setter
    def name(self, value):
        # Prevent changing the author's name after it's set
        raise AttributeError("Author's name cannot be changed once set")

    def articles(self):
        # Return a list of all the author's articles
        return self._articles

    def magazines(self):
        # Return a list of unique magazines the author has written for
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        # Create and return a new article written by this author
        return Article(self, magazine, title)
    
    def topic_areas(self):
        # Return a list of unique topic areas (magazine categories) for all articles by the author
        # Ensure it returns a list, not None, even if no articles are available
        return list(set(article.magazine.category for article in self._articles)) if self._articles else None


class Magazine:
    # List to keep track of all magazines
    all = []

    def __init__(self, name, category):
        # Initialize the magazine with a name and category
        if len(name) < 2 or len(name) > 16:
            raise ValueError("Magazine name must be between 2 and 16 characters")
        if not isinstance(name, str):
            raise ValueError("Magazine name must be a string")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self._name = name  # Set the magazine's name
        self._category = category  # Set the magazine's category
        self._articles = []  # Initialize an empty list to hold the magazine's articles
        Magazine.all.append(self)  # Add this magazine to the global list of magazines

    @property
    def name(self):
        # Get the magazine's name
        return self._name

    @name.setter
    def name(self, value):
        # Allow changing the magazine's name (with validation)
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Magazine name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        # Get the magazine's category
        return self._category

    @category.setter
    def category(self, value):
        # Allow changing the magazine's category (with validation)
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        if value == "":
            raise ValueError("Category cannot be empty")
        self._category = value

    def articles(self):
        # Return a list of all articles in this magazine
        return self._articles

    def contributors(self):
        # Return a list of unique authors who have contributed to the magazine
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        # Return a list of all article titles in this magazine
        return [article.title for article in self._articles] if self._articles else None

    def contributing_authors(self):
        # Return a list of authors who have written more than 2 articles for this magazine
        if not self._articles:
            return None
        authors_count = {}
        for article in self._articles:
            authors_count[article.author] = authors_count.get(article.author, 0) + 1
        contributing_authors = [author for author, count in authors_count.items() if count > 2]
        return contributing_authors if contributing_authors else None

    @classmethod
    def top_publisher(cls):
        # Return the magazine with the most articles published
        if not cls.all:
            return None
        return max(cls.all, key=lambda magazine: len(magazine._articles), default=None)
