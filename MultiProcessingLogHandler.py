from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import multiprocessing, threading, logging, sys, traceback


class MultiProcessingLogHandler(logging.Handler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, fmt=None):
        logging.Handler.__init__(self)

        self.filename = filename
        self.mode = mode
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.encoding = encoding
        self.delay = delay
        self._handler = None
        self._handler_stream = None
        self.fmt = fmt

        # self._handler = RotatingFileHandler(filename, mode, maxBytes, backupCount, encoding, delay)
        # self._handler_stream = StreamHandler()
        # pool = multiprocessing.Pool()
        m = multiprocessing.Manager()
        self.queue = m.Queue(-1)

        # self.queue = multiprocessing.Queue(-1)

        p = multiprocessing.Process(target=self.receive)
        p.start()
        # t = threading.Thread(target=self.receive)
        # t.daemon = True
        # t.start()

    # def setFormatter(self, fmt):
        # logging.Handler.setFormatter(self, fmt)
        # self._handler.setFormatter(fmt)
        # self._handler_stream.setFormatter(fmt)

    def receive(self):
        self._handler = RotatingFileHandler(self.filename, self.mode, self.maxBytes, self.backupCount, self.encoding, self.delay)
        self._handler_stream = StreamHandler()

        logging.Handler.setFormatter(self, self.fmt)
        self._handler.setFormatter(self.fmt)
        self._handler_stream.setFormatter(self.fmt)

        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
                self._handler_stream.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified.  Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        if self._handler is not None:
            self._handler.close()
        if self._handler_stream is not None:
            self._handler_stream.close()
        logging.Handler.close(self)


# TEST code.
"""
logger = logging.getLogger('logger')
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
fileMaxByte = 1024 * 1024 * 15 # 15MB

multi_handler = MultiProcessingLogHandler.MultiProcessingLogHandler('log.log', maxBytes=fileMaxByte, backupCount=0, encoding='utf-8', fmt=formatter)
logger.addHandler(multi_handler)

# fileHandler = logging.handlers.RotatingFileHandler('log.log', maxBytes=fileMaxByte, backupCount=0, encoding='utf-8')
# streamHandler = logging.StreamHandler()
# fileHandler.setFormatter(formatter)
# logger.addHandler(fileHandler)
# logger.addHandler(streamHandler)

logger.setLevel(logging.DEBUG)
"""