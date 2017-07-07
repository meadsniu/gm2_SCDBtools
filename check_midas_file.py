"""
check_midas_file.py

Python script to look into a midas (text) file and spit out some basic data.

M. Eads
July 2017
"""

import SCMIDASutil

debug = True
show_timestamps = True
show_eventIDs = True
show_banks = True
show_events = True
pause = False

input_filenames = []
input_filenames.append('midas_files/run00585.mid.txt')

bank_list = []
eventID_list = []
mscb_list = []
mscb_dict = {'006e':'mscb110', '00ae':'mscb174', '013e':'mscb13e', '013f':'mscb319', '0143':'mscb323', '011a':'mscb282' }

for filename in input_filenames:
    m = SCMIDASutil.SCMIDASutil(filename)

    # find the run number
    first_index = filename.find('run')+3
    second_index = filename.find('.mid')
    runNum = int(filename[first_index:second_index])
    print '================== Processing Run', runNum, '=================='

    i = 0

    while True:
        event = m.get_next_event()
        if not event: break
        i = i + 1

        b = m.get_banks(event)

        if len(b) > 0:
            print '*** event', b[0].eventNum, 'has', len(b), 'banks'

            for bank in b:
                print '      bank:', bank.bankName
                print '           timestamp:', bank.timestamp
                print '           eventID:', bank.eventID
                print '           lines:', bank.bank
                
                if bank.bankName not in bank_list:
                    bank_list.append(bank.bankName)
                if bank.eventID not in eventID_list:
                    eventID_list.append(bank.eventID)
                

        if pause:
            x = raw_input()

    print
    print '** found', i, 'events'
    print '   banks:', bank_list
    print '   eventIDs:', eventID_list
