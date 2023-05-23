import os

if os.environ['DEV_FLAG'] == 'True':
    from .dev import *
else:
    from .prod import *