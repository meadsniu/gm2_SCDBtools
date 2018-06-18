"""
plot_averages.py

Python script to make some plots of the average temperatue by magnet sector.

M. Eads
June 2017
"""

import SCDButil
import ROOT
import time

time_interval = 'all'
avg_interval = 600.0

if time_interval == 'hour':
        begTime = time.time() - 3600
elif time_interval == 'day':
        begTime = time.time() - 86400
elif time_interval == 'week':
        begTime = time.time() - 604800
elif time_interval == 'month':
        begTime = time.time() - 2678400
elif time_interval == 'year':
        begTime = time.time() - 31536000
elif time_interval == 'all':
        begTime = time.time() - 315360000



# set up a dictionary with all the channels and indices by magnet sector
d = {}
d['A'] = ('mscb323_Temp_P1', [0, 1, 2])
d['C'] = ('mscb323_Temp_P1', [4, 5, 6])
d['E'] = ('mscb323_Temp_P2', [0, 1, 2])
d['G'] = ('mscb323_Temp_P2', [4, 5, 6])
d['I'] = ('mscb323_Temp_P3', [0, 1, 2])

d['B'] = ('mscb13e_Temp_P1', [0, 1, 2])
d['D'] = ('mscb13e_Temp_P1', [4, 5, 6])
d['F'] = ('mscb13e_Temp_P2', [0, 1, 2])
d['H'] = ('mscb13e_Temp_P2', [4, 5, 6])
d['J'] = ('mscb13e_Temp_P3', [0, 1, 2])

# get the graphs of average temperature by sector
db = SCDButil.SCDButil(calib=True)


#gList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
gList = ['A']


for graph in gList:
    g_avg = ROOT.TGraph()
    g_avg.SetMarkerColor(ROOT.kBlack)
    g_avg.SetLineColor(ROOT.kBlack)

    graphList = []
    diffList = []

    sum = 0.
    num = 0
    i = 0
    j = 0
    while i < 3:

        graphList.append(db.get_average_graph(d[graph][0], d[graph][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime))                 

        diffList.append(ROOT.TGraph())

        if graph == 'A':
            graphList[i].SetMarkerColor(ROOT.kRed+i)
            graphList[i].SetLineColor(ROOT.kRed+i)
            graphList[i].SetFillColor(ROOT.kRed+i)
            diffList[i].SetMarkerColor(ROOT.kRed+i)
            diffList[i].SetLineColor(ROOT.kRed+i)
            diffList[i].SetFillColor(ROOT.kRed+i)
       	elif graph == 'B':
            graphList[i].SetMarkerColor(ROOT.kOrange+i)
       	    graphList[i].SetLineColor(ROOT.kOrange+i)
            graphList[i].SetFillColor(ROOT.kOrange+i)
            diffList[i].SetMarkerColor(ROOT.kOrange+i)
            diffList[i].SetLineColor(ROOT.kOrange+i)
            diffList[i].SetFillColor(ROOT.kOrange+i)
       	elif graph == 'C':
            graphList[i].SetMarkerColor(ROOT.kYellow+i)
       	    graphList[i].SetLineColor(ROOT.kYellow+i)
            graphList[i].SetFillColor(ROOT.kYellow+1)
            diffList[i].SetMarkerColor(ROOT.kYellow+i)
            diffList[i].SetLineColor(ROOT.kYellow+i)
            diffList[i].SetFillColor(ROOT.kYellow+1)
       	elif graph == 'D':
            graphList[i].SetMarkerColor(ROOT.kGreen+i)
       	    graphList[i].SetLineColor(ROOT.kGreen+i)
            graphList[i].SetFillColor(ROOT.kGreen+i)
            diffList[i].SetMarkerColor(ROOT.kGreen+i)
            diffList[i].SetLineColor(ROOT.kGreen+i)
       	    diffList[i].SetFillColor(ROOT.kGreen+i)
       	elif graph == 'E':
            graphList[i].SetMarkerColor(ROOT.kTeal+i)
       	    graphList[i].SetLineColor(ROOT.kTeal+i)
            graphList[i].SetFillColor(ROOT.kTeal+i)
            diffList[i].SetMarkerColor(ROOT.kTeal+i)
            diffList[i].SetLineColor(ROOT.kTeal+i)
       	    diffList[i].SetFillColor(ROOT.kTeal+i)
       	elif graph == 'F':
            graphList[i].SetMarkerColor(ROOT.kCyan+i)
       	    graphList[i].SetLineColor(ROOT.kCyan+i)
            graphList[i].SetFillColor(ROOT.kCyan+i)
            diffList[i].SetMarkerColor(ROOT.kCyan+i)
            diffList[i].SetLineColor(ROOT.kCyan+i)
       	    diffList[i].SetFillColor(ROOT.kCyan+i)
       	elif graph == 'G':
            graphList[i].SetMarkerColor(ROOT.kAzure+i)
       	    graphList[i].SetLineColor(ROOT.kAzure+i)
            graphList[i].SetFillColor(ROOT.kAzure+i)
            diffList[i].SetMarkerColor(ROOT.kAzure+i)
            diffList[i].SetLineColor(ROOT.kAzure+i)
            diffList[i].SetFillColor(ROOT.kAzure+i)
       	elif graph == 'H':
            graphList[i].SetMarkerColor(ROOT.kBlue+i)
       	    graphList[i].SetLineColor(ROOT.kBlue+i)
            graphList[i].SetFillColor(ROOT.kBlue+i)
            diffList[i].SetMarkerColor(ROOT.kBlue+i)
            diffList[i].SetLineColor(ROOT.kBlue+i)
            diffList[i].SetFillColor(ROOT.kBlue+i)
       	elif graph == 'I':
            graphList[i].SetMarkerColor(ROOT.kViolet+i)
       	    graphList[i].SetLineColor(ROOT.kViolet+i)
            graphList[i].SetFillColor(ROOT.kViolet+i)
            diffList[i].SetMarkerColor(ROOT.kViolet+i)
            diffList[i].SetLineColor(ROOT.kViolet+i)
            diffList[i].SetFillColor(ROOT.kViolet+i)
       	elif graph == 'J':
            graphList[i].SetMarkerColor(ROOT.kMagenta+i)
       	    graphList[i].SetLineColor(ROOT.kMagenta+i)
            graphList[i].SetFillColor(ROOT.kMagenta+i)
            diffList[i].SetMarkerColor(ROOT.kMagenta+i)
            diffList[i].SetLineColor(ROOT.kMagenta+i)
            diffList[i].SetFillColor(ROOT.kMagenta+i)
        i += 1

    
    for j in range(graphList[0].GetN()):
        x = ROOT.Double()
        y = ROOT.Double()
        
        sum = 0.
        num = 0
        k = 0
        while k < 3:
            graphList[k].GetPoint(j, x, y)
            sum += y
            num += 1
            k += 1
        avg = sum/num
        g_avg.SetPoint(j, x, avg)

        for n in range(0,3):
            if graphList[n].GetN() != 0:
                graphList[n].GetPoint(j, x, y)
                diffList[n].SetPoint(j, x, y-avg)

    graphList.append(g_avg)


    mgcanvas = ROOT.TCanvas(graph + '_' + time_interval + '_canvas', graph + '_' + time_interval + '_canvas', 1)
    
    mg = ROOT.TMultiGraph()
    mg.SetTitle('Magnet ' + graph + ': Averages')    

    for gr in graphList:
        mg.Add(gr)


    mg.Draw('ap')
    mg.GetXaxis().SetTimeDisplay(1)
    mg.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
    mg.GetXaxis().SetLabelSize(0.025)
    mg.GetXaxis().SetLabelOffset(0.02)
    mg.GetYaxis().SetTitle('Temperature (#circ C)')
    mg.GetYaxis().SetTitleOffset(1.3)

    legmg = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
    legmg.AddEntry(graphList[0], graph + ' Top', 'f')
    legmg.AddEntry(graphList[1], graph + ' Mid', 'f')
    legmg.AddEntry(graphList[2], graph + ' Bot', 'f')
    legmg.AddEntry(graphList[3], graph + ' Avg', 'f')
    legmg.Draw()

    mgcanvas.SaveAs(graph + '_' + time_interval + '_averages.pdf')
   
    
    mgdcanvas = ROOT.TCanvas(graph + '_' + time_interval + '_avg_canvas', graph + '_' + time_interval + '_avg_canvas', 1)

    mgd = ROOT.TMultiGraph()
    mgd.SetTitle('Magnet ' + graph + ': Deviation from avg')    

    for dr in diffList:
        mgd.Add(dr)

    mgd.Draw('ap')
    mgd.GetXaxis().SetTimeDisplay(1)
    mgd.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
    mgd.GetXaxis().SetLabelSize(0.025)
    mgd.GetXaxis().SetLabelOffset(0.02)
    mgd.GetYaxis().SetTitle('Temperature Difference (#circ C)')
    mgd.GetYaxis().SetTitleOffset(1.3)

    legmgd = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
    legmgd.AddEntry(graphList[0], graph + ' Top', 'f')
    legmgd.AddEntry(graphList[1], graph + ' Mid', 'f')
    legmgd.AddEntry(graphList[2], graph + ' Bot', 'f')
    legmgd.Draw()

    mgdcanvas.SaveAs(graph + '_' + time_interval + '_differences.pdf')
