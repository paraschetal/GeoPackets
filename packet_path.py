import dpkt
import socket
def printPcap(pcap):
	for (ts, buf) in pcap:
		try:
			eth=dpkt.ethernet.Ethernet(buf)
			ip=eth.data
			src=socket.inet_ntoa(ip.src)
			dst=socket.inet_ntoa(ip.dst)
			print '[+] Src: '+src+' --> Dst: '+ dst
		except Exception,e :
			pass	
def main():
	f=open('test.pcap')
	pcap=dpkt.pcap.Reader(f)
	printPcap(pcap)
if __name__=='__main__':
	main()
