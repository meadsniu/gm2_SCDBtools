"""
make_all_temp_plots.py

Python script to make a whole bunch of temperature plots. Saves canvases as 
PDF files. Design to run as a cron job which can update plots for a web page.

M. Eads
July 2017
"""

import SCDButil
import ROOT

db = SCDButil.SCDButil()

# create list of plots to make
plot_list = ['hall']

# which time interval plots to make
interval_list = ['all', 'week', 'day']

for plot in plot_list:
    g = db.plot_channels(db.subchannel_dict[plot], ROOT.TCanvas())
    g.Draw('ap')
