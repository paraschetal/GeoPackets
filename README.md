# GeoPackets
>A script that takes a pcap(packet capture) file as input and plots the source and destination of the data packets along with a web joining all the nodes on a KML file which can be then opened by Google Earth/Maps.

## Setup:
* ``` $ sudo python setup.py ```
* Installs all dependencies

## Dependencies (Covered in Setup):
* GeoCityLite database which is an open-source database from MaxMind, Inc. This database correlates registered IP addresses to physical locations. It can be downloaded from [here](http://dev.maxmind.com/geoip/legacy/geolite/). After downloading, uncompress the GeoLiteCity.dat.gz file and move it to the location /opt/GeoIP/Geo.dat
* [pygeoip](https://github.com/appliedsec/pygeoip) library for python which queries the GeoLiteCity database and can be installed using:``` [sudo] pip install pygeoip ```
* [dpkt](https://github.com/kbandla/dpkt) library for python which analyzes data packets. It can be installed using :``` [sudo] pip install dpkt ```

## TODOs:
* ~~Plot lines in the kml file.~~
* ~~Make installation procedure a bit easier.~~


## Usage:

* ``` $ python GeoPackets.py -p <pcap file location> ```

* The KML file gets saved in the current working directory. This file can now be opened by Google Earth and the various source and destination points of the data packets, and the web can be seen.

## Screenshots:
![Screenshot1](/Tested_KMLs/Screenshots/Screenshot1.png? raw=true)
![Screenshot2](/Tested_KMLs/Screenshots/Screenshot2.png? raw=true)
![Screenshot3](/Tested_KMLs/Screenshots/Screenshot3.png? raw=true)







