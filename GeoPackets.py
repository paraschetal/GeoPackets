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
			)%(ip,longitude,latitude)
		# print ip
		return kml
	except :
		return ''
def drawLines(srcORdstList):
	linePoints=[]
	count=0
	for i in srcORdstList:
		for j in srcORdstList:
			try:
				if i==j:
					continue
				rec1=gi.record_by_name(i)
				rec2=gi.record_by_name(j)
				
				lat1=rec1['latitude']
				lon1=rec1['longitude']
				lat2=rec2['latitude']
				lon2=rec2['longitude']
				
				linePoint=str(lon1)+','+str(lat1)+','+str(0)+" "+str(lon2)+","+str(lat2)+",0."+'\n'
				# print linePoint+' '+i+' to '+j
				linePoints.append(linePoint)
				# count+=1
			except Exception,e:
				pass
	kml=''
	# print len(linePoints)		
	# print count			
	# kml=('')
	for i in linePoints:
		# print i
		kml+=(
			'<Placemark>\n'
			'<name></name>\n'
			'<LineString>\n'
			'<tessellate>1</tessellate>\n'
			'<coordinates>\n'
			)	
		
		kml+=i
			
		kml+=(	'</coordinates>\n'
				'</LineString>\n'
			 )	
		kml=kml+('<Style>\n'
			'<LineStyle>\n'
			'<width>1</width>\n'
			'<color>#ff0000ff</color>\n'
			'</LineStyle>\n'
			'</Style>\n'
			'</Placemark>\n'
		)				
	return(kml)			
def plotIPs(pcap):
	kmlPts=''
	srcList=[]
	dstList=[]
	srcORdstList=[]
	for (ts,buf) in pcap:
		try:
			eth=dpkt.ethernet.Ethernet(buf)
			ip=eth.data
			
			src=socket.inet_ntoa(ip.src)
			rec=gi.record_by_name(src)
			if src not in srcORdstList and rec['latitude']!=None:
				srcORdstList.append(src)
			# if src not in srcList:
			# 	srcList.append(src)
			dst=socket.inet_ntoa(ip.dst)
			rec=gi.record_by_name(dst)
			if dst not in srcORdstList and rec['latitude']!=None:
				srcORdstList.append(dst)
			# if dst not in dstList:
			# 	dstList.append(dst)

		except:
			pass
	for node in srcORdstList:
		# print node
		kmlPts=kmlPts+retKML(node)
	# my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
	kmlMap=kmlPts+drawLines(srcORdstList)
	for i in srcORdstList:
		rec=gi.record_by_name(i)
		# try:
		# 	print rec['city']+rec['country_name']
		# except:
		# 	print i	
	return kmlMap
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

