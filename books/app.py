import csv
import os
from flask import Flask, render_template, request
from Book import Book, load_books 
from book_functions import create_author_dictionary, create_book_dictionary

app = Flask(__name__)

import os
filename = os.path.join(
    r"C:\Users\Usuario\OneDrive - Universidad de Sonora\Escritorio\Actividades_escuela\Desarrollo4\books",
    "booklist2000.csv"
)
books = load_books(filename)
book_dict = create_book_dictionary(books)
author_dict = create_author_dictionary(books)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_by_author', methods=['GET', 'POST'])
def search_by_author():
    if request.method == 'POST':
        author = request.form['author']
        books_list = author_dict.get(author.lower(), [])
        return render_template('search_by_author.html', books_list=books_list)
    else:
        return render_template('search_by_author.html', books_list=books[:10])

@app.route('/book/<str:book_id>')
def book_detail(book_id):
    book = book_dict.get(book_id)
    print(book)
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)