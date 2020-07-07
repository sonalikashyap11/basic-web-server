'''
@date: 7th July 20202
@author: Sonali Kashyap
RUN: python webserver.py 
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
# HTTPServer -> specify port
# BaseHTTPRequestHandler-> Handle GET/POST requests

class echoHandler(BaseHTTPRequestHandler): 
    '''
    Class getHandler inherits from BaseHTTPRequestHandler class
    Handle all the GET requests that the server recieves
    '''
    def do_GET(self):
        self.send_response(200) #send back a response
        self.send_header('content-type', 'text/html') 
        self.end_headers() # always close headers
        # setup content to page
        #self.wfile.write('Welcome to the web app!'.encode()) #wfile --> writable file write to the page
        self.wfile.write(self.path[1:].encode())
        # cant send strings on http requests so encode method encodes the string into bytes and then it is served up on the webpage as a string
def main():
    '''
    It is going instantiate actual port 
    and create a server
    '''
    PORT = 8000
    server = HTTPServer(('',PORT), echoHandler) #instance of the HTTPServer class 
    # 1st arg: --(hostName,PORT)
    # 2nd arg: --(requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever() # Server will keep running until stopped by control+C in tertminal

if __name__ == '__main__':
    '''
    If name = main then the file is not being run as an imported module
    '''
    main()