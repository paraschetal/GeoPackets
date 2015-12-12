import os

os.system("sudo pip install dpkt")

os.system("sudo pip install pygeoip")

os.system("gunzip -k GeoLiteCity.dat.gz")
os.system("sudo mkdir /opt/GeoIP")
os.system("sudo mv GeoLiteCity.dat /opt/GeoIP")
os.system("sudo mv /opt/GeoIP/GeoLiteCity.dat /opt/GeoIP/Geo.dat")

#Fin.