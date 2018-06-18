"""
plot_averages.py

Python script to make some plots of the average temperatue by magnet sector.

M. Eads
June 2017
"""

import SCDButil
import ROOT
import time

time_interval = 'month'
avg_interval = 600.0
i = 0

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
while i < 3:
	gA = db.get_average_graph(d['A'][0], d['A'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gB = db.get_average_graph(d['B'][0], d['B'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gC = db.get_average_graph(d['C'][0], d['C'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gD = db.get_average_graph(d['D'][0], d['D'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gE = db.get_average_graph(d['E'][0], d['E'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gF = db.get_average_graph(d['F'][0], d['F'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gG = db.get_average_graph(d['G'][0], d['G'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gH = db.get_average_graph(d['H'][0], d['H'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gI = db.get_average_graph(d['I'][0], d['I'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	gJ = db.get_average_graph(d['J'][0], d['J'][1][i], time_interval=time_interval, avg_interval=avg_interval, begTime=begTime)
	i += 1

dA = ROOT.TGraph()
dB = ROOT.TGraph()
dC = ROOT.TGraph()
dD = ROOT.TGraph()
dE = ROOT.TGraph()
dF = ROOT.TGraph()
dG = ROOT.TGraph()
dH = ROOT.TGraph()
dI = ROOT.TGraph()
dJ = ROOT.TGraph()


c1 = ROOT.TCanvas('c1','c1', 1)

gA.SetMarkerColor(ROOT.kRed)
gB.SetMarkerColor(ROOT.kOrange)
gC.SetMarkerColor(ROOT.kYellow)
gD.SetMarkerColor(ROOT.kGreen)
gE.SetMarkerColor(ROOT.kTeal)
gF.SetMarkerColor(ROOT.kCyan)
gG.SetMarkerColor(ROOT.kAzure)
gH.SetMarkerColor(ROOT.kBlue)
gI.SetMarkerColor(ROOT.kViolet)
gJ.SetMarkerColor(ROOT.kMagenta)
gA.SetLineColor(ROOT.kRed)
gB.SetLineColor(ROOT.kOrange)
gC.SetLineColor(ROOT.kYellow)
gD.SetLineColor(ROOT.kGreen)
gE.SetLineColor(ROOT.kTeal)
gF.SetLineColor(ROOT.kCyan)
gG.SetLineColor(ROOT.kAzure)
gH.SetLineColor(ROOT.kBlue)
gI.SetLineColor(ROOT.kViolet)
gJ.SetLineColor(ROOT.kMagenta)

dA.SetMarkerColor(ROOT.kRed)
dB.SetMarkerColor(ROOT.kOrange)
dC.SetMarkerColor(ROOT.kYellow)
dD.SetMarkerColor(ROOT.kGreen)
dE.SetMarkerColor(ROOT.kTeal)
dF.SetMarkerColor(ROOT.kCyan)
dG.SetMarkerColor(ROOT.kAzure)
dH.SetMarkerColor(ROOT.kBlue)
dI.SetMarkerColor(ROOT.kViolet)
dJ.SetMarkerColor(ROOT.kMagenta)
dA.SetLineColor(ROOT.kRed)
dB.SetLineColor(ROOT.kOrange)
dC.SetLineColor(ROOT.kYellow)
dD.SetLineColor(ROOT.kGreen)
dE.SetLineColor(ROOT.kTeal)
dF.SetLineColor(ROOT.kCyan)
dG.SetLineColor(ROOT.kAzure)
dH.SetLineColor(ROOT.kBlue)
dI.SetLineColor(ROOT.kViolet)
dJ.SetLineColor(ROOT.kMagenta)

mg = ROOT.TMultiGraph()
mg.SetTitle('Magnet Sector Averages - ' + time_interval)
mg.Add(gA)
mg.Add(gB)
mg.Add(gC)
mg.Add(gD)
mg.Add(gE)
mg.Add(gF)
mg.Add(gG)
mg.Add(gH)
mg.Add(gI)
mg.Add(gJ)

mg.Draw('ap')
mg.GetXaxis().SetTimeDisplay(1)
mg.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
mg.GetXaxis().SetLabelSize(0.025)
mg.GetXaxis().SetLabelOffset(0.02)
mg.GetYaxis().SetTitle('Temperature (#circ C)')
mg.GetYaxis().SetTitleOffset(1.3)

leg = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
leg.AddEntry(gA, 'Sector A', 'l')
leg.AddEntry(gB, 'Sector B', 'l')
leg.AddEntry(gC, 'Sector C', 'l')
leg.AddEntry(gD, 'Sector D', 'l')
leg.AddEntry(gE, 'Sector E', 'l')
leg.AddEntry(gF, 'Sector F', 'l')
leg.AddEntry(gG, 'Sector G', 'l')
leg.AddEntry(gH, 'Sector H', 'l')
leg.AddEntry(gI, 'Sector I', 'l')
leg.AddEntry(gJ, 'Sector J', 'l')
leg.Draw()

# make a graph of the overall average
canvas = ROOT.TCanvas('average_' + time_interval + '_canvas', 'average_' + time_interval + '_canvas', 1)
g_avg = ROOT.TGraph()
for i in range(gA.GetN()):
    x = ROOT.Double()
    y = ROOT.Double()

    sum = 0.
    num = 0
    for graph in [gA, gB, gC, gD, gE, gF, gG, gH, gI, gJ]:
        graph.GetPoint(i, x, y)
        sum += y
        num += 1

    avg = sum/num
    g_avg.SetPoint(i, x, avg)

    gA.GetPoint(i, x, y)
    dA.SetPoint(i, x, y-avg)
    gB.GetPoint(i, x, y)
    dB.SetPoint(i, x, y-avg)
    gC.GetPoint(i, x, y)
    dC.SetPoint(i, x, y-avg)
    gD.GetPoint(i, x, y)
    dD.SetPoint(i, x, y-avg)
    gE.GetPoint(i, x, y)
    dE.SetPoint(i, x, y-avg)
    gF.GetPoint(i, x, y)
    dF.SetPoint(i, x, y-avg)
    gG.GetPoint(i, x, y)
    dG.SetPoint(i, x, y-avg)
    gH.GetPoint(i, x, y)
    dH.SetPoint(i, x, y-avg)
    gI.GetPoint(i, x, y)
    dI.SetPoint(i, x, y-avg)
    gJ.GetPoint(i, x, y)
    dJ.SetPoint(i, x, y-avg)



leg.AddEntry(g_avg, 'Average', 'p')
g_avg.Draw('p same')
c1.SaveAs('Differences_' + time_interval + '.pdf')

c2 = ROOT.TCanvas('c2', 'c2', 1)
mgd = ROOT.TMultiGraph()
mgd.SetTitle('Magnet Sectors: Deviation from avg - ' + time_interval)
mgd.Add(dA)
mgd.Add(dB)
mgd.Add(dC)
mgd.Add(dD)
mgd.Add(dE)
mgd.Add(dF)
mgd.Add(dG)
mgd.Add(dH)
mgd.Add(dI)
mgd.Add(dJ)
mgd.Draw('ap')
mgd.GetXaxis().SetTimeDisplay(1)
mgd.GetXaxis().SetTimeFormat('#splitline{%b-%d}{%H:%M}')
mgd.GetXaxis().SetLabelSize(0.025)
mgd.GetXaxis().SetLabelOffset(0.02)
mgd.GetYaxis().SetTitle('Temperature Difference (#circ C)')
mgd.GetYaxis().SetTitleOffset(1.3)

leg2 = ROOT.TLegend(0.85, 0.65, 0.95, 0.95)
leg2.AddEntry(dA, 'Sector A', 'l')
leg2.AddEntry(dB, 'Sector B', 'l')
leg2.AddEntry(dC, 'Sector C', 'l')
leg2.AddEntry(dD, 'Sector D', 'l')
leg2.AddEntry(dE, 'Sector E', 'l')
leg2.AddEntry(dF, 'Sector F', 'l')
leg2.AddEntry(dG, 'Sector G', 'l')
leg2.AddEntry(dH, 'Sector H', 'l')
leg2.AddEntry(dI, 'Sector I', 'l')
leg2.AddEntry(dJ, 'Sector J', 'l')
leg2.Draw()

c2.SaveAs('Deviation_' + time_interval + '.pdf')

