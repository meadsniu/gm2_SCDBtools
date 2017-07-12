"""
makePlots.py

Python script to make some plots of slow controls database quantities

M. Eads
Jun 2017
"""

import SCDButil
import ROOT

canvas_dict = {}
canvas_list = {}
graph_dict = {}

canvas_dict['c1'] = [ ('mscb323_Temp_P1', 0), ('mscb323_Temp_P1', 1), ('mscb323_Temp_P1', 2), ('mscb323_Temp_P1', 3) ]

#canvas_dict['c2'] = [ ('mscb13e_Temp_P1', 0), ('mscb13e_Temp_P1', 1), ('mscb13e_Temp_P1', 2), ('mscb13e_Temp_P1', 3) ]

#canvas_dict['c1'] = [ ('mscb323_Temp_P1', 0), ('mscb13e_Temp_P1', 0) ]

color_dict = {}
color_dict['c1'] = ROOT.kBlue
color_dict['c2'] = ROOT.kRed
color_dict['c3'] = ROOT.kGreen


time_interval = 'week'
draw_average = True
draw_legend = True


db = SCDButil.SCDButil()

for canvas in canvas_dict:
    print canvas
    canvas_list[canvas] = ROOT.TCanvas(canvas, canvas, 1)

    mg = ROOT.TMultiGraph()

    legend = ROOT.TLegend(0.75, 0.75, 0.95, 0.95)
    
    index_list = []

    first = True
    i = 0
    for entry in canvas_dict[canvas]:
        print entry
        graph_dict[canvas] = []
        index_list.append(entry[1])

        gr = db.get_graph(channel=entry[0], index=entry[1], time_interval=time_interval)
        gr.SetMarkerStyle(2)
        gr.SetMarkerColor(color_dict[canvas]+i)
        gr.SetMarkerSize(0.5)
        i += 1

        mg.Add(gr)

        if draw_legend:
            leg_title = db.get_label(channel=entry[0], index=entry[1])
            legend.AddEntry(gr, leg_title, 'p')
        #gr.SetMarkerColor(ROOT.kBlue+i)
        #if first:
        #    gr.Draw('ap')
        #    gr.GetXaxis().SetTimeDisplay(1)
        #    gr.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
        #    gr.GetXaxis().SetLabelSize(0.025)
        #    gr.GetXaxis().SetLabelOffset(0.02)

#            yaxis_title = 'value'
#            if entry[0].find('Temp') != -1:
#                yaxis_title = 'Temperature (#circ C)'
#            elif entry[0].find('ADC') != -1:
#                yaxis_title = 'ADC value (Volts)'
#            gr.GetYaxis().SetTitle(yaxis_title)
#            gr.GetYaxis().SetTitleOffset(1.3)
        
#            first = False
#        else:
#            gr.Draw('a same')
            
        #graph_dict[canvas].append(gr)
        

    #canvas_list[canvas].SaveAs(canvas + '.pdf')
    if draw_average:
        g_avg = db.get_average_graph(channel=canvas_dict[canvas][0][0], index_list=index_list, time_interval=time_interval)
        g_avg.SetMarkerColor(ROOT.kBlack)
        #g_avg.SetMarkerStyle(5)
        #g_avg.SetMarkerSize(0.5)
        mg.Add(g_avg)

        if draw_legend:
            legend.AddEntry(g_avg, 'Average', 'p')


    mg.Draw('ap')
    mg.GetXaxis().SetTimeDisplay(1)
    mg.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
    mg.GetXaxis().SetLabelSize(0.025)
    mg.GetXaxis().SetLabelOffset(0.02)
    yaxis_title = 'value'
    if canvas_dict[canvas][0][0].find('Temp') != -1:
        yaxis_title = 'Temperature (#circ C)'
    elif canvas_dict[canvas][0][0].find('ADC') != -1:
        yaxis_title = 'ADC value (Volts)'
    mg.GetYaxis().SetTitle(yaxis_title)
    mg.GetYaxis().SetTitleOffset(1.3)


    if draw_legend:
        legend.Draw()
    
