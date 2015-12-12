import os

os.system("sudo pip install dpkt")

os.system("sudo pip install pygeoip")

os.system("gunzip -k GeoIP.dat.gz")
os.system("sudo mkdir /opt/GeoIP")
os.system("sudo mv GeoIP.dat /opt/GeoIP")
os.system("sudo mv /opt/GeoIP/GeoIP.dat /opt/GeoIP/Geo.dat")

#Fin.