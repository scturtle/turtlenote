from bottle import *
from bottle import static_file
from markdown import markdown
import os, stat, json

@post('/convert')
def convert():
    return markdown(request.forms.get('content','').decode('utf-8'))

@route('/')
def note():
    return template('note.html')

if __name__=='__main__':
    debug(True)
    run(server='gae')