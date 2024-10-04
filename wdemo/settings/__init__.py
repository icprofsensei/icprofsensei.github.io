from .base import *

# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.environ['myproject'] == 'prod':
   from .production import *
else:
   from .development import *