# Author:Sarah Shi
from flask import Flask,render_template,abort
import os
import json

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

#files_path='../files'

class Files:
    directory=os.path.normpath(os.path.join(
        os.path.dirname(__file__),'..','files'))

    def __init__(self):
        self._files=self._read_all_files()

    def _read_all_files(self):
        result={}
        for filename in os.listdir(self.directory):
            file_path=os.path.join(self.directory,filename)
            with open(file_path) as f:
                result[filename[:-5]]=json.load(f)
        return result

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self,filename):
        return self._files.get(filename)

files=Files()

@app.route('/')
def index():
    return render_template('index.html',title=files.get_title_list())
    # ??? /home/shiyanlou/files/ ????? json ???? `title` ????


@app.route('/files/<filename>')
def file(filename):
    file_item=files.get_by_filename(filename)
    if not file_item:
        abort(404)   #??404???flask???????
    print(file_item)
    return render_template('file.html',item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
    # ????? filename.json ??????
    # ?? filename='helloshiyanlou' ????? helloshiyanlou.json ????
    # ?? filename ???????????? `shiyanlou 404` 404 ????



if __name__=='__main__':
    app.run(host='127.0.0.1',port=3000,debug=True)
    #flask run --port 3000
