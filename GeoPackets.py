import dpkt
import socket
import pygeoip
import optparse

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')


def retKML(ip):  # Plots each point on the kml file
    rec = gi.record_by_name(ip)
    try:
        latitude = rec['latitude']
        longitude = rec['longitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<Point>\n'
            '<coordinates>%6f,%6f</coordinates>\n'
            '</Point>\n'
            '</Placemark>\n'
        ) % (ip, longitude, latitude)

        return kml
    except:
        return ''


# Joins all the points among themselves with red color path representing
# the web
def drawLines(srcORdstList):
    linePoints = []
    count = 0
    for i in srcORdstList:
        for j in srcORdstList:
            try:
                if i == j:
                    continue
                rec1 = gi.record_by_name(i)
                rec2 = gi.record_by_name(j)

                lat1 = rec1['latitude']
                lon1 = rec1['longitude']
                lat2 = rec2['latitude']
                lon2 = rec2['longitude']

                linePoint = str(lon1) + ',' + str(lat1) + ',' + str(0) + \
                    " " + str(lon2) + "," + str(lat2) + ",0." + '\n'
                linePoints.append(linePoint)
            except Exception as e:
                pass

    kml = ''

    for i in linePoints:

        kml += (
            '<Placemark>\n'
            '<name></name>\n'
            '<LineString>\n'
            '<tessellate>1</tessellate>\n'
            '<coordinates>\n'
        )

        kml += i

        kml += (	'</coordinates>\n'
                 '</LineString>\n'
                 )
        kml = kml + ('<Style>\n'
                     '<LineStyle>\n'
                     '<width>1</width>\n'
                     '<color>#ff0000ff</color>\n'
                     '</LineStyle>\n'
                     '</Style>\n'
                     '</Placemark>\n'
                     )
    return(kml)


def plotIPs(pcap):  # parses the pcap file to get all IP addresses and calls the retKML and the drawLine function to plot the kml file
    kmlPts = ''
    srcList = []
    dstList = []
    srcORdstList = []
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            src = socket.inet_ntoa(ip.src)
            rec = gi.record_by_name(src)
            if src not in srcORdstList and rec['latitude'] != None:
                srcORdstList.append(src)
            dst = socket.inet_ntoa(ip.dst)
            rec = gi.record_by_name(dst)
            if dst not in srcORdstList and rec['latitude'] != None:
                srcORdstList.append(dst)
        except:
            pass
    for node in srcORdstList:
        kmlPts = kmlPts + retKML(node)
    kmlMap = kmlPts + drawLines(srcORdstList)
    for i in srcORdstList:
        rec = gi.record_by_name(i)
    return kmlMap


def main():
    parser = optparse.OptionParser('usage%prog -p ,pcap file.')
    parser.add_option(
        '-p',
        dest='pcapFile',
        type='string',
        help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile is None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.0"> <Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc = kmlheader + plotIPs(pcap) + kmlfooter
    pcapFile = pcapFile.strip(".pcap").strip("pcap/")
    kmlFile = open(pcapFile + '.kml', 'w+')
    kmlFile.write(kmldoc)
    kmlFile.close()


if __name__ == '__main__':
    main()
