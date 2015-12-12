# GeoPackets
>A script that takes a pcap file as input and plots the source and destination of the data packets on a KML file which can be then opened by Google Earth/Maps.

## Requirements:
* GeoCityLite database which is an open-source database from MaxMind, Inc. This database correlates registered IP addresses to physical locations. It can be downloaded from [here](http://dev.maxmind.com/geoip/legacy/geolite/). After downloading, uncompress the GeoLiteCity.dat.gz file and move it to the location /opt/GeoIp/Geo.dat
* [pygeoip](https://github.com/appliedsec/pygeoip) library for python which queries the GeoLiteCity database and can be installed using:``` [sudo] pip install pygeoip ```
* [dpkt](https://github.com/kbandla/dpkt) library for python which analyzes data packets. It can be installed using :``` [sudo] pip install dpkt ```

## TODOs:
* If the source has an Unregistered IP, then mark the current location of the computer.
* Plot lines in the kml file joining source to desination(with arrowheads)
* Make installation procedure a bit easier.


## Usage:

* ``` $ python GeoPackets.py -p <pcap file location> ```

* The KML file gets saved in the current working directory. This file can now be opened by Google Earth and the various source and destination points of the data packets can be seen.

## Screenshots:
![Screenshot1](/Tested_KMLs/Screenshots/Selection_018.png? raw=true)
![Screenshot2](/Tested_KMLs/Screenshots/Selection_019.png? raw=true)
![Screenshot3](/Tested_KMLs/Screenshots/Selection_016.png? raw=true)
![Screenshot4](/Tested_KMLs/Screenshots/Selection_017.png? raw=true)






