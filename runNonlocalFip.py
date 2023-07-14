
def runNonlocalFip():

    import os
    import time

    from nonlocalFIP import nonlocalFIP
    from nonlocalFIPWeight import nonlocalFIPWeight
    from dictionary import thisdict

    isWeight = thisdict["isWeight"]

    if isWeight == True:
        nonlocalFIPWeight()
    else:
        nonlocalFIP()

