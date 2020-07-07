'''
@date: 7th July 20202
@author: Sonali Kashyap
RUN: python webserver_v3.py
Go to: http://localhost:8000/tasklist
'''
###

#from flask import Flask
#from flask_restful import Resource, Api, reqparse
#app = Flask(__name__)
#api = Api(app)


class recruiter(Resource):
  global dfj, dfc
  def get(self):
    return 'Enter <Recruiter ID>:'
  
  def post(self):
    parser.add_argument("id")
    args = parser.parse_args()
    df = dfj.loc[dfj['AGENT']==args["id"],['REQID','CREATE_DAY','JOB_CATEGORY']]
    return df.to_json(),201
class candidates(Resource):
  global dfj, dfc
  def get(self):
    parser.add_argument("req_id") 
    args = parser.parse_args()
    df = dfc.loc[dfc['REQID']==args["req_id"]]
    return df.to_json()

  def test(self):
    parser.add_argument("req_id")
    args = parser.parse_args()
    df = dfc.loc[dfc['REQID']==args["req_id"],['CANDID','STATE']]
    print(df['CANDID'].unique())
    df = df[['CANDID','STATE']].groupby(['STATE']).agg(['count'])
    return df.to_json()

  def post(self):
    parser.add_argument("req_id")
    args = parser.parse_args()
    df = dfc.loc[dfc['REQID']==args["req_id"]]
    cand = df['CANDID'].unique()
    df_alt = dfc.loc[dfc['CANDID'].isin(cand)]
    df = df_alt[['REQID','CANDID','STATE']].groupby(['CANDID','STATE']).agg(['count'])
    return df.to_json()

# endpoints      
#api.add_resource(recruiter, '/recruiter/')
#api.add_resource(candidates, '/candidates/')
parser = reqparse.RequestParser()


  
#app.run(debug=True)
###
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi 
#cgi -> common gateway interface helps to process user input submitted for a HTML form 
# HTTPServer -> specify port
# BaseHTTPRequestHandler-> Handle GET/POST requests

import csv
import pandas as pd

tasklist = ['Task 1','Task 2','Task 3' ]

class requestHandler(BaseHTTPRequestHandler): 
    '''
    Class getHandler inherits from BaseHTTPRequestHandler class
    Add Tasks to the server and delete tasks
    '''

    def do_GET(self):

        if self.path.endswith('/tasklist'):
            self.send_response(200) #send back a response
            self.send_header('content-type', 'text/html') 
            self.end_headers() # always close headers
            # setup content to page
            #self.wfile.write('Welcome to the web app!'.encode()) #wfile --> writable file write to the page
            #self.wfile.write(self.path[1:].encode())
            # cant send strings on http requests so encode method encodes the string into bytes and then it is served up on the webpage as a string

            #output tasklist to the browser window
            output = ''
            output += '<html><body>'
            output += '<h1>TASK LIST</h1>'

            # Create a page in our server to add a new task
            # Add link to a new page
            output += '<h3><a href="/tasklist/new">Add New Task</a></h3>'



            # loop to iterate through all the tasks
            for task in tasklist:
                output += task
                # Adding a remove functionality to a server/ task  when completed
                output += '<a/ href="/tasklist/%s/remove">X</a>'% task
                output += '</br>'
            output += '</body></html>'
            # writing the o/p to the browser window
            self.wfile.write(output.encode())

        # handling get request with new at the end of the address path
        if self.path.endswith('/new'):
            self.send_response(200) #send back a response
            self.send_header('content-type', 'text/html') 
            self.end_headers() # always close headers

            output = ''
            output += '<html><body>'
            output += '<h1>Add New Task</h1>'

            output += '<form method ="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="task" type="text" placeholder="Add new task">'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'
        
            self.wfile.write(output.encode())

        # handling get request with remove at the end of the address path
        if self.path.endswith('/remove'): 
            # Getting the task list id for the particular task
            listIDPath = self.path.split('/')[2] # split the path by '/': forward slash
            #print(listIDPath)
            self.send_response(200) #send back a response
            self.send_header('content-type', 'text/html') 
            self.end_headers() # always close headers

            output = ''
            output += '<html><body>'
            output += '<h1>Remove Task: %s</h1>' % listIDPath.replace('%20',' ')
            output += '<form method ="POST" enctype="multipart/form-data" action="/tasklist/%s/remove">' %listIDPath
            output += '<input type="submit" value="Remove">'
            output += '</form>'
            output += '<a href="/tasklist">Cancel</a>'
            
            output += '</body></html>'
        
            self.wfile.write(output.encode())



    def do_POST(self):
        if self.path.endswith('/new'):
            # get content type and a dict of content type parameters
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            # ctype : Scans the post methos and checks for content type in the enctype: multipart/form-data
            # we get a boundary key within the form which gives us a dictionary parameter 
            # to meet the boundary and allows the server to separate the values provided within the form
            #pdict --> primitive dict
            pdict['boundary'] = bytes(pdict['boundary']).encode("utf-8")
            # Content length of the submitted POST
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len

            if ctype == 'multipart/form-data':
                #To get each individual fields of the form
                fields = cgi.parse_multipart(self.rfile, pdict)
                # rfile->read the file
                new_task = fields.get('task')

                #append the task to the list
                tasklist.append(new_task[0])

            self.send_response(301) # redirect requst to /task list main page where all the tasks are listed 
            self.send_header('content-type', 'text/html') 
            self.send_header('Location', '/tasklist')
            self.end_headers() # always close headers


        # For remove functionality to work
        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            # Passing form submission to get content type and a dict of content type parameters
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            
            if ctype == 'multipart/form-data':
                list_item = listIDPath.replace('%20',' ')
                tasklist.remove(list_item)

            self.send_response(301) # redirect requst to /task list main page where all the tasks are listed 
            self.send_header('content-type', 'text/html') 
            self.send_header('Location', '/tasklist')
            self.end_headers() # always close headers

    def loadData():
        filename ="downloads/jobData.csv"
        # opening the file using "with"  
        # statement 
        dfj = pd.read_csv(filename)
        #filename ="C:/Users/MUNISHGOYAL/Box Sync/Projects/Providence/annonymized/candData2.csv"
        filename ="downloads/candData2.csv" 
        dfc = pd.read_csv(filename)
        dfc.columns = ['REQID', 'CANDID','DAYS','STATE']
        return dfj,dfc

            
def main():
    '''
    It is going instantiate actual port 
    and create a server
    '''
    PORT = 8000
    server = HTTPServer(('',PORT), requestHandler) #instance of the HTTPServer class 
    # 1st arg: --(hostName,PORT)
    # 2nd arg: --(requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever() # Server will keep running until stopped by control+C in tertminal
    dfj,dfc= loadData()

if __name__ == '__main__':
    '''
    If name = main then the file is not being run as an imported module
    '''
    main()
    