"""
make_all_temp_plots.py

Python script to make a whole bunch of temperature plots. Saves canvases as 
PDF files. Design to run as a cron job which can update plots for a web page.

M. Eads
July 2017
"""

import SCDButil
import ROOT

# for non-calirated plots
db = SCDButil.SCDButil()

# create list of plots to make
plot_list = ['hall', 'laser_hut', 'computer_room', 'magnetA', 'magnetB', 'magnetC', 'magnetD', 'magnetE', 'magnetF', 'magnetG', 'magnetH', 'magnetI']
#plot_list = ['magnetA', 'magnetB']

# which time interval plots to make
interval_list = ['week', 'day', 'month', 'all']

leg_dict = {}

for plot in plot_list:
    for interval in interval_list:
        g = db.plot_channels(db.subchannel_dict[plot], time_interval=interval, title=plot + ', ' + interval, draw_legend=False, fixed_scale=False)
    
        canvas = ROOT.TCanvas(plot + '_' + interval + '_canvas', plot + '_' + interval + '_canvas', 1)
        g.Draw('ap')

        #leg_dict[ (plot, interval) ] = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
        #print len(g.GetListOfGraphs())
        #for i in range(len(g.GetListOfGraphs())):
            #leg_dict[ (plot, interval) ].AddEntry(gr, gr.GetName(), 'l')
            #print i
        #leg_dict[ (plot, interval) ].Draw()

        canvas.SaveAs(plot + '_' + interval + '.png')

# for calibrated plots
db2 = SCDButil.SCDButil(calib=True)
plot_list2 = ['humidity', 'pressure']

for plot in plot_list2:
    for interval in interval_list:
        g = db2.plot_channels(db.subchannel_dict[plot], time_interval=interval, title=plot + ', ' + interval, draw_legend=False, fixed_scale=False)
    
        canvas = ROOT.TCanvas(plot + '_' + interval + '_canvas', plot + '_' + interval + '_canvas', 1)
        g.Draw('ap')

        #leg_dict[ (plot, interval) ] = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
        #print len(g.GetListOfGraphs())
        #for i in range(len(g.GetListOfGraphs())):
            #leg_dict[ (plot, interval) ].AddEntry(gr, gr.GetName(), 'l')
            #print i
        #leg_dict[ (plot, interval) ].Draw()

        canvas.SaveAs(plot + '_' + interval + '.png')
