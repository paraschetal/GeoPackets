import os

os.system("sudo pip install dpkt")

os.system("sudo pip install pygeoip")

os.system("gunzip Geo*.dat.gz")
os.system("sudo mkdir /opt/GeoIP")
os.system("sudo mv Geo* /opt/GeoIP")
os.system("cd /opt/GeoIp")
os.system("sudo mv GeoIP.dat Geo.dat")

#Fin.