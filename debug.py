from datetime import datetime
import sys

DEBUG = True
DEBUG_ALL = False # subtexts
def log(str,sub=''):
  if DEBUG_ALL or (DEBUG and (len(sub)==0)):
    fcn_name = sys._getframe(1).f_code.co_name
    if 'self' in sys._getframe(1).f_locals:
      class_name = sys._getframe(1).f_locals["self"].__class__
    else:
      class_name = "<unknown class>"
    print "[%s] <%s>%s %s"%(datetime.now().time().isoformat(),fcn_name,sub,str)