from bottle import *
from bottle import static_file
from markdown import markdown
import os, stat, json, shutil

markdown_options =['extra']

@route('/css/<path:path>')
def server_static(path):
    return static_file(path, root='css')

@route('/js/<path:path>')
def server_static(path):
    return static_file(path, root='js')

@route('/img/<path:path>')
def server_static(path):
    return static_file(path, root='document/img')

@post('/convert')
def convert():
    return markdown(request.forms.get('content','').decode('utf-8'),markdown_options)

@post('/save')
def save():
    filename = request.forms.get('filename','')
    content = request.forms.get('content','')
    if not filename:
        return
    filename = os.path.basename(filename)
    if not filename.lower().endswith('.md'):
        filename+='.md'
    with file('document/'+filename,'w') as f:
        f.write(content)
        print 'OK'

def rmtree(path):
    if not os.path.isdir(path):
        return
    try:
        names = os.listdir(path)
        for name in names:
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                rmtree(fullname)
            else:
                os.chmod(fullname, stat.S_IWRITE)
                os.remove(fullname)
        os.chmod(path, stat.S_IWRITE)
        os.rmdir(path)
    except:
        print '[ERROR] rmtree()'

@post('/savehtml')
def savehtml():
    filename = request.forms.get('filename','')
    content = request.forms.get('content','').decode('utf-8')
    if not filename:
        return
    filename = os.path.basename(filename)
    if filename.lower().endswith('.md'):
        filename = filename[:-3]
    tpl = file('views/tmp.html').read()
    html = tpl.replace('{{title}}',filename).replace('{{content}}',markdown(content,markdown_options))
    rmtree('document/html') # shutil.rmtree BU KAO PU
    os.mkdir('document/html')
    with file('document/html/index.html','w') as f:
        f.write(html.encode('utf-8'))
    if os.path.isdir('document/img/'+filename):
        os.mkdir('document/html/img')
        shutil.copytree('document/img/'+filename, 'document/html/img/'+filename)

@post('/allmd')
def allmd():
    fl = os.listdir('document')
    fl = filter(lambda fn: fn.lower().endswith('.md'), fl)
    return json.dumps(fl)

@post('/load')
def load():
    filename = request.forms.get('filename','')
    if not filename: return
    filename = os.path.basename(filename)
    filename = 'document/' + filename
    if not filename.lower().endswith('.md'):
        filename+='.md'
    if os.path.isfile(filename):
        return file(filename).read()

@route('/')
def note():
    return template('note.html')

debug(True)
run(host='0.0.0.0',port=8901,reloader=True)
