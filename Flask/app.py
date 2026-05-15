from dataclasses import dataclass
import os, sys, re, codecs, binascii, datetime, pickle

from book import Book
from book import BookItem
from flask import Flask
from flask import render_template
from flask import g

app = Flask(__name__)

def GetBook():
    if 'book' not in g:
        g.book = Book()
    return g.book

@app.route("/")
def bookindex():
    return GetBook().GetHeader() + GetBook().ShowBook() + GetBook().GetFooter()

@app.route("/showform/<int:id>")
def showform(id):
    return GetBook().GetHeader() + GetBook().ShowForm(id) + GetBook().GetFooter()

@app.route("/delete/<int:id>")
def deleteitem(id):
    return GetBook().GetHeader() + GetBook().Delete(id) + GetBook().GetFooter()

@app.route("/add", methods=['POST'])
def add():
    return GetBook().GetHeader() + GetBook().Add() + GetBook().GetFooter()

@app.teardown_appcontext
def teardown_book(ctx):
    GetBook().storage.Store()

if __name__ == "__main__":
    app.run(debug=True)