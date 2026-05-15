# -*- coding: utf-8 -*-

from dataclasses import dataclass
import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def LoadTpl(tpl):
    with open(os.environ['PATH_TRANSLATED']+'/tpl/'+tpl+'.tpl') as f:
        return f.read().replace('{selfurl}', os.environ['SCRIPT_NAME'])

class Book:
    def __init__(self, q):
        self.q = q
        self.storage = PickleStorage(self)
          
    def PrintHeader(self):
        print(LoadTpl('header'))

    def PrintFooter(self):
        print(LoadTpl('footer'))
        
    def ShowForm(self):
        item = self.storage.GetItem(int(self.q.getvalue('id', 0)))
        item.ShowForm()
        
    def ShowBook(self):
        for item in self.storage.GetItems():
            item.Show()
        print(LoadTpl('add'))
        
    def Add(self):
        item = self.storage.GetItem(int(self.q.getvalue('id', 0)))
        item.SetFormData(self.q)
        self.storage.Add(item);
            
    def Delete(self):
        self.storage.Delete((int(self.q.getvalue('id', 0))))

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
        print(LoadTpl('item').format(**self.__dict__))
    
    def SetFormData(self, q):
        self.id = int(q.getvalue('id', 0))
        self.title = q.getvalue('title')
        self.body = q.getvalue('body')
        self.author = q.getvalue('author')
    
    def ShowForm(self):
        print(LoadTpl('form').format(**self.__dict__))

def main():
    q = cgi.FieldStorage()
    book = Book(q)
    
    book.PrintHeader()
    
    MENU = {
        'showform': book.ShowForm,
        'add':      book.Add,
        'delete':   book.Delete
    
    }
    
    try:
        MENU[q.getvalue('type')]()
    except Exception as e:
        print(e, '<br>')
    
    book.ShowBook()
    book.storage.Store()
    book.PrintFooter()
        
        
main()
