#-*- coding:utf-8 -*-
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

import cgi
import json
from utils import *
import MCTS
from randomNetwork import RandomNetwork

class MCTSHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            game = None
            wait_time = 2
            if "board" in data:
                board, player = Othello.str_to_board(data["board"][0])
                game = Othello(board=board, player=player)
                # print ("Game board received. Player = " + player + ", board:")
                # print (Othello.print_board(board))
            else:
                self.send_error(415, "No value named 'board'.")
                return

            if "wait_time" in data:
                wait_time = int(data["wait_time"][0])
            mcts = MCTS.MCTS(prior_prob=RandomNetwork(), rollout_policy=RandomNetwork(), seconds_per_move=wait_time)
            move = mcts.suggest_move(game)
            # print ("move: " + str(move))
            return_data = json.dumps({'move': move})
        else:
            self.send_error(415, "Only application/x-www-form-urlencoded data is supported.")
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(return_data)

PORT = 8888

httpd = HTTPServer(("", PORT), MCTSHandler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()
