""" book_functions.py
    Contains functions to work with Book objects
"""

from Book import Book
from Book import load_books

def get_genres(books:list[Book])->list[str]:
    """Get all unique genres from a list of Book objects"""
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(list(genres))

def create_author_dictionary(books:list[Book])->dict[str,list[Book]]:
    """Create a dictionary of authors and their books"""
    author_dict = {}
    for book in books:
        if book.author.lower() not in author_dict:
            author_dict[book.author.lower()] = []
        author_dict[book.author.lower()].append(book)
        # Multiple names or authors
        author_names = book.author.lower().split(" ")
        if len(author_names) >= 2:
            for name in author_names:   
                if name not in author_dict:
                    author_dict[name] = []
                author_dict[name].append(book)
    return author_dict

def create_book_dictionary(book_list:list)->dict[str,Book]:
    """Create a dictionary of books and their ids"""
    book_dict = {}
    for book in book_list:
        book_dict[book.id] = book
    return book_dict

if __name__ == "__main__":
    books = load_books("booklist2000.csv")
    print(get_genres(books))
    author_dict = create_author_dictionary(books)
    print(author_dict["sandra"][0])