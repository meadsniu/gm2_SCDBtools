"""
SCDButil.py

Python utility class (SCDButil) to handle getting data from the g-2 
slow controls database. 

M. Eads
June 2017
"""

import sys, time, datetime
import psycopg2
import ROOT
import RunDButil

class SCDButil:
    """
    SCDButil class is a utility class for accessing information in the 
    slow controls database
    """

    # dictionary to hold the marker colors for various subchannels
    color_dict = { ('mscb323_Temp_P1', 0):ROOT.kRed, 
                   ('mscb323_Temp_P1', 1):ROOT.kRed+1,
                   ('mscb323_Temp_P1', 2):ROOT.kRed+2,
                   ('mscb13e_Temp_P1', 3):ROOT.kRed+3,
                   ('mscb13e_Temp_P1', 0):ROOT.kOrange, 
                   ('mscb13e_Temp_P1', 1):ROOT.kOrange+1,
                   ('mscb13e_Temp_P1', 2):ROOT.kOrange+2,
                   ('mscb13e_Temp_P1', 3):ROOT.kOrange+3,
                   ('mscb323_Temp_P1', 4):ROOT.kYellow, 
                   ('mscb323_Temp_P1', 5):ROOT.kYellow+1,
                   ('mscb323_Temp_P1', 6):ROOT.kYellow+2,
                   ('mscb13e_Temp_P1', 7):ROOT.kYellow+3,
                   ('mscb13e_Temp_P1', 4):ROOT.kGreen, 
                   ('mscb13e_Temp_P1', 5):ROOT.kGreen+1,
                   ('mscb13e_Temp_P1', 6):ROOT.kGreen+2,
                   ('mscb13e_Temp_P1', 7):ROOT.kGreen+3,
                   ('mscb323_Temp_P2', 0):ROOT.kTeal, 
                   ('mscb323_Temp_P2', 1):ROOT.kTeal+1,
                   ('mscb323_Temp_P2', 2):ROOT.kTeal+2,
                   ('mscb13e_Temp_P2', 3):ROOT.kTeal+3,
                   ('mscb13e_Temp_P2', 0):ROOT.kCyan, 
                   ('mscb13e_Temp_P2', 1):ROOT.kCyan+1,
                   ('mscb13e_Temp_P2', 2):ROOT.kCyan+2,
                   ('mscb13e_Temp_P2', 3):ROOT.kCyan+3,
                   ('mscb323_Temp_P2', 4):ROOT.kAzure, 
                   ('mscb323_Temp_P2', 5):ROOT.kAzure+1,
                   ('mscb323_Temp_P2', 6):ROOT.kAzure+2,
                   ('mscb13e_Temp_P2', 7):ROOT.kAzure+3,
                   ('mscb13e_Temp_P2', 4):ROOT.kBlue, 
                   ('mscb13e_Temp_P2', 5):ROOT.kBlue+1,
                   ('mscb13e_Temp_P2', 6):ROOT.kBlue+2,
                   ('mscb13e_Temp_P2', 7):ROOT.kBlue+3,
                   ('mscb323_Temp_P3', 0):ROOT.kViolet, 
                   ('mscb323_Temp_P3', 1):ROOT.kViolet+1,
                   ('mscb323_Temp_P3', 2):ROOT.kViolet+2,
                   ('mscb13e_Temp_P3', 3):ROOT.kViolet+3,
                   ('mscb323_Temp_P3', 4):ROOT.kViolet, 
                   ('mscb323_Temp_P3', 5):ROOT.kViolet+1,
                   ('mscb323_Temp_P3', 6):ROOT.kViolet+2,
                   ('mscb13e_Temp_P3', 7):ROOT.kViolet+3,
                   ('mscb13e_Temp_P3', 0):ROOT.kMagenta, 
                   ('mscb13e_Temp_P3', 1):ROOT.kMagenta+1,
                   ('mscb13e_Temp_P3', 2):ROOT.kMagenta+2,
                   ('mscb13e_Temp_P3', 3):ROOT.kMagenta+3,
                   ('mscb13e_Temp_P4', 1):ROOT.kMagenta, 
                   ('mscb13e_Temp_P4', 2):ROOT.kMagenta+1,
                   ('mscb13e_Temp_P4', 3):ROOT.kMagenta+2,
                   ('mscb13e_Temp_P4', 4):ROOT.kMagenta+3,
                   ('mscb174_Temp_P1', 4):ROOT.kSpring-4,
                   ('mscb174_Temp_P1', 5):ROOT.kSpring-3,
                   ('mscb174_Temp_P1', 6):ROOT.kSpring-2,
                   ('mscb174_Temp_P1', 7):ROOT.kSpring-1,
                   ('mscb174_Temp_P5', 0):ROOT.kSpring,
                   ('mscb174_Temp_P5', 1):ROOT.kSpring+1,
                   ('mscb174_Temp_P5', 2):ROOT.kSpring+2,
                   ('mscb174_Temp_P5', 3):ROOT.kSpring+3,
                   ('mscb174_Temp_P5', 4):ROOT.kSpring+4,
                   ('mscb174_Temp_P5', 5):ROOT.kSpring+5,
                   ('mscb174_Temp_P5', 6):ROOT.kSpring+6,
                   ('mscb174_Temp_P5', 7):ROOT.kSpring+7,
                   ('mscb174_Temp_P7', 0):ROOT.kPink,
                   ('mscb174_Temp_P7', 1):ROOT.kPink+1, 
                   ('mscb110_Temp_P1', 0):ROOT.kBlue-3,
                   ('mscb110_Temp_P1', 1):ROOT.kBlue-2,
                   ('mscb110_Temp_P1', 2):ROOT.kBlue-1,
                   ('mscb110_Temp_P1', 3):ROOT.kBlue,
                   ('mscb110_Temp_P1', 4):ROOT.kBlue+1,
                   ('mscb110_Temp_P1', 5):ROOT.kBlue+2,
                   ('mscb110_Temp_P1', 6):ROOT.kBlue+3, 
                   ('mscb13e_ADC_P0', 2):ROOT.kBlue,
                   ('mscb174_ADC_P0', 7):ROOT.kBlue+1,
                   ('mscb110_ADC_P0', 1):ROOT.kBlue+2,
                   ('mscb13e_ADC_P0', 0):ROOT.kBlue,
                   ('mscb174_ADC_P0', 5):ROOT.kBlue+1,
                   ('mscb110_ADC_P0', 0):ROOT.kBlue+2,
                   ('mscb282_DAC_P6', 0):ROOT.kBlue-10,
                   ('mscb282_DAC_P6', 1):ROOT.kBlue,
                   ('mscb282_DAC_P6', 2):ROOT.kBlue+4,
                   ('mscb282_Temp_P2', 3):ROOT.kRed-10,
                   ('mscb282_Temp_P2', 4):ROOT.kRed,
                   ('mscb282_Temp_P2', 5):ROOT.kRed+4,
                   ('mscb282_Din_P4', 0):ROOT.kGray,
                   ('mscb282_Din_P4', 1):ROOT.kGray+1,
                   ('mscb282_Din_P4', 2):ROOT.kGray+2,
                   ('mscb282_Din_P4', 3):ROOT.kOrange-4,
                   ('mscb282_Din_P4', 4):ROOT.kOrange,
                   ('mscb282_Din_P4', 5):ROOT.kOrange+7,
                   ('mscb319_PT1000_P0', 0): ROOT.kOrange-9,
                   ('mscb319_PT1000_P0', 1): ROOT.kOrange-8,
                   ('mscb319_PT1000_P1', 0): ROOT.kOrange-7,
                   ('mscb319_PT1000_P1', 1): ROOT.kOrange-6,
                   ('mscb319_PT1000_P2', 0): ROOT.kOrange-5,
                   ('mscb319_PT1000_P2', 1): ROOT.kOrange-4,
                   ('mscb319_PT1000_P3', 0): ROOT.kOrange-3,
                   ('mscb319_PT1000_P3', 1): ROOT.kOrange-2,
                   ('mscb319_PT1000_P4', 0): ROOT.kOrange-1,
                   ('mscb319_PT1000_P4', 1): ROOT.kOrange,
                   ('mscb319_PT1000_P5', 0): ROOT.kOrange+1,
                   ('mscb319_PT1000_P5', 1): ROOT.kOrange+2, 
                   ('acnet_weather_dtemp', 0): ROOT.kGray+2,
                   ('acnet_weather_gtemp', 0): ROOT.kBlack,
                   ('acnet_weather_ghumid', 0): ROOT.kBlack,
                   ('acnet_weather_gbress', 0): ROOT.kBlack
                 }

    # Dictionary to hold the list of subchannels for specific plots
    subchannel_dict = {}
    subchannel_dict['hall'] = [ ('mscb174_Temp_P1', 4), ('mscb174_Temp_P1', 5), ('mscb174_Temp_P1', 6), ('mscb174_Temp_P1', 7), ('mscb174_Temp_P5', 0), ('mscb174_Temp_P5', 1), ('mscb174_Temp_P5', 2), ('mscb174_Temp_P5', 3), ('mscb174_Temp_P5', 4), ('mscb174_Temp_P5', 5), ('mscb174_Temp_P5', 6), ('mscb174_Temp_P5', 7) ]
    subchannel_dict['hall_outside'] = [ ('mscb174_Temp_P1', 4), ('mscb174_Temp_P1', 5), ('mscb174_Temp_P1', 6), ('mscb174_Temp_P1', 7), ('mscb174_Temp_P5', 0), ('mscb174_Temp_P5', 1), ('mscb174_Temp_P5', 2), ('mscb174_Temp_P5', 3), ('mscb174_Temp_P5', 4), ('mscb174_Temp_P5', 5), ('mscb174_Temp_P5', 6), ('mscb174_Temp_P5', 7), ('acnet_weather_gtemp', 0)]
    subchannel_dict['laser_hut'] = [ ('mscb174_Temp_P7', 0), ('mscb174_Temp_P7', 1) ]
    subchannel_dict['computer_room'] = [ ('mscb110_Temp_P1', 0), ('mscb110_Temp_P1', 1), ('mscb110_Temp_P1', 2), ('mscb110_Temp_P1', 3), ('mscb110_Temp_P1', 4), ('mscb110_Temp_P1', 5), ('mscb110_Temp_P1', 6) ]
    subchannel_dict['magnetA'] = [ ('mscb323_Temp_P1', 0), ('mscb323_Temp_P1', 1), ('mscb323_Temp_P1', 2), ('mscb323_Temp_P1', 3) ]
    subchannel_dict['magnetB'] = [ ('mscb13e_Temp_P1', 0), ('mscb13e_Temp_P1', 1), ('mscb13e_Temp_P1', 2), ('mscb13e_Temp_P1', 3) ]
    subchannel_dict['magnetC'] = [ ('mscb323_Temp_P1', 4), ('mscb323_Temp_P1', 5), ('mscb323_Temp_P1', 6), ('mscb323_Temp_P1', 7) ]
    subchannel_dict['magnetD'] = [ ('mscb13e_Temp_P1', 4), ('mscb13e_Temp_P1', 5), ('mscb13e_Temp_P1', 6), ('mscb13e_Temp_P1', 7) ]
    subchannel_dict['magnetE'] = [ ('mscb323_Temp_P2', 0), ('mscb323_Temp_P2', 1), ('mscb323_Temp_P2', 2), ('mscb323_Temp_P2', 3) ]
    subchannel_dict['magnetF'] = [ ('mscb13e_Temp_P4', 6), ('mscb13e_Temp_P2', 1), ('mscb13e_Temp_P2', 0), ('mscb13e_Temp_P2', 3) ]
    subchannel_dict['magnetG'] = [ ('mscb323_Temp_P2', 4), ('mscb323_Temp_P2', 5), ('mscb323_Temp_P2', 6), ('mscb323_Temp_P2', 7) ]
    subchannel_dict['magnetH'] = [ ('mscb13e_Temp_P2', 4), ('mscb13e_Temp_P2', 5), ('mscb13e_Temp_P2', 6), ('mscb13e_Temp_P2', 7) ]
    subchannel_dict['magnetI'] = [ ('mscb323_Temp_P3', 0), ('mscb323_Temp_P3', 1), ('mscb323_Temp_P3', 2), ('mscb323_Temp_P4', 3) ]
    subchannel_dict['magnetJ'] = [ ('mscb13e_Temp_P3', 7), ('mscb13e_Temp_P3', 1), ('mscb13e_Temp_P3', 2), ('mscb13e_Temp_P3', 3) ]
    subchannel_dict['magnetK'] = [ ('mscb323_Temp_P3', 4), ('mscb323_Temp_P3', 5), ('mscb323_Temp_P3', 6), ('mscb323_Temp_P3', 7) ]
    subchannel_dict['magnetL'] = [ ('mscb13e_Temp_P4', 1), ('mscb13e_Temp_P4', 2), ('mscb13e_Temp_P3', 5), ('mscb13e_Temp_P4', 4) ]
    subchannel_dict['humidity'] = [ ('mscb13e_ADC_P0', 2), ('mscb174_ADC_P0', 7), ('mscb110_ADC_P0', 1), ('acnet_weather_ghumid', 0) ]
    subchannel_dict['pressure'] = [ ('mscb13e_ADC_P0', 0), ('mscb174_ADC_P0', 5), ('mscb110_ADC_P0', 0), ('acnet_weather_gbpress', 0) ]
    subchannel_dict['kickersetv'] = [('mscb282_DAC_P6', 0), ('mscb282_DAC_P6', 1), ('mscb282_DAC_P6', 2) ]
    subchannel_dict['kickertemp'] = [('mscb282_Temp_P2', 3), ('mscb282_Temp_P2', 4), ('mscb282_Temp_P2', 5) ]
    subchannel_dict['kickeroil'] = [('mscb282_Din_P4', 0), ('mscb282_Din_P4', 1), ('mscb282_Din_P4', 2), ('mscb282_Din_P4', 3), ('mscb282_Din_P4', 4), ('mscb282_Din_P4', 5)]
    subchannel_dict['vacchamber'] = [('mscb319_PT1000_P0', 0), ('mscb319_PT1000_P0', 1), ('mscb319_PT1000_P1', 0), ('mscb319_PT1000_P1', 1), ('mscb319_PT1000_P2', 0), ('mscb319_PT1000_P2', 1), ('mscb319_PT1000_P3', 0), ('mscb319_PT1000_P3', 1), ('mscb319_PT1000_P4', 0), ('mscb319_PT1000_P4', 1), ('mscb319_PT1000_P5', 0), ('mscb319_PT1000_P5', 1) ]
    subchannel_dict['acnet_temp'] = [('acnet_weather_gtemp', 0), ('acnet_weather_dtemp', 0)]
    subchannel_dict['acnet_humidity'] = [('acnet_weather_ghumid', 0)]
    subchannel_dict['acnet_pressure'] = [('acnet_weather_gbpress', 0)]

    subchannel_dict['magnetback'] = [('mscb323_Temp_P1', 1), ('mscb323_Temp_P1', 5), ('mscb323_Temp_P2', 1), ('mscb323_Temp_P2', 5), ('mscb323_Temp_P3', 1), ('mscb323_Temp_P3', 5), ('mscb13e_Temp_P1', 1), ('mscb13e_Temp_P1', 5), ('mscb13e_Temp_P2', 1), ('mscb13e_Temp_P2', 5), ('mscb13e_Temp_P3', 1), ('mscb13e_Temp_P4', 2) ]

    # calibration dictionary to hold the calibration values
    calib_dict = {}

    def __init__(self, db='online', calib = False):
        # initialize the database connection
        params = ""
        if db == 'online':
            params = 'dbname=gm2_online_prod user=gm2_reader host=localhost port=5433'
        elif db == 'offline':
            # if connecting from a Fermilab IP, you don't need a password
            params = 'dbname=gm2_online_prod user=gm2_reader  host=ifdbprod.fnal.gov port=5452'
            # connecting from offsite requires a password, add it here
            #params = 'dbname=gm2_online_prod user=gm2_reader password=XXX host=ifdbprod.fnal.gov port=5452'
        else:
            print 'Unknown database:', db
        self.conn = psycopg2.connect(params)

        self.calib = calib
        # pull out the temperature calibration numbers
        if (self.calib):
            sql = 'SELECT subchannel, calib_value  FROM g2sc_calib_temp WHERE "isValid"=true ; '
            cur = self.conn.cursor()
            cur.execute(sql)

            while True:
                entry = cur.fetchone()
                if not entry: 
                    break
                subchannel = entry[0]
                value = entry[1]
                index = int(subchannel.split('_')[-1])
                channel = subchannel[:-2]
                self.calib_dict[ (channel, index) ] = value

            # pull out the humidity/pressure calibration numbers
            sql = 'SELECT subchannel, calib_slope, calib_intercept  FROM g2sc_calib_adc WHERE "isValid"=true ; '
            cur = self.conn.cursor()
            cur.execute(sql)

            while True:
                entry = cur.fetchone()
                if not entry: 
                    break
                subchannel = entry[0]
                slope = entry[1]
                intercept = entry[2]
                index = int(subchannel.split('_')[-1])
                channel = subchannel[:-2]
                self.calib_dict[ (channel, index) ] = (slope, intercept)

    def __del__(self):
        # close the database connection
        self.conn.close()

    def execute_query(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur

    def generate_sql_channel(self, channel, time_interval='all', checkGood=True, limit=-1):
       if time_interval == 'hour':
           interval = " now() - interval '1 hour' "
       elif time_interval == 'day':
           interval = " now() - interval '1 day' "
       elif time_interval == 'week':
           interval = " now() - interval '1 week' "
       elif time_interval == 'month':
           interval = " now() - interval '1 month' "
       elif time_interval == 'all':
           interval = " now() - interval '10 years' "
       elif time_interval == 'commissioning_run':
           interval = " date('2017-05-31') AND time < date('2017-07-08') "
       elif time_interval.startswith('runrange'):
           rundb = RunDButil.RunDButil()
           startrun = time_interval.split('-')[0][8:]
           stoprun = time_interval.split('-')[1]
           start = rundb.get_starttime(startrun)
           stop = rundb.get_stoptime(stoprun)
           interval = "'" + start.isoformat() + "'"' AND time < ' + "'" + stop.isoformat() + "' "
       elif time_interval.startswith('run'):
           rundb = RunDButil.RunDButil()
           run = time_interval[3:]
           start = rundb.get_starttime(run)
           stop = rundb.get_stoptime(run)
           interval = "'" + start.isoformat() + "'"' AND time < ' + "'" + stop.isoformat() + "' "

       sql = "SELECT * from g2sc_values "
       sql += "WHERE channel='" + channel + "' "
       sql += 'AND "isGood"=true  '
       sql += 'AND time > ' + interval 
       

       if checkGood:
           sql += ' AND "isGood"=True '

       if limit > 0:
           sql += ' LIMIT ' + str(limit) + ' '

       sql += ' ; '
        
       #print sql
       return sql

    def get_channel_data(self, channel, checkGood=True, time_interval='all', limit=-1):
        cur = self.execute_query(self.generate_sql_channel(channel=channel, checkGood=checkGood, time_interval=time_interval))
        return cur.fetchall()
                              
    def get_subchannel_data(self, channel, index, checkGood=True, time_interval='all', limit=-1):
        # execute the query for the channel
        channel_data = self.get_channel_data(channel=channel, checkGood=checkGood, time_interval=time_interval)

        # loop over channel data, pull out a tuple with only the specirfic subchannel
        results = []
        for entry in channel_data:
            results.append( (entry[3], entry[2][index]) )

        return results

    def get_title(self, channel, index):
        title = channel + ', subchannel ' + str(index)
        sql =  "SELECT name FROM g2sc_subchannels "
        sql += "WHERE channel='" + channel + "' AND index=" + str(index)
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) == 1:
            title = results[0][0]

        return title

    def get_label(self, channel, index):
        title = channel + ', subchannel ' + str(index)
        sql =  "SELECT display_name FROM g2sc_subchannels "
        sql += "WHERE channel='" + channel + "' AND index=" + str(index)
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        if len(results) == 1:
            title = results[0][0]

        return title

    def get_graph(self, channel, index, checkGood=True, time_interval='all', scale_overflow=True):
        cur = self.execute_query(self.generate_sql_channel(channel=channel, checkGood=checkGood, time_interval=time_interval))

        #cal = 0.0
        #if self.calib:
        #    if (channel, index) in self.calib_dict.keys():
        #        cal = self.calib_dict[ (channel, index) ]
        #    print 'found calibration:', channel, index, cal

        gr = ROOT.TGraph()
        i = 0
        while True:
            entry = cur.fetchone()
            if not entry:
                break

            value = entry[2][index]

            if scale_overflow == True:
                # for adc channels, should be between 0 and 5
                if channel.find('ADC') != -1:
                    if (value < 0.0) or (value > 5.0):
                        value = 0.0;
                # don't make any changes to ACNET channels
                elif channel.find('acnet') != -1:
                    pass
                # for temp channels, set to 25
                else:
                    if value < -10.:
                        value = 25.
                    elif value > 50.:
                        value = 25.

            if channel.find('Temp') != -1:
                if self.calib and ( (channel, index) in self.calib_dict.keys()):
                    gr.SetPoint(i, time.mktime(entry[3].timetuple()), value+self.calib_dict[ (channel, index) ])
                    #print 'apply calibration:', channel, index, value, self.calib_dict[ (channel, index) ],  value-self.calib_dict[ (channel, index) ]
                else:
                    gr.SetPoint(i, time.mktime(entry[3].timetuple()), value)
            elif self.calib and (channel.find('ADC') != -1):
                if (channel, index) in self.calib_dict.keys():    
                    gr.SetPoint(i, time.mktime(entry[3].timetuple()), self.calib_dict[ (channel, index) ][0]*value+self.calib_dict[ (channel, index) ][1])
                else:
                    gr.SetPoint(i, time.mktime(entry[3].timetuple()), value)
            else:
                gr.SetPoint(i, time.mktime(entry[3].timetuple()), value)
            i += 1

        return gr

    def get_average_graph(self, channel, index_list, checkGood=True, time_interval='all'):
        cur = self.execute_query(self.generate_sql_channel(channel=channel, checkGood=checkGood, time_interval=time_interval))

        gr = ROOT.TGraph()
        i = 0
        while True:
            entry = cur.fetchone()
            if not entry:
                break

            sum = 0.
            num = 0
            for index in index_list:
                value = entry[2][index]
                if value > -49. and value < 149.:
                    sum += value
                    num += 1
            avg = sum/num
            gr.SetPoint(i, time.mktime(entry[3].timetuple()), avg)
            i += 1

        return gr
        
        
    def plot_channel(self, channel, index, checkGood=True, time_interval='all', scale_overflow=True):
        #canvas = ROOT.TCanvas()
        #canvas.cd()
        gr = self.get_graph(channel=channel, index=index, checkGood=checkGood, time_interval=time_interval, scale_overflow=scale_overflow)

        gr.SetMarkerColor(ROOT.kBlue)
        gr.Draw('ap')
        gr.GetXaxis().SetTimeDisplay(1)
        gr.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
        gr.GetXaxis().SetLabelSize(0.025)
        gr.GetXaxis().SetLabelOffset(0.02)

        yaxis_title = 'value'
        if channel.find('Temp') != -1:
            yaxis_title = 'Temperature (#circ C)'
        elif channel.find('PT1000') != -1:
            yaxis_title = 'Temperature (#circ C)'
        elif channel.find('ADC') != -1:
            yaxis_title = 'ADC value (Volts)'
        gr.GetYaxis().SetTitle(yaxis_title)
        gr.GetYaxis().SetTitleOffset(1.3)

        gr.SetTitle(self.get_title(channel=channel, index=index))

        return gr

    def plot_channels(self, subchannel_list, checkGood=True, time_interval='all', title='', scale_overflow=True, fixed_scale=False, draw_legend=True):
        graphs = []
        mg = ROOT.TMultiGraph()
        mg.SetTitle(title)
        leg = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
        for entry in subchannel_list:
            gr = self.get_graph(channel=entry[0], index=entry[1], checkGood=checkGood, time_interval=time_interval, scale_overflow=scale_overflow)
            gr.SetName(self.get_label(channel=entry[0], index=entry[1]))
            if (entry[0], entry[1]) in self.color_dict.keys():
                gr.SetMarkerColor(self.color_dict[ (entry[0], entry[1]) ])
                gr.SetLineColor(self.color_dict[ (entry[0], entry[1]) ] )
            else:
                gr.SetMarkerColor(ROOT.kBlack)
                gr.SetLineColor(ROOT.kBlack)
            if 'mscb282_DAC_P6' in entry[0]:
                gr.SetMarkerStyle(6)
            graphs.append(gr)

        #canvas = ROOT.TCanvas()
        first = True
        i = 0
        for gr in graphs:
            mg.Add(gr)

            
            #if first:
                #gr.SetMarkerColor(ROOT.kBlue)
                #gr.Draw('ap')
                #gr.GetXaxis().SetTimeDisplay(1)
                #gr.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
                #gr.GetXaxis().SetLabelSize(0.025)
                #gr.GetXaxis().SetLabelOffset(0.02)

                #yaxis_title = 'value'
                #if subchannel_list[0][0].find('Temp') != -1:
                #    yaxis_title = 'Temperature (#circ C)'
                #elif subchannel_list[0][0].find('ADC') != -1:
                #    yaxis_title = 'ADC value (Volts)'
                #gr.GetYaxis().SetTitle(yaxis_title)
                #gr.GetYaxis().SetTitleOffset(1.3)

                #first = False
            #else:
                #i += 1
                #gr.SetMarkerColor(ROOT.kBlue+i)
                #gr.Draw('a same')

            #print 'adding graph to legend..'
            leg.AddEntry(gr, 'name', 'l')

        mg.Draw('ap')
        mg.GetXaxis().SetTimeDisplay(1)
        mg.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
        mg.GetXaxis().SetLabelSize(0.025)
        mg.GetXaxis().SetLabelOffset(0.02)

        if draw_legend:
            #print 'drawing legend...'
            leg.Draw()

        yaxis_title = 'value'
        if subchannel_list[0][0].find('Temp') != -1:
            if self.calib == False:
                yaxis_title = 'Temp(raw) (#circ C)'
            else:
                yaxis_title = 'Temp(calib) (#circ C)'
        elif subchannel_list[0][0].find('PT1000') != -1:
            if self.calib == False:
                yaxis_title = 'Temp(raw) (#circ C)'
            else:
                yaxis_title = 'Temp(raw) (#circ C)'
        elif subchannel_list[0][0].find('ADC') != -1:
            if self.calib == False:
                yaxis_title = 'ADC value (Volts)'
            elif subchannel_list[0] in self.subchannel_dict['humidity']:
                yaxis_title = 'Relative Humidity (%)'
            elif subchannel_list[0] in self.subchannel_dict['pressure']:
                yaxis_title = 'Air Pressure (mbar)'
            else:
                yaxis_title = 'ADC value (Volts)'
        mg.GetYaxis().SetTitle(yaxis_title)
        mg.GetYaxis().SetTitleOffset(1.3)

        if fixed_scale:
            mg.GetYaxis().SetRangeUser(25., 35.)

        return mg


if __name__ == '__main__':
    db = SCDButil(calib=True)

    subchannel_list = [ ('mscb323_Temp_P1', 0), ('mscb323_Temp_P1', 1) ]

    canvas = ROOT.TCanvas('c1', 'c1', 1)
    g = db.plot_channels(db.subchannel_dict['magnetback'], time_interval='all')
    g.Draw('ap')

    #ROOT.gApplication.Run()
