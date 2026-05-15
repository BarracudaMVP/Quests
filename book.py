# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from dataclasses import dataclass
import pickle, datetime

class Book:
    def __init__(self):
        self.items = dict()
        self.storage = PickleStorage(self)
        self.maxID = 0
        
    def add(self):
        self.maxID += 1
        item = BookItem(id=self.maxID)
        item.read()
        self.items[item.id] = item

    def write(self):
        for id, item in self.items.items():
            item.write()

    def store(self):
        self.storage.store()

    def load(self):
        self.storage.load()

    def delete(self):
        id = int(input("id: "))
        del self.items[id]

class ConsoleIO:
    def input(self, field, defvalue=None):
        return input(f"{field}: ")
    
    def output(self, title, field):
        print(f"{title}: {field}")

class PickleStorage:
    def __init__(self, book):
        self.book = book
    
    def store(self):
        pickle.dump((self.book.maxID, self.book.items), open("data.dat", "wb"))
        
    def load(self):
        (self.book.maxID, self.book.items) = pickle.load(open("data.dat", "rb"))

@dataclass
class BookItem:
    id: int = 0
    title: str = ""
    body: str = ""
    author: str = ""
    time = 0
    
    def __post_init__(self):
        self.time = datetime.datetime.now()
        self.io = ConsoleIO()
        
    def read(self):
        self.title = self.io.input('title')
        self.body = self.io.input('body')
        self.author = self.io.input('author')
        
    def write(self):
        self.io.output('ID', self.id)
        self.io.output('Title', self.title)
        self.io.output('Body', self.body)
        self.io.output('Author', self.author)
        self.io.output('Time', self.time)
        
        
def main():
    book = Book()
    
    menu = [
        ["Добавить", book.add],
        ["Удалить", book.delete],
        ["Показать", book.write],
        ["Сохранить", book.store],
        ["Загрузить", book.load],
    ]

    while True:
        for i,menuItem in enumerate(menu, 1):
            print(f"{i}. {menuItem[0]}")
        m = int(input())
        menu[m-1][1]()

main()