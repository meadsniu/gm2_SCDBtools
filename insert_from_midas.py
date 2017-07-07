"""
insert_from_midas.py

Python script to read in a midas (.txt from mdump) file and then 
upload the contained information to the slow controls database. 

M. Eads
July 2017
"""

import SCMIDASutil
import psycopg2
import sys

debug = False
write_to_db = False

conn = ''
if write_to_db:
    conn = psycopg2.connect("dbname=gm2_online_prod user=gm2_writer host=localhost port=5433")

mscb_list = []
last_timestamp = {}

filename = 'midas_files/run00593.mid.txt'

m = SCMIDASutil.SCMIDASutil(filename)

last_timestamp = {}
good_channels = []
good_channels.append('mscb323_Temp_P1')
good_channels.append('mscb323_Temp_P2')
good_channels.append('mscb323_Temp_P3')
good_channels.append('mscb323_Temp_P4')
good_channels.append('mscb13e_ADC_P0')
good_channels.append('mscb13e_Temp_P1')
good_channels.append('mscb13e_Temp_P2')
good_channels.append('mscb13e_Temp_P3')
good_channels.append('mscb13e_Temp_P4')
good_channels.append('mscb319_PT1000_P0')
good_channels.append('mscb174_ADC_P0')
good_channels.append('mscb174_Temp_P1')
good_channels.append('mscb174_Temp_P5')
good_channels.append('mscb174_Temp_P7')
good_channels.append('mscb110_ADC_P0')
good_channels.append('mscb110_Temp_P1')
good_channels.append('mscb282_ADC_P0')
good_channels.append('mscb282_ADC_P1')
good_channels.append('mscb282_Temp_P2')
good_channels.append('mscb282_Temp_P3')
good_channels.append('mscb282_Din_P4')
good_channels.append('mscb282_Dout_P5')
good_channels.append('mscb282_DAC_P6')

# find the run number
first_index = filename.find('run')+3
second_index = filename.find('.mid')
runNum = int(filename[first_index:second_index])
print '================== Processing Run', runNum, '=================='
i = 0
while True:
    event = m.get_next_event()
    if not event: break
    i = i+1

    b = m.get_banks(event)

    if len(b) == 0: break

    # check the mscb
    mscb = 'x'
    if b[0].eventID in m.mscb_dict.keys():
        mscb = m.mscb_dict[b[0].eventID]
        if mscb not in mscb_list:
            mscb_list.append(mscb)
            last_timestamp[mscb] = -1
    else:
        print 'unknown eventID:', b[0].eventID, ', exiting...'
        sys.exit()

    # check the timestamp
    timestamp = int(b[0].timestamp, 16)
    if timestamp == last_timestamp[mscb]:
        continue
    else:
        last_timestamp[mscb] = timestamp

    print mscb, b[0].timestamp

    values = []

    sql_base = 'INSERT INTO g2sc_values (channel, value, time) VALUES ('

    for bank in b:
        # generate the channel name
        if mscb == 'mscb323' and bank.bankName == 'MSCI':
            channel = 'mscb323_ADC_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb323_Temp_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb323_Temp_P2'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[3].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
           
            channel = 'mscb323_Temp_P3'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[4].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb323_Temp_P4'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[5].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
        elif mscb == 'mscb13e' and bank.bankName == 'MSCI':
            channel = 'mscb13e_ADC_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb13e_Temp_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb13e_Temp_P2'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[3].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb13e_Temp_P2'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[3].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb13e_Temp_P3'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[4].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb13e_Temp_P4'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[5].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

        elif mscb == 'mscb319' and bank.bankName == 'MSCI':
            channel = 'mscb319_PT1000_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2]  + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb319_PT1000_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[3] + ', ' + v[4]  + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb319_PT1000_P2'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[5] + ', ' + v[6]  + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb319_PT1000_P3'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[7] + ', ' + v[8]  + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb319_PT1000_P4'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2]  + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

        elif mscb == 'mscb174' and bank.bankName == 'MSCI':
            channel = 'mscb174_ADC_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb174_Temp_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb174_Temp_P5'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[3].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
            channel = 'mscb174_Temp_P7'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[5].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
        elif mscb == 'mscb110' and bank.bankName == 'MSCI':
            channel = 'mscb110_ADC_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb110_Temp_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
            
        elif mscb == 'mscb282' and bank.bankName == 'MSCI':
            channel = 'mscb282_ADC_P0'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb282_ADC_P1'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb282_Temp_P2'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[3].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb282_Temp_P3'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[4].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb282_Din_P4'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[5].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

        elif mscb == 'mscb282' and bank.bankName == 'MSCO':
            channel = 'mscb282_Dout_P5'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[1].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            channel = 'mscb282_DAC_P6'
            sql = sql_base + "'" + channel + "', '{"
            v = bank.bank[2].split()
            sql += v[1] + ', ' + v[2] + ', ' + v[3] + ', ' + v[4] + ', ' + v[5] + ', ' + v[6] + ', ' + v[7] + ', ' + v[8] + "}', "
            sql += "to_timestamp('" + bank.timestamp + "') "
            sql += ') ;'

            if debug: print sql
            if write_to_db:
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()

            
    #raw_input()
            

print '** processed', i, 'events'
print '   found mscbs', mscb_list
