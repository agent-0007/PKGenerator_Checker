#!/usr/bin/env python3

import time
import logging
import requests
from lxml import html
from random import randint


iterating = 0
napLength = 3 # time in seconds to sleep for
iterLimits = 1000 # how many API lookups till we take a Nap

from smtplib import SMTP_SSL as SMTP
from time import sleep

host        = "smtp.ymail.com" 
usrnme      = "myemail@yahoomail.com" 
pswd        = "myFancyPantsPasswording"
subject = "check this private key pls"

def send_email(from_addr, to_addr, body_text):
    """
    Send an Email
    """

    msg_body = ""
    parts = ["From: %s" % from_addr,
            "To: %s" % to_addr,
            "MIME-Version: 1.0",
            "Content-type: text/html",
            "Subject: %s" % subject,
            "",
            body_text
            , "\r\n"]
    msg_body = "\r\n".join(parts)
    server = SMTP(host, 465)
    # server.set_debuglevel(1)
    server.ehlo()
    server.login(usrnme,pswd)
    server.sendmail(from_addr, to_addr, msg_body)
    server.quit()



def generatePage():
    return randint(0,904625697166532776746648320380374280100293470930272690489102837043110636675)



def grabPks(pageNum):
    req = requests.get("https://directory.io/"+str(pageNum))
        tree = html.fromstring(req.text)
        pk = tree.xpath("//*[@id]/span[1]//text()")
    resCmpress = tree.xpath("//*[@id]/a[3]//text()")
    resXtend = tree.xpath("//*[@id]/a[2]//text()")
    return pk, resCmpress, resXtend


while True:
    pkArray = grabPks(generatePage())
    for i in range(len(pkArray[0])):
        if (iterating >= iterLimits):
            print("taking a {0} second Nap..ZZZzzzzz".format(napLength))
            time.sleep(napLength)
            iterating = -1
        iterating +=1
        resCmp = requests.get("https://blockchain.info/q/addressbalance/" +str(pkArray[1][i]))
        endCmp =  resCmp.text
        resXnd = requests.get("https://blockchain.info/q/addressbalance/" +str(pkArray[2][i]))
        endExt =  resXnd.text
        if "Illegal character   at position" not in endCmp:

        if endCmp != "0" :
            print ("endCmp = " + endCmp)
            print("We may have found something! check out Private Key {0}, for compressed Address {1}".format(pkArray[0][i], pkArray[1][i]))
            send_email("myemail@gmail.com", "myemail@gmail.com", "check out Private Key {0}, for Adress {1}, and {2}".format(pkArray[0][i], pkArray[1][i], pkArray[2][i] ))
            raise SystemExit


    if "Illegal character   at position" not in endExt:

        if endExt != "0" :
            print ("endExt = " + endExt)
            print("We may have found something! check out Private Key {0}, for extended Address {1}".format(pkArray[0][i], pkArray[2][i]))
            send_email("myemail@gmail.com", "myemail@gmail.com", "check out Private Key {0}, for Adress {1}, and {2}".format(pkArray[0][i], pkArray[1][i], pkArray[2][i] ))
            raise SystemExit

    print ("Ext: {0}, Stndrd {1}".format(endExt, endCmp))


''' HEY THERE PIRATE!

THIS IS A 2017 FACELIFT TO THE TOY APP POOR MANS MINING.
HUNT THEM 2010 ERA COINS!!!!  Currently the Script uses Directory.IO
and blockchain.info to parse (at random) the entire sha256 keylist page by page
256 different lookups per page (1 for compressesed public address one for standard.
Feel Free to checkout Line 63 IF YOU REALLY WANT TO KNOW HOW BIG THIS IS...
and impractical mind you!  This script may be your friend if you - can setup
and distribute this, like a botnet so that its scanning all the time from different
machines and ultimately pinging you on anything found.  You are literally stealing
someone else's private key - if the BTC utxo's are OLD like 2010 old you may be
able to comformably claim those - if the funds are a couple months old however,
you may need to consider returning a large portion if not all of them back to the
rightful owner.  Just like with my PK generator/checker tool this is literally for
enteratinment purposes and not designed for extended real world use.  Your IP
Address may become blocked from using this toy extensively, proceed with caution.
If you DO actually happen to find a collision (ie someone else's private key),
pat yourself on the back because that's supposed to not be possible...and maybe
send a few duckets my way: 18ZVx4i7FKYj6GYa1XgBM2ZfQdjE6nUMgt

'''
