import sys
import os
import logging
from datetime import datetime


def write(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error_message = 'Error! Code: {c}, Message, {m}, Type, {t}, File, {f}, Line {line}'.format(c=type(e).__name__, m=str(e), t=exc_type, f=fname, line=exc_tb.tb_lineno)
    print(error_message)


def comment(comment_string):
    print(comment_string)