# -*- coding: utf-8 -*-

from dataclasses import dataclass
import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from flask import render_template
from flask import request

class Book:
    def __init__(self):
        self.storage = PickleStorage(self)
        
          
    def GetHeader(self):
        return render_template('header.tpl')

    def GetFooter(self):
        return render_template('footer.tpl')
        
    def ShowForm(self, id):
        return self.storage.GetItem(id).ShowForm()
        
    def ShowBook(self):
        r = ''
        for item in self.storage.GetItems():
            r += item.Show()
            
        return r + render_template('add.tpl')
        
    def Add(self):
        item = self.storage.GetItem(int( request.form.get('id', 0) ))
        item.SetFormData(request.form)
        self.storage.Add(item);
        return self.ShowBook()
            
    def Delete(self, id):
        self.storage.Delete(id)
        return self.ShowBook()

class PickleStorage:
    def __init__ (self, book):
        self.book = book
        try:
            self.Load()
        except:
            self.items = {}
            self.maxid = 0

    def Load(self):
        with open('book.db', 'rb') as f:
            (self.maxid, self.items) = pickle.load(f)
        
    def Store(self):
        with open('book.db', 'wb') as f:
            pickle.dump((self.maxid, self.items), f)

    def GetItem(self, id):
        if id <= 0:
            return BookItem()
        else:
            return self.items[id]

    def Add(self, item):
        if item.id <= 0:
            self.maxid += 1;
            item.id = self.maxid
            self.items[item.id] = item
            
    def Delete(self, id):
        del self.items[id]
        
    def GetItems(self):
        for(id, item) in self.items.items():
            yield(item)

@dataclass
class BookItem:
    id: int = 0
    title: str = ''
    body: str = ''
    author: str = ''
    time = 0
   
    def __post_init__(self):
        self.time = datetime.datetime.now()

    def Show(self):
        return render_template('item.tpl', **self.__dict__)
    
    def SetFormData(self, form):
        self.id = int(form.get('id'))
        self.title = form.get('title')
        self.body = form.get('body')
        self.author = form.get('author')
    
    def ShowForm(self):
        return render_template('form.tpl', **self.__dict__)

