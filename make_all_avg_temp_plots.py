"""
make_all_temp_plots.py

Python script to make a whole bunch of temperature plots. Saves canvases as 
PDF files. Design to run as a cron job which can update plots for a web page.

M. Eads
July 2017
"""

import SCDButil
import ROOT
import time

# for non-calirated plots
db = SCDButil.SCDButil(calib=True)

# create list of plots to make
#plot_list = ['hall', 'laser_hut', 'computer_room', 'magnetA', 'magnetB', 'magnetC', 'magnetD', 'magnetE', 'magnetF', 'magnetG', 'magnetH', 'magnetI', 'magnetJ', 'magnetK', 'magnetL', 'kickersetv', 'kickertemp', 'kickeroil']
plot_list = ['magnetA']

# which time interval plots to make
#interval_list = ['week', 'day', 'month', 'all']
interval = 'month'

leg_dict = {}

if interval == 'hour':
	begTime = time.time() - 3600	
elif interval == 'day':
	begTime = time.time() - 86400
elif interval == 'week':
	begTime = time.time() - 604800
elif interval == 'month':
	begTime = time.time() - 2678400
elif interval == 'year':
	begTime = time.time() - 31536000
elif interval == 'all':
	begTime = time.time() - 315360000

for plot in plot_list:
        g = db.avg_plot_channels(db.subchannel_dict[plot], time_interval=interval, title='Average:' + plot + ', ' + interval, draw_legend=False, fixed_scale=False, avg_interval=600.0, begTime = begTime)
        canvas = ROOT.TCanvas(plot + '_' + interval + '_canvas', plot + '_' + interval + '_canvas', 1)
        g.Draw('ap')

        #leg_dict[ (plot, interval) ] = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
        #print len(g.GetListOfGraphs())
        #for i in range(len(g.GetListOfGraphs())):
            #leg_dict[ (plot, interval) ].AddEntry(gr, gr.GetName(), 'l')
            #print i
        #leg_dict[ (plot, interval) ].Draw()

        canvas.SaveAs('avg_' + plot + '_' + interval + '.pdf')

# for calibrated plots
#db2 = SCDButil.SCDButil(calib=True)
#plot_list2 = ['humidity', 'pressure']

#for plot in plot_list2:
#    for interval in interval_list:
#        g = db2.plot_channels(db.subchannel_dict[plot], time_interval=interval, title=plot + ', ' + interval, draw_legend=False, fixed_scale=False)
    
#        canvas = ROOT.TCanvas(plot + '_' + interval + '_canvas', plot + '_' + interval + '_canvas', 1)
#        g.Draw('ap')

        #leg_dict[ (plot, interval) ] = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
        #print len(g.GetListOfGraphs())
        #for i in range(len(g.GetListOfGraphs())):
            #leg_dict[ (plot, interval) ].AddEntry(gr, gr.GetName(), 'l')
            #print i
        #leg_dict[ (plot, interval) ].Draw()

#        canvas.SaveAs(plot + '_' + interval + '.png')
