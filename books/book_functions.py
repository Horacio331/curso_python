"""book_functions.py
Contains functios to work whit Book objects"""

from Book import Book
from Book import load_books

def get_genres(books:list[Book])->list[str]:
    """Get all unique genres from a list of Book objects"""
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(genres)

def create_author_dictionary(books:list[Book])->dict[str, list[Book]]:
    """Create a dictionary with authors as keys and a list of their books as values"""
    author_dict = {}
    for book in books:
        if book.author.lower() not in author_dict:
            author_dict[book.author.lower()] = []
        author_dict[book.author.lower()].append(book)
        # Multiple names or author
        author_names = book.author.lower().split(" ")
        if len(author_names) >= 2:
            for name in author_names:
                if name not in author_dict:
                    author_dict[name] = []
                author_dict[name].append(book)

    return author_dict
if __name__ == "__main__":
    books = load_books("booklist2000.csv")
    print(get_genres(books))
    author_dict = create_author_dictionary(books)
    print(author_dict["sandra"][0].title)