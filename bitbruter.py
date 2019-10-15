#!/usr/bin/python3
# Coded by anomobb
# Edited by Bronx Anarchy ( Add Compress Adress and Multiprocessing )

import hashlib
import pyperclip
import PySimpleGUI as sg
import random
import multiprocessing
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
import datetime
import bitcoin




print('Starting up...')

sg.ChangeLookAndFeel('Black')
layout =  [
            [sg.Text('Bitcoin bruteforcer - Bitbruter', size=(80,1), font=('Comic sans ms', 20), text_color='red')],
            [sg.Text('This program has been running for... ', size=(30,1), font=('Comic sans ms', 10)),sg.Text('', size=(30,1), font=('Comic sans ms', 10), key='_DATE_')],
            [sg.Image('sco.png', size=(225, 225))],
            [sg.Text('Address: ', size=(9,1), font=('Comic sans ms', 14)), sg.Text('', size=(120,1), font=('Comic sans ms', 14),  key='address')],
            [sg.Text('CAddress: ', size=(9,1), font=('Comic sans ms', 14)), sg.Text('', size=(120,1), font=('Comic sans ms', 14),  key='addressc')],
            [sg.Text('Privatekey: ', size=(9,1), font=('Comic sans ms', 14)), sg.Text('', size=(120,1), font=('Comic sans ms', 14), key= 'private_key')],
            [sg.Button('Exit', button_color=('white', 'red'))]
          ]

window = sg.Window('Bitbruter',
                  layout=layout,
                   default_element_size=(12,1),
                   font='Helvetica 18',
                   )

start_time = datetime.datetime.now()
#private_key = random.randrange(0,115792089237316195423570985008687907852837564279074904382605163141518161494337)
def generate_private_key():
    private_key = random.randrange(0,4)
    return private_key

def pubkey(private_key):
    pubkey = bitcoin.fast_multiply(bitcoin.G, private_key)
    return pubkey

def pubkeyc(private_key):
    pubkey = bitcoin.fast_multiply(bitcoin.G, private_key)
    (pubkey_x, pubkey_y) = pubkey
    if pubkey_y % 2 == 0:
        compressed_prefix = '02'
    else:
        compressed_prefix = '03'
    hexo = compressed_prefix + bitcoin.encode(pubkey_x, 16)
    pubkeyc = hexo.encode('utf-8')
    return pubkeyc   

def addr(pubkey):
   return bitcoin.pubkey_to_address(pubkey)

def addrc(pubkeyc):
   return bitcoin.pubkey_to_address(pubkeyc)   
   

def database(private_key, address, addressc, database):
    with open("data-base", "r") as m:
        add = m.read().split()
        for ad in add:
            continue
        if address in add or addressc in add:

                data = open("Win.txt","a")
                data.write('Private : '+str(bitcoin.encode_privkey(private_key,'hex'))+'\n'+
                           'Address : '+str(address)+'\n'+'cAddress: '+str(addressc) +'\n\n')
                data.close()


def bitbrute(iterator):
    while True:
        private_key = generate_private_key()
        public_key = pubkey(private_key)
        public_keyc = pubkeyc(private_key)
        address = addr(public_key)
        addressc = addrc(public_keyc) 
        data_base = database(private_key, address, addressc, database)
        print(str(address)+" "+str(addressc))
        #multi = (secret_exponent, public_key, address, WIF, data_base)
        event, values = window.Read(timeout=10)     # read with a timeout of 10 ms
        if event in (None, 'Exit'):
            break
         #Output the "uptime" statistic to a text field in the window
        window.Element('_DATE_').Update(str(datetime.datetime.now()-start_time))
        window.Element('address').Update(str(address))
        window.Element('addressc').Update(str(addressc))        
        window.Element('private_key').Update(str(bitcoin.encode_privkey(private_key,'hex')))
    # Exiting the program
if __name__ == '__main__':
    try:
        pool = ThreadPool(processes = multiprocessing.cpu_count()*2)
        pool.map(bitbrute, range(0, 3)) #<----- change 10 to 5 if computer get slowly
    except:
        pool.close()
        exit()


