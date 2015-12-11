import dpkt, socket, pygeoip, optparse
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')
def retKML(ip):
	rec=gi.record_by_name(ip)
	try:
		latitude=rec['latitude']
		longitude=rec['longitude']
		kml=(
			'<Placemark>\n'
			'<name>%s</name>\n'
			'<Point>\n'
			'<coordinates>%6f,%6f</coordinates>\n'
			'</Point>\n'	
			'</Placemark>\n'
			)%(ip+"("+rec['city']+", "+rec['country_name']+")",longitude,latitude)
		return kml
	except:
		return ''
def plotIPs(pcap):
	kmlPts=''
	srcList=[]
	dstList=[]
	for (ts,buf) in pcap:
		try:
			eth=dpkt.ethernet.Ethernet(buf)
			ip=eth.data
			src=socket.inet_ntoa(ip.src)
			if src not in srcList:
				srcList.append(src)
			dst=socket.inet_ntoa(ip.dst)
			if dst not in dstList:
				dstList.append(dst)
		except:
			pass
	for srcs in srcList:
		kmlPts=kmlPts+retKML(srcs)		
	for dsts in dstList:
		kmlPts=kmlPts+retKML(dsts)	
	return kmlPts
def main():
	parser=optparse.OptionParser('usage%prog -p ,pcap file.')
	parser.add_option('-p', dest='pcapFile' ,type='string', help='specify pcap filename')
	(options, args)=parser.parse_args()
	if options.pcapFile==None:
		print parser.usage
		exit(0)
	pcapFile=options.pcapFile
	f=open(pcapFile)
	pcap=dpkt.pcap.Reader(f)
	kmlheader='<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.0"> <Document>\n'
	kmlfooter='</Document>\n</kml>\n'
	kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
	pcapFile=pcapFile.strip(".pcap").strip("pcap/")
	kmlFile=open(pcapFile+'.kml', 'w+')
	kmlFile.write(kmldoc)
	kmlFile.close()

if __name__=='__main__':
	main()

