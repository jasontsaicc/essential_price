import os
import sys

sys.path.insert(0, os.getcwd())
print(sys.path.insert(0, os.getcwd()))
from tgi102_flask import create_app

# Create an application instance that web servers can use. We store it as
# "application" (the wsgi default) and also the much shorter and convenient
# "app".
app = create_app()
