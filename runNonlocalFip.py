import os
import time

from nonlocalFIP import nonlocalFIP
from nonlocalFIPWeight import nonlocalFIPWeight

isWeight = True

if isWeight == True:
    nonlocalFIPWeight()
else:
    nonlocalFIP()
