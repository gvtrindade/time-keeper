import os

if bool(os.environ['DEV_FLAG']) == True:
    from .dev import *
else:
    from .prod import *