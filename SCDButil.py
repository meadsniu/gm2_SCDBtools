"""
SCDButil.py

Python utility class (SCDButil) to handle getting data from the g-2 
slow controls database. 

M. Eads
June 2017
"""

import sys, time
import psycopg2
import ROOT

class SCDButil:
    """
    SCDButil class is a utility class for accessign information in the 
    slow controls database
    """
    def __init__(self, db='online'):
        # initialize the database connection
        params = ""
        if db == 'online':
            params = 'dbname=gm2_online_prod user=gm2_reader host=localhost port=5433'
        else:
            print 'Unknown database:', db
        self.conn = psycopg2.connect(params)

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

       sql = "SELECT * from g2sc_values "
       sql += "WHERE channel='" + channel + "' "
       sql += 'AND "isGood"=true  '
       sql += 'AND time > ' + interval 

       if checkGood:
           sql += ' AND "isGood"=True '

       if limit > 0:
           sql += ' LIMIT ' + str(limit) + ' '

       sql += ' ; '
        
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

    def get_graph(self, channel, index, checkGood=True, time_interval='all'):
        cur = self.execute_query(self.generate_sql_channel(channel=channel, checkGood=checkGood, time_interval=time_interval))

        gr = ROOT.TGraph()
        i = 0
        while True:
            entry = cur.fetchone()
            if not entry:
                break

            gr.SetPoint(i, time.mktime(entry[3].timetuple()), entry[2][index])
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
        
        
    def plot_channel(self, channel, index, checkGood=True, time_interval='all'):
        #canvas = ROOT.TCanvas()
        #canvas.cd()
        gr = self.get_graph(channel=channel, index=index, checkGood=checkGood, time_interval=time_interval)

        gr.SetMarkerColor(ROOT.kBlue)
        gr.Draw('ap')
        gr.GetXaxis().SetTimeDisplay(1)
        gr.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
        gr.GetXaxis().SetLabelSize(0.025)
        gr.GetXaxis().SetLabelOffset(0.02)

        yaxis_title = 'value'
        if channel.find('Temp') != -1:
            yaxis_title = 'Temperature (#circ C)'
        elif channel.find('ADC') != -1:
            yaxis_title = 'ADC value (Volts)'
        gr.GetYaxis().SetTitle(yaxis_title)
        gr.GetYaxis().SetTitleOffset(1.3)

        gr.SetTitle(self.get_title(channel=channel, index=index))

        return gr

    def plot_channels(self, subchannel_list, canvas, checkGood=True, time_interval='all'):
        graphs = []
        mg = ROOT.TMultiGraph()
        for entry in subchannel_list:
            graphs.append(self.get_graph(channel=entry[0], index=entry[1], checkGood=checkGood, time_interval=time_interval))

        canvas = ROOT.TCanvas()
        first = True
        i = 0
        for gr in graphs:
            mg.Add(gr)
            if first:
                gr.SetMarkerColor(ROOT.kBlue)
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

                first = False
            else:
                i += 1
                gr.SetMarkerColor(ROOT.kBlue+i)
                gr.Draw('a same')

        mg.Draw('ap')
        mg.GetXaxis().SetTimeDisplay(1)
        mg.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
        mg.GetXaxis().SetLabelSize(0.025)
        mg.GetXaxis().SetLabelOffset(0.02)

        mg.SetTitle()

        yaxis_title = 'value'
        if subchannel_list[0][0].find('Temp') != -1:
            yaxis_title = 'Temperature (#circ C)'
        elif subchannel_list[0][0].find('ADC') != -1:
            yaxis_title = 'ADC value (Volts)'
        mg.GetYaxis().SetTitle(yaxis_title)
        mg.GetYaxis().SetTitleOffset(1.3)

        return mg


if __name__ == '__main__':
    db = SCDButil()

    subchannel_list = [ ('mscb323_Temp_P1', 0), ('mscb323_Temp_P1', 1) ]

    canvas = ROOT.TCanvas('c1', 'c1', 1)
    g = db.plot_channels(subchannel_list, canvas)
    g.Draw('ap')

    #ROOT.gApplication.Run()
