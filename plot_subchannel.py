"""
plot_subchannel.py

Defines python function to plot a single subchannel from the database.

M. Eads
Jun 2017
"""

import psycopg2
import sys, time
import ROOT

gr = ROOT.TGraph()

do_calib = False
calib = {}


def get_connection():
    return psycopg2.connect("dbname=gm2_online_prod user=gm2_reader password=gm2_4_reader host=ifdbprod.fnal.gov port=5452")
    #return psycopg2.connect("dbname=gm2_online_prod user=gm2_reader host=localhost port=5433")


def plot_subchannel(channel='test_channel', index=0, time_interval='all'):
    
    conn = get_connection()

    # figure out the time interval for the SQL query
    now = time.time()
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
    sql += 'AND time > ' + interval + ' ; '

    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()

    if len(results) == 0:
        print 'No results for channel', channel, ', index', index
        print 'exiting...'
        return

    cur.close()
    #conn.close()

    ##print results
    ##print "Returned", len(results), "values"

    # loop through the results, pull out the timestamp and the single value
    scrubbed_results = []
    for entry in results:
        #print entry 
        #print entry[2][index], entry[3]
        scrubbed_results.append( (entry[3], entry[2][index]) )

    #print scrubbed_results

    # fill entries in the TGraph
    i = 0
    for entry in scrubbed_results:
        gr.SetPoint(i, time.mktime(entry[0].timetuple()), entry[1])
        i += 1

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

    title = channel + ', subchannel ' + str(index)
    sql =  "SELECT name FROM g2sc_subchannels "
    sql += "WHERE channel='" + channel + "' AND index=" + str(index)
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    #print results[0][0]
    if len(results) == 1:
        title = results[0][0]
    conn.close()

    gr.SetTitle(title)

    return 

if do_calib:
    # get the connection, do the query
    conn = get_connection()
    sql = 'SELECT subchannel, calib_value  FROM g2sc_calib_temp; '
    cur = conn.cursor()
    cur.execute(sql)

    while True:
        entry = cur.fetchone()
        if not entry: 
            break
        #print entry
        subchannel = entry[0]
        value = entry[1]
        index = int(subchannel.split('_')[-1])
        channel = subchannel[:-2]
        #print channel, index
        calib[ (channel, index) ] = value




if __name__ == '__main__':

    channel = 'test_channel'
    index = 0
    time_interval = 'all'

    if len(sys.argv) > 1:
        channel = sys.argv[1]
    if len(sys.argv) > 2:
        index = int(sys.argv[2])
    if len(sys.argv) > 3:
        time_interval = sys.argv[3]

    if time_interval not in ['all', 'hour', 'day', 'week', 'month']:
        print 'Unknown time interval:', time_interval
        print 'Valid time intervals are: all, hour, day, week, or month'
        print
        sys.exit()
    
    plot_subchannel(channel=channel, index=index, time_interval=time_interval)
