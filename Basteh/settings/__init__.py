from .base import *

if os.environ.get('env') == 'prod':
   print("hi")
   from .prod import *
else:
   from .dev import *
