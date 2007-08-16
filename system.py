#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Convert model number to System Name

import model

def name():
    
    modelname = model.determine_model()
    
    if modelname == "koap1":
        systemname = "Koala Performance"
        return systemname
    elif modelname == "daru1":
        systemname = "Darter Ultra"
        return systemname
    elif modelname == "sabv1":
        systemname = "Sable Series"
        return systemname
    elif modelname == "sabv2":
        systemname = "Sable Series"
        return systemname
    elif modelname == "wilp1":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "ratv1":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "ratv2":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "ratv3":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "gazv2":
        systemname = "Gazelle Value"
        return systemname
    elif modelname == "wilp2":
        systemname = "Wild Dog Professional"
        return systemname
    elif modelname == "wilp3":
        systemname = "Wild Dog Professional"
        return systemname
    elif modelname == "gazv1":
        systemname = "Gazelle Value"
        return systemname
    elif modelname == "gazv3":
        systemname = "Gazelle Value"
        return systemname
    elif modelname == "gazv4":
        systemname = "Gazelle Value"
        return systemname
    elif modelname == "gazp1":
        systemname = "Gazelle Performance"
        return systemname
    elif modelname == "gazp2":
        systemname = "Gazelle Performance"
        return systemname
    elif modelname == "gazp3":
        systemname = "Gazelle Performance"
        return systemname
    elif modelname == "panv2":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "serp1":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "serp2":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "bonp1":
        systemname = "Bonobo Performance"
        return systemname
    elif modelname == "panv1":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "koav1":
        systemname == "Koala Value"
        return systemname
    else:
        modelname = "nonsystem76"
        return modelname