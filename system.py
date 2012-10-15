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
    elif modelname == "daru2":
        systemname = "Darter Ultra"
        return systemname
    elif modelname == "daru3":
        systemname = "Darter Ultra"
        return systemname
    elif modelname == "lemu1":
        systemname = "Lemur UltraThin"
        return systemname
    elif modelname == "lemu2":
        systemname = "Lemur UltraThin"
        return systemname
    elif modelname == "lemu3":
        systemname = "Lemur Ultra"
        return systemname
    elif modelname == "lemu4":
        systemname = "Lemur Ultra"
        return systemname
    elif modelname == "leo1":
        systemname = "The Leopard Extreme"
        return systemname
    elif modelname == "leox2":
        systemname = "The Leopard Extreme"
        return systemname
    elif modelname == "leox3":
        systemname = "The Leopard Extreme"
        return systemname
    elif modelname == "ment1":
        systemname = "Meerkat NetTop"
        return systemname
    elif modelname == "ment2":
        systemname = "Meerkat Ion NetTop"
        return systemname
    elif modelname == "ment3":
        systemname = "Meerkat NetTop"
        return systemname
    elif modelname == "ment5":
        systemname = "Meerkat Ion NetTop"
        return systemname
    elif modelname == "star1":
        systemname = "Starling NetBook"
        return systemname
    elif modelname == "star2":
        systemname = "Starling EduBook"
        return systemname
    elif modelname == "star3":
        systemname = "Starling NetBook"
        return systemname
    elif modelname == "star4":
        systemname = "Starling NetBook"
        return systemname
    elif modelname == "star5":
        systemname = "Starling NetBook"
        return systemname
    elif modelname == "sabv1":
        systemname = "Sable Series"
        return systemname
    elif modelname == "sabv2":
        systemname = "Sable Series"
        return systemname
    elif modelname == "sabv3":
        systemname = "Sable Series"
        return systemname
    elif modelname == "wilp1":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilp5":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilp6":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilp7":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilp8":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilp9":
        systemname = "Wild Dog Performance"
        return systemname
    elif modelname == "wilb1":
        systemname = "Wildebeest Performance"
        return systemname
    elif modelname == "wilb2":
        systemname = "Wildebeest Performance"
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
    elif modelname == "ratv4":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "ratv5":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "ratv6":
        systemname = "Ratel Value"
        return systemname
    elif modelname == "ratu1":
        systemname = "Ratel Ultra"
        return systemname
    elif modelname == "ratu2":
        systemname = "Ratel Ultra"
        return systemname
    elif modelname == "ratp1":
        systemname = "Ratel Performance"
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
    elif modelname == "gazv5":
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
    elif modelname == "gazp5":
        systemname = "Gazelle Value with nVidia and Camera"
        return systemname
    elif modelname == "gazp6":
        systemname = "Gazelle Professional"
        return systemname
    elif modelname == "gazp7":
        systemname = "Gazelle Professional"
        return systemname
    elif modelname == "gazp8":
        systemname = "Gazelle Professional"
        return systemname
    elif modelname == "gazu1":
        systemname = "Gazelle Ultra"
        return systemname
    elif modelname == "meec1":
        systemname = "Meerkat Compact"
        return systemname
    elif modelname == "panv2":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "panv3":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "serp1":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "serp2":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "serp3":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "serp4":
        systemname = "Serval Performance"
        return systemname
    elif modelname == "serp5":
        systemname = "Serval Professional"
        return systemname
    elif modelname == "serp6":
        systemname = "Serval Professional"
        return systemname
    elif modelname == "serp7":
        systemname = "Serval Professional"
        return systemname
    elif modelname == "bonp1":
        systemname = "Bonobo Performance"
        return systemname
    elif modelname == "bonp2":
        systemname = "Bonobo Professional"
        return systemname
    elif modelname == "bonp3":
        systemname = "Bonobo Performance"
        return systemname
    elif modelname == "bonp4":
        systemname = "Bonobo Professional"
        return systemname
    elif modelname == "bonp5":
        systemname = "Bonobo Professional"
        return systemname
    elif modelname == "panp4i":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp4n":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp5":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp6":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp7":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp8":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panp9":
        systemname = "Pangolin Performance"
        return systemname
    elif modelname == "panv1":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "panv2":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "panv3":
        systemname = "Pangolin Value"
        return systemname
    elif modelname == "koav1":
        systemname == "Koala Value"
        return systemname
    else:
        modelname = "nonsystem76"
        return modelname
