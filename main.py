import dpkt
import socket
import pygeoip
import time

gi = pygeoip.GeoIP('GeoLiteCity.dat')


def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('106.51.137.221')
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

def plotIPs(pcap):
    kmlPts = ''
    print("Parsing all the packets.............")
    time.sleep(5)
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src)
            kmlPts = kmlPts + KML
        except:
            pass
    time.sleep(3)
    return kmlPts

def main():
    file1 = open("data.kml", "a") 
    fileName=input("Enter the name of pcap file: ")
    f = open(f'{fileName}.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    print("Reading the pcap file packets...........")
    time.sleep(5)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    file1.writelines(kmldoc)
    file1.close()
    print("KML file has been created in the current directory and it is named as data.kml")

if __name__ == '__main__':
    main()

