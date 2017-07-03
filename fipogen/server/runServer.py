# -*- coding: utf-8 -*-

from docopt import docopt
import logging
from logging.handlers import RotatingFileHandler
from server import runServer


usage = """
FiPoGen
Run the web server

Usage:
  runServer.py -h | --help
  runServer.py [options] [--debug]

Options:
  -h --help                    Show this screen.
  -p PORT --port=PORT          web server port [default: 8080].
  -H HOST --host=HOST          Server host [default: localhost].
  -C PATH --cache=PATH         Cache path [default: cache/]
  -G PATH --generated=PATH     Generated files path [default: ../Generated/LaTeX/] 
  --debug                      Debug mode (clear caches, log and display everything)
"""


if __name__ == "__main__":

	# parse the command line
	args = docopt(usage)
	args['--port'] = int(args['--port'])
	debug = '--debug' in args       # True when debug mode

	# Create and setup the logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG if debug else logging.WARNING)

	# add an handler to redirect the log to a file (1Mo max)
	file_handler = RotatingFileHandler('activity.log', mode='a', maxBytes=1e6, backupCount=1)
	file_handler.setLevel(logging.DEBUG)
	file_formatter = logging.Formatter('%(asctime)s [%(name)s] | %(message)s', "%m/%d %H:%M:%S")
	file_handler.setFormatter(file_formatter)
	logger.addHandler(file_handler)

	# Start !
	logger.info("")
	logger.info("#============================#")
	logger.info("# running FiPoGen web server #")
	logger.info("#============================#")
	logger.info("")
	runServer(args['--host'], args['--port'], debug, args['--cache'], args['--generated'])





