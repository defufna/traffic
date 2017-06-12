#!/usr/bin/env python3

# This file is part of Traffic.
#
# Traffic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Traffic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Traffic.  If not, see <http://www.gnu.org/licenses/>.

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import threading
import sys

status = 0
lock = threading.Lock()

class TrafficHTTPServer(SimpleHTTPRequestHandler):
    def __init__(self, *args):
        SimpleHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        if self.path == "/status":
            self.get_status()
            return
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == "/toggle":
            lock.acquire()
            global status
            status = (status + 1) % 2
            lock.release()
            self.get_status()
        else:
            SimpleHTTPRequestHandler.do_POST(self)


    def get_status(self):
        content = str(status)

        self.protocol_version='HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()

        self.wfile.write(bytes(content, 'utf8'))

def main():
    port = 8000 if len(sys.argv) == 1 else int(sys.argv[1])
    os.chdir("./content")
    print("Serving on {0}".format(port))
    server = HTTPServer(('', port), TrafficHTTPServer)
    server.serve_forever()

if __name__ == "__main__":
    main()
