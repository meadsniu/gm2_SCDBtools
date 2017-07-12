"""
SCMIDASutil.py

Python utility class (SCMIDASutil) to pull information from midas files.
Currently only handles the text midas files produced with mdump.

M. Eads
July 2017
"""

class SCMIDASutil:
    """
    SCMIDASutil class is a utility class for pulling information 
    from midas (text) files
    """

    mscb_dict = {'006e':'mscb110', '00ae':'mscb174', '013e':'mscb13e', '013f':'mscb319', '0143':'mscb323', '011a':'mscb282' }

    def __init__(self, filename):
        # open the file
        self.infile = open(filename)

    def get_next_event(self):
        last_pos = self.infile.tell()
        line = self.infile.readline()

        event_lines = []
        eventNum = -1

        # skip event 0, which is empty
        if line.startswith('------------------------ Event# 0'):
            last_pos = self.infile.tell()
            line = self.infile.readline()

        # check for end of file
        #print line
        if not self.infile:
            return

        # find the first line of the event
        while not line.startswith('------------------------ Event#'):
            last_pos = self.infile.tell()
            line = self.infile.readline()
            if line == '': break

        # get the event number
        if line.startswith('------------------------ Event#'):
            eventNum = int(line.split()[2])

        # read through the file, adding lines to the output until next event or end of file is found
        event_lines.append(line)
        while True:
            last_pos = self.infile.tell()
            line = self.infile.readline()
            if line.startswith('------------------------ Event#'): break
            if line == None or line == '': 
                #print 'EOF'
                return
            event_lines.append(line)
            
        # move the file pointer back one line
        self.infile.seek(last_pos)

        #print '*** event', eventNum
        #print event_lines

        return (eventNum, event_lines)

    def get_banks(self, event_info):
        ret = []
        bank_list = []

        #print '** processing event', event_info[0]

        # get the event ID
        if len(event_info[1]) == 1:
            print 'empty event, exiting'
            return ret

        # get the event ID and timestamp
        eventID = event_info[1][1][5:9]
        mscb = self.mscb_dict[eventID]
        #print eventID, mscb

        # get the timestamp
        first_index = event_info[1][1].find('Time:') + 5
        second_index = event_info[1][1].find('Dsize:') - 2
        if first_index == 4 or second_index == -3:
            print "can't find timestamp for event", event_info[0], ', exiting'
            return ret
        timestamp =  event_info[1][1][first_index:second_index]

        # loop through event lines, find lines starting with "Bank"
        bank_lines = []
        for i in range(len(event_info[1])):
            if event_info[1][i].startswith('Bank:'):
                bank_lines.append(i)
            
        #print bank_lines
        
        bankName = ''
        if len(bank_lines) == 0:
            print 'no banks found for event', event_info[0], ', exiting'
            return ret
        elif len(bank_lines) == 1:
            #ret.append(event_info[1][bank_lines[0]:])
            bankName = event_info[1][bank_lines[0]][5:9]
            bank_list.append(MidasBank(eventNum=event_info[0], eventID=eventID, bankName=bankName, timestamp=timestamp, bank=event_info[1][bank_lines[0]:]))
        elif len(bank_lines) == 2:
            #ret.append(event_info[1][bank_lines[0]:bank_lines[1]])
            #ret.append(event_info[1][bank_lines[1]:])
            bankName = event_info[1][bank_lines[0]][5:9]
            bank_list.append(MidasBank(eventNum=event_info[0], eventID=eventID, bankName=bankName, timestamp=timestamp, bank=event_info[1][bank_lines[0]:bank_lines[1]]))

            bankName = event_info[1][bank_lines[1]][5:9]
            bank_list.append(MidasBank(eventNum=event_info[0], eventID=eventID, bankName=bankName, timestamp=timestamp, bank=event_info[1][bank_lines[1]:]))
                             
        else:
            print 'too many banks:', bank_lines, ', exiting...'
            return ret

        #print ret
        return bank_list

class MidasBank:
    """
    Class to hold the information from a single midas bank
    """
    def __init__(self, eventNum = -1, eventID = -1, bankName = 'XXX', timestamp = -1, bank = []):
        self.eventNum = eventNum
        self.eventID = eventID
        self.bankName = bankName
        self.timestamp = timestamp
        self.bank = bank


if __name__ == '__main__':

    filename = 'midas_files/run00580.mid.txt'
    mf = SCMIDASutil(filename)

    #for i in range(5):
    #    event = mf.get_next_event()
    #    banks = mf.get_banks(event)
    
