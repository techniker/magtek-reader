#!/usr/bin/python
"""
Bjoern Heller <tec@codeburn.de> (c) 2012
Code will be placed under public domain
 
MagTek USB magnetic-swipe-reader
Forked from: Copyright (c) 2010 - Micah Carrick - http://www.micahcarrick.com/credit-card-reader-pyusb.html
"""
import sys
import usb.core
import usb.util

#USB ID def
VENDOR_ID = 0x0801
PRODUCT_ID = 0x0002
DATA_SIZE = 329 #datasize of reader output 373

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class MagSwipe:
    def __init__(self):
        # find the MagSwipe reader
        device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

        if device is None:
            sys.exit("No MagTek reader found")

        # make sure the hiddev kernel driver is not active
        if device.is_kernel_driver_active(0):
            try:
                device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                sys.exit("error detatching kernel driver: %s" % str(e))

        # set configuration
        try:
            device.set_configuration()
            device.reset()
        except usb.core.USBError as e:
            sys.exit("error setting configuration: %s" % str(e))

        self._endpoint = device[0][(0,0)][0]

    def wait_for_swipe(self):
        # wait for swipe
        data = []
        swiped = False
        print "Please swipe card..."

        while 1:
            try:
                data += self._endpoint.read(self._endpoint.wMaxPacketSize)
                if not swiped:
                    print "Reading card..."
                swiped = True

            except usb.core.USBError as e:
                if e.args[0] == 110 and swiped:
                    if len(data) < DATA_SIZE:
                        print "Bad swipe, try again. (%d bytes)" % len(data)
                        print "Data: %s" % ''.join(map(chr, data))
			print data #print raw data
                        data = []
                        swiped = False
                        continue
                    else:
			print "Data: %s" % '' .join(map(chr, data))
                        break   # got data

        return data

if __name__ == "__main__":
    print MagSwipe().wait_for_swipe()
