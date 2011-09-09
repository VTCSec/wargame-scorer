import services
from services import *

print len(services.Service.plugins)
for p in services.Service.plugins:
    print p.name

http = services.Service.get_plugin('http')

