from datetime import datetime
import sys

DEBUG = True
DEBUG_ALL = True # subtexts
def log(str,sub=''):
  if DEBUG_ALL or (DEBUG and (len(sub)==0)):
    print "[%s] <%s>%s %s"%(datetime.now().time().isoformat(),sys._getframe(1).f_code.co_name,sub,str)