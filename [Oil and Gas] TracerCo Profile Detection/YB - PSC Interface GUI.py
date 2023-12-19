### DEFINE IMPORTS ###

# Import Tkinter for GUI interface 
import tkinter as tk
# Import PI ODBC database connection
import CNRLPIconnect.ODBCconnect as md # "make data"
ODBCconnection = md.ODBCServer("ALBIANPI") # Live data connection to plant data via ODBC

import pandas as pd
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
from functools import partial
from tkcalendar import Calendar, DateEntry
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter.font as tkFont
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

##### DEFINE HYPERPARAMETERS #####
minimumArraySize = 3
minimumFrothThreshold = 300

# Hyperparameter that defines the maximum density to be considered a plugged tube
pluggedTubeHP = 1400
# Z-score to filter any outliers on first pass
zScoreHP_1 = 3
# Z-score to filter any outliers on the second pass
zScoreHP_2 = 1.5
# Used to separate the headspace from the froth/middlings - clustering algorithm
bulkDifferenceThreshold = 500
# Used to analyze froth/middlings layer in froth/middlings - slope method
pairedDifferenceThreshold = 20
slopeThreshold = 20
# Hyperparameter for trace threshold - sigmoid method
traceThreshold_1 = 300
traceThreshold_2 = 1000000

historicalData = []
processedResults = []
index = 0


class interfaceWindow:
    def __init__(self, window):
        
        '''
        self.f, self.ax = plt.subplots(figsize=(8, 5))
        sns.set_context(rc={"lines.linewidth": 3})

        self.canvas = FigureCanvasTkAgg(self.f, window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 4, rowspan = 12, sticky='NS')
        '''
        #fontBody = tkFont.Font(family="Arial", size=12)
        
        # Initialize buttons and labels
        
        ## DISABLE COMPANY LOGO
        # self.imageLogo = ImageTk.PhotoImage(Image.open(r'\\cnrl.com\cnrl\users\tommych\Desktop\1200px-Logo.svg.png').resize((100, 41)))
        # self.logo = tk.Label(window, image=self.imageLogo)
        # self.logo.image = self.imageLogo
        # self.logo.grid(row = 0, column = 1)
        self.title=tk.Label(window, text='PSC Detection Tool', font = ('Arial Narrow', 16, 'bold')).grid(row = 0, column = 2)
        
        self.pscSelection = tk.StringVar(window)
        self.startDateLabel=tk.Label(window, text='Select PSC').grid(row = 1, column = 1)
        self.pscSelection.set("No Selection") # default value
        self.pscSelectBox = tk.OptionMenu(window, self.pscSelection, "MRM PSC 1", "MRM PSC 2", "JPM PSC")
        self.pscSelectBox.grid(row = 1, column = 2)
        
        self.startDate = tk.StringVar(window)
        self.startDate.set("YYYY-MM-DD")
        self.startTime = tk.StringVar(window)
        self.startTime.set("HH:MM:SS AM/PM")
        self.endDate = tk.StringVar(window)
        self.endDate.set("YYYY-MM-DD")
        self.endTime = tk.StringVar(window)
        self.endTime.set("HH:MM:SS AM/PM")
        self.modeText = tk.StringVar(window)
        self.perFoundText = tk.StringVar(window)
        self.intFoundText = tk.StringVar(window)
        self.startDateCalendar = partial(self.calendar, "start")
        self.endDateCalendar = partial(self.calendar, "end")
       
        self.startDateLabel=tk.Label(window, text='Start Date:').grid(row = 2, column = 1)
        self.startDateBox=tk.Entry(textvariable=self.startDate).grid(row = 2, column = 2)
        self.startTimeLabel=tk.Label(window, text='Start Time:').grid(row = 3, column = 1)
        self.startTimeBox=tk.Entry(textvariable=self.startTime).grid(row = 3, column = 2)
        self.endDateLabel=tk.Label(window, text='End Date:').grid(row = 4, column = 1)
        self.endDateBox=tk.Entry(textvariable=self.endDate).grid(row = 4, column = 2)
        self.endTimeLabel=tk.Label(window, text='End Time:').grid(row = 5, column = 1)
        self.endTimeBox=tk.Entry(textvariable=self.endTime).grid(row = 5, column = 2)
        self.startDateButton = tk.Button(window, 
                           text="-", 
                           width=3,
                           height=1,
                           command=self.startDateCalendar).grid(row = 2, column = 3)
        self.endDateButton = tk.Button(window, 
                           text="-", 
                           width=3,
                           height=1,
                           command=self.endDateCalendar).grid(row = 4, column = 3)
        self.perFoundLabel=tk.Label(window, text='Percent Found (%):').grid(row = 6, column = 1)
        self.perFoundBox=tk.Entry(textvariable=self.perFoundText).grid(row = 6, column = 2)
        self.interfaceFoundLabel=tk.Label(window, text='Interface Found:').grid(row = 7, column = 1)
        self.interfaceFoundBox=tk.Entry(textvariable=self.intFoundText).grid(row = 7, column = 2)
        self.modeLabel=tk.Label(window, textvariable = self.modeText, font = ('Arial Narrow', 12, 'bold')).grid(row = 9, column = 1, columnspan = 3)
        self.leftBorder=tk.Label(window, background='grey37').grid(row = 0, column = 0, rowspan = 12, sticky='NS', ipadx = 5)
        self.leftPad=tk.Label(window).grid(row = 11, column = 0, columnspan = 2, ipady = 200)
        
        self.historicalButton = tk.Button(window, 
                           text="Get Historical", 
                           fg="Black",
                           width=20,
                           height=5,
                           command=self.getHistorical)
        self.liveButton = tk.Button(window, 
                           text="Live Mode", 
                           fg="Black",
                           width=20,
                           height=5,
                           command=quit)
        self.nextButton = tk.Button(window, 
                           text="Next", 
                           fg="Black",
                           command=self.renderNext)
        self.backButton = tk.Button(window, 
                           text="Back", 
                           fg="Black",
                           command=self.renderBack)

        self.historicalButton.grid(row = 8, column = 1)
        self.liveButton.grid(row = 8, column = 2)
        self.backButton.grid(row = 10, column = 1)
        self.nextButton.grid(row = 10, column = 2)
        
        # Initialize calendar
    def calendar(self, startend):
        def print_sel():
            if startend == "start":
                self.startDate.set(self.cal.selection_get())
            else:
                self.endDate.set(self.cal.selection_get())
        top = tk.Toplevel(window)
        self.cal = Calendar(top,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2020, month=1, day=1)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(top, text="Select", command=print_sel).pack()

        
    def getData(self, pscSelection, startDate, endDate):
        if pscSelection == "MRM PSC 1":
            tagMap = {"247CP01:240DT1111_1.LIN":"1",
            "247CP01:240DT1111_2.LIN":"2",
            "247CP01:240DT1111_3.LIN":"3",
            "247CP01:240DT1111_4.LIN":"4",
            "247CP01:240DT1111_5.LIN":"5",
            "247CP01:240DT1111_6.LIN":"6",
            "247CP01:240DT1111_7.LIN":"7",
            "247CP01:240DT1111_8.LIN":"8",
            "247CP01:240DT1111_9.LIN":"9",
            "247CP01:240DT1111_10.LIN":"10",
            "247CP01:240DT1111_11.LIN":"11",
            "247CP01:240DT1111_12.LIN":"12",
            "247CP01:240DT1111_13.LIN":"13",
            "247CP01:240DT1111_14.LIN":"14",
            "247CP01:240DT1111_15.LIN":"15",
            "247CP01:240DT1111_16.LIN":"16",
            "247CP01:240DT1111_17.LIN":"17",
            "247CP01:240DT1111_18.LIN":"18",
            "247CP01:240DT1111_19.LIN":"19",
            "247CP01:240DT1111_20.LIN":"20",
            "247CP01:240DT1111_21.LIN":"21",
            "247CP01:240DT1111_22.LIN":"22",
            "247CP01:240DT1111_23.LIN":"23",
            "247CP01:240DT1111_24.LIN":"24",
            "247CP01:240DT1111_25.LIN":"25",
            "247CP01:240DT1111_26.LIN":"26",
            "247CP01:240DT1111_27.LIN":"27",
            "247CP01:240DT1111_28.LIN":"28",
            "247CP01:240DT1111_29.LIN":"29",
            "247CP01:240DT1111_30.LIN":"30",
            "247CP01:240DT1111_31.LIN":"31",
            "247CP01:240DT1111_32.LIN":"32",
            "247CP01:240DT1111_33.LIN":"33",
            "247CP01:240DT1111_34.LIN":"34",
            "247CP01:240DT1111_35.LIN":"35",
            "247CP01:240DT1111_36.LIN":"36",
            "247CP01:240DT1111_37.LIN":"37",
            "247CP01:240DT1111_38.LIN":"38",
            "247CP01:240DT1111_39.LIN":"39",
            "247CP01:240DT1111_40.LIN":"40",
            "247CP01:240DT1111_41.LIN":"41",
            "247CP01:240DT1111_42.LIN":"42",
            "247CP01:240DT1111_43.LIN":"43",
            "247CP01:240DT1111_44.LIN":"44",
            "247CP01:240DT1111_45.LIN":"45",
            "247CP01:240DT1111_46.LIN":"46",
            "247CP01:240DT1111_47.LIN":"47",
            "247CP01:240DT1111_48.LIN":"48",
            "247CP01:240DT1111_49.LIN":"49",
            "247CP01:240DT1111_50.LIN":"50",
            "247CP01:240DT1111_51.LIN":"51",
            "247CP01:240DT1111_52.LIN":"52",
            "247CP01:240DT1111_53.LIN":"53",
            "247CP01:240DT1111_54.LIN":"54",
            "247CP01:240DT1111_55.LIN":"55",
            "247CP01:240DT1111_56.LIN":"56",
            "247CP01:240DT1111_57.LIN":"57",
            "247CP01:240DT1111_58.LIN":"58",
            "247CP01:240DT1111_59.LIN":"59",
            "247CP01:240DT1111_60.LIN":"60",
            "247CP01:240DT1111_61.LIN":"61",
            "247CP01:240DT1111_62.LIN":"62",
            "247CP01:240DT1111_63.LIN":"63",
            "247CP01:240DT1111_64.LIN":"64",
            "247CP01:240DT1111_65.LIN":"65",
            "247CP01:240DT1111_66.LIN":"66",
            "247CP01:240DT1111_67.LIN":"67",
            "247CP01:240DT1111_68.LIN":"68",
            "247CP01:240DT1111_69.LIN":"69",
            "247CP01:240DT1111_70.LIN":"70",
            "247CP01:240DT1111_71.LIN":"71",
            "247CP01:240DT1111_72.LIN":"72",
            "247CP01:240DT1111_73.LIN":"73",
            "247CP01:240DT1111_74.LIN":"74",
            "247CP01:240DT1111_75.LIN":"75",
            "247CP01:240DT1111_76.LIN":"76",
            "247CP01:240DT1111_77.LIN":"77",
            "247CP01:240DT1111_78.LIN":"78",
            "247CP01:240DT1111_79.LIN":"79",
            "247CP01:240DT1111_80.LIN":"80",
            "247CP01:240DT1111_81.LIN":"81",
            "247CP01:240DT1111_82.LIN":"82",
            "247CP01:240DT1111_83.LIN":"83",
            "247CP01:240DT1111_84.LIN":"84",
            "247CP01:240DT1111_85.LIN":"85",
            "247CP01:240DT1111_86.LIN":"86",
            "247CP01:240DT1111_87.LIN":"87",
            "247CP01:240DT1111_88.LIN":"88"}
        elif pscSelection == "MRM PSC 2":
            tagMap = {"247CP02:240DT2111_1.LIN":"1",
            "247CP02:240DT2111_2.LIN":"2",
            "247CP02:240DT2111_3.LIN":"3",
            "247CP02:240DT2111_4.LIN":"4",
            "247CP02:240DT2111_5.LIN":"5",
            "247CP02:240DT2111_6.LIN":"6",
            "247CP02:240DT2111_7.LIN":"7",
            "247CP02:240DT2111_8.LIN":"8",
            "247CP02:240DT2111_9.LIN":"9",
            "247CP02:240DT2111_10.LIN":"10",
            "247CP02:240DT2111_11.LIN":"11",
            "247CP02:240DT2111_12.LIN":"12",
            "247CP02:240DT2111_13.LIN":"13",
            "247CP02:240DT2111_14.LIN":"14",
            "247CP02:240DT2111_15.LIN":"15",
            "247CP02:240DT2111_16.LIN":"16",
            "247CP02:240DT2111_17.LIN":"17",
            "247CP02:240DT2111_18.LIN":"18",
            "247CP02:240DT2111_19.LIN":"19",
            "247CP02:240DT2111_20.LIN":"20",
            "247CP02:240DT2111_21.LIN":"21",
            "247CP02:240DT2111_22.LIN":"22",
            "247CP02:240DT2111_23.LIN":"23",
            "247CP02:240DT2111_24.LIN":"24",
            "247CP02:240DT2111_25.LIN":"25",
            "247CP02:240DT2111_26.LIN":"26",
            "247CP02:240DT2111_27.LIN":"27",
            "247CP02:240DT2111_28.LIN":"28",
            "247CP02:240DT2111_29.LIN":"29",
            "247CP02:240DT2111_30.LIN":"30",
            "247CP02:240DT2111_31.LIN":"31",
            "247CP02:240DT2111_32.LIN":"32",
            "247CP02:240DT2111_33.LIN":"33",
            "247CP02:240DT2111_34.LIN":"34",
            "247CP02:240DT2111_35.LIN":"35",
            "247CP02:240DT2111_36.LIN":"36",
            "247CP02:240DT2111_37.LIN":"37",
            "247CP02:240DT2111_38.LIN":"38",
            "247CP02:240DT2111_39.LIN":"39",
            "247CP02:240DT2111_40.LIN":"40",
            "247CP02:240DT2111_41.LIN":"41",
            "247CP02:240DT2111_42.LIN":"42",
            "247CP02:240DT2111_43.LIN":"43",
            "247CP02:240DT2111_44.LIN":"44",
            "247CP02:240DT2111_45.LIN":"45",
            "247CP02:240DT2111_46.LIN":"46",
            "247CP02:240DT2111_47.LIN":"47",
            "247CP02:240DT2111_48.LIN":"48",
            "247CP02:240DT2111_49.LIN":"49",
            "247CP02:240DT2111_50.LIN":"50",
            "247CP02:240DT2111_51.LIN":"51",
            "247CP02:240DT2111_52.LIN":"52",
            "247CP02:240DT2111_53.LIN":"53",
            "247CP02:240DT2111_54.LIN":"54",
            "247CP02:240DT2111_55.LIN":"55",
            "247CP02:240DT2111_56.LIN":"56",
            "247CP02:240DT2111_57.LIN":"57",
            "247CP02:240DT2111_58.LIN":"58",
            "247CP02:240DT2111_59.LIN":"59",
            "247CP02:240DT2111_60.LIN":"60",
            "247CP02:240DT2111_61.LIN":"61",
            "247CP02:240DT2111_62.LIN":"62",
            "247CP02:240DT2111_63.LIN":"63",
            "247CP02:240DT2111_64.LIN":"64",
            "247CP02:240DT2111_65.LIN":"65",
            "247CP02:240DT2111_66.LIN":"66",
            "247CP02:240DT2111_67.LIN":"67",
            "247CP02:240DT2111_68.LIN":"68",
            "247CP02:240DT2111_69.LIN":"69",
            "247CP02:240DT2111_70.LIN":"70",
            "247CP02:240DT2111_71.LIN":"71",
            "247CP02:240DT2111_72.LIN":"72",
            "247CP02:240DT2111_73.LIN":"73",
            "247CP02:240DT2111_74.LIN":"74",
            "247CP02:240DT2111_75.LIN":"75",
            "247CP02:240DT2111_76.LIN":"76",
            "247CP02:240DT2111_77.LIN":"77",
            "247CP02:240DT2111_78.LIN":"78",
            "247CP02:240DT2111_79.LIN":"79",
            "247CP02:240DT2111_80.LIN":"80",
            "247CP02:240DT2111_81.LIN":"81",
            "247CP02:240DT2111_82.LIN":"82",
            "247CP02:240DT2111_83.LIN":"83",
            "247CP02:240DT2111_84.LIN":"84",
            "247CP02:240DT2111_85.LIN":"85",
            "247CP02:240DT2111_86.LIN":"86",
            "247CP02:240DT2111_87.LIN":"87",
            "247CP02:240DT2111_88.LIN":"88"}
        else:
            tagMap = {"240DI4401.PV":"1",
                "240DI4402.PV":"2",
                "240DI4403.PV":"3",
                "240DI4404.PV":"4",
                "240DI4405.PV":"5",
                "240DI4406.PV":"6",
                "240DI4407.PV":"7",
                "240DI4408.PV":"8",
                "240DI4409.PV":"9",
                "240DI4410.PV":"10",
                "240DI4411.PV":"11",
                "240DI4412.PV":"12",
                "240DI4413.PV":"13",
                "240DI4414.PV":"14",
                "240DI4415.PV":"15",
                "240DI4416.PV":"16",
                "240DI4417.PV":"17",
                "240DI4418.PV":"18",
                "240DI4419.PV":"19",
                "240DI4420.PV":"20",
                "240DI4421.PV":"21",
                "240DI4422.PV":"22",
                "240DI4423.PV":"23",
                "240DI4424.PV":"24",
                "240DI4425.PV":"25",
                "240DI4426.PV":"26",
                "240DI4427.PV":"27",
                "240DI4428.PV":"28",
                "240DI4429.PV":"29",
                "240DI4430.PV":"30",
                "240DI4431.PV":"31",
                "240DI4432.PV":"32",
                "240DI4433.PV":"33",
                "240DI4434.PV":"34",
                "240DI4435.PV":"35",
                "240DI4436.PV":"36",
                "240DI4437.PV":"37",
                "240DI4438.PV":"38",
                "240DI4439.PV":"39",
                "240DI4440.PV":"40",
                "240DI4441.PV":"41",
                "240DI4442.PV":"42",
                "240DI4443.PV":"43",
                "240DI4444.PV":"44",
                "240DI4445.PV":"45",
                "240DI4446.PV":"46",
                "240DI4447.PV":"47",
                "240DI4448.PV":"48",
                "240DI4449.PV":"49",
                "240DI4450.PV":"50",
                "240DI4451.PV":"51",
                "240DI4452.PV":"52",
                "240DI4453.PV":"53",
                "240DI4454.PV":"54",
                "240DI4455.PV":"55",
                "240DI4456.PV":"56",
                "240DI4457.PV":"57",
                "240DI4458.PV":"58",
                "240DI4459.PV":"59",
                "240DI4460.PV":"60",
                "240DI4461.PV":"61",
                "240DI4462.PV":"62",
                "240DI4463.PV":"63",
                "240DI4464.PV":"64",
                "240DI4465.PV":"65",
                "240DI4466.PV":"66",
                "240DI4467.PV":"67",
                "240DI4468.PV":"68",
                "240DI4469.PV":"69",
                "240DI4470.PV":"70",
                "240DI4471.PV":"71",
                "240DI4472.PV":"72",
                "240DI4473.PV":"73",
                "240DI4474.PV":"74",
                "240DI4475.PV":"75",
                "240DI4476.PV":"76",
                "240DI4477.PV":"77",
                "240DI4478.PV":"78",
                "240DI4479.PV":"79",
                "240DI4480.PV":"80",
                "240DI4481.PV":"81",
                "240DI4482.PV":"82"
                }

        searchTags = list(tagMap.keys())
        ODBCconnection.fetch_tags(searchTags,"").tag_dataframe
        interval = "60m" 
        df_raw = ODBCconnection.fetch_data(startDate,endDate,interval).data
        df = df_raw.copy() 
        df = df.rename(columns = tagMap) 
        
        return df
    
    def goLive(self):
        self.modeText.set("*** LIVE MODE ***")
    
    def getHistorical(self):
        global historicalData
        global processedResults
        
        getPSC = myWindow.pscSelection.get() # i.e. "MRM PSC 1"
        startDate = myWindow.startDate.get() + " " + myWindow.startTime.get() # i.e. "2020-05-01 06:00:00 AM"
        endDate = myWindow.endDate.get() + " " + myWindow.endTime.get() # i.e. "2020-05-01 08:00:00 AM"
        
        # Pull PI Query
        historicalData = myWindow.getData(getPSC, startDate, endDate)
        # Run raw data through algorithm
        processedResults = slopeMethod("Historical", historicalData)
        
        self.modeText.set("*** HISTORICAL MODE ***")
        
        # Determine the average amount of interfaces found
        averageIntFound = 0
        count = 0
        for interface in processedResults:
            averageIntFound = averageIntFound + interface['Output']
            count += 1
        averageIntFound = (averageIntFound / count)*100
        self.perFoundText.set(averageIntFound)
        
        self.renderInformation(0)
        
    
    def renderInformation(self, index):
        plt.clf()
        plt.xlim(0, 1500)
        self.f, self.ax = plt.subplots(figsize=(8, 5))
        sns.set_context(rc={"lines.linewidth": 3})

        self.canvas = FigureCanvasTkAgg(self.f, window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 4, rowspan = 12, sticky='NES')
        
        # Store Date String
        dateString = str(processedResults[index]['Date'])
        
        # Set interface found label
        self.intFoundText.set("True") if processedResults[index]['Output'] == 1 else self.intFoundText.set("False")
        
        # Bar chart information for TracerCo
        origRawData = processedResults[index]['Original Data']
        
        # Get line information to draw straight lines
        slopeLineData = processedResults[index]['Line Data']
        
        # Line information for froth layer
        f1 = lambda x: slopeLineData['Froth Slope']*x + slopeLineData['Froth Intercept']
        x1 = np.array([0,88])
        
        # Line information for middlings layer
        f2 = lambda x: slopeLineData['Middlings Slope']*x + slopeLineData['Middlings Intercept']
        x2 = np.array([0,88])
    
        # Plot bar chart data
        origRawData = origRawData.to_frame()
        origRawData.columns = ['Density (kg/m3)'] 
        origRawData['Tube Number'] = origRawData.index
        origRawData['Tube Number'] = origRawData['Tube Number'].astype(int)
        origRawData = origRawData.sort_values(by=['Tube Number'])
        
        clusterLabels = processedResults[index]['Clustered Labels']
        clusterData = processedResults[index]['Clustered Data']
        clusterData = pd.DataFrame(data=clusterData,index=clusterData[:,0])
        clusterData.columns = ['Tube Number','Density (kg/m3)','Cluster Label']
        clusterData['Tube Number'] = clusterData['Tube Number'].astype(int)
        # clusterData = clusterLabels.sort_values(by=['Tube Number'])
    
        # Create a custom palette for cluster colors
        custom_palette = {}
        # Iterate through the raw dta
        for index, row in origRawData.iterrows():
            # Initialiuze a label - arbitrary set to 9 to catch errors
            label = 9
            
            # Iterate through the cluster data
            for index2, row2 in clusterData.iterrows():
                # Check for a tube match in the filtered data - record cluster label
                if row2['Tube Number'] == int(index):
                    label = row2['Cluster Label']
                    break
            
            # Assign a label based on cluster data
            if label == clusterLabels[1]:
                custom_palette[row['Tube Number']] = 'tan'
            elif label == clusterLabels[2]:
                custom_palette[row['Tube Number']] = 'palegoldenrod'
            elif label == clusterLabels[0]:
                custom_palette[row['Tube Number']] = 'dimgray'
            else:
                custom_palette[row['Tube Number']] = 'black'
        
        tracerCoPlot = sns.barplot(x='Density (kg/m3)', y='Tube Number', data = origRawData, palette=custom_palette, orient = 'h').set_title(dateString);
        frothLine = sns.lineplot(x=f1(x1), y=x1, ax=self.ax, color='blue');
        middlingsLine = sns.lineplot(x=f2(x2), y=x2, ax=self.ax, color='red');
        
        self.canvas.draw()
        
        
    def renderNext(self):
        global index
        try:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
            index = index + 1
            self.renderInformation(index)
        except:
            pass

    
    def renderBack(self):
        global index
        if index > 0:
            try: 
                self.canvas.get_tk_widget().destroy()
                self.canvas = None
                index = index - 1
                self.renderInformation(index)
            except AttributeError: 
                pass 
            



##### DATA PREPROCESSING #####
# Function to scale the data to min max
def scaleData(i):
    scaler = MinMaxScaler()
    scaledData = scaler.fit_transform(i)
    return scaledData

# Function to clean the data
def dataClean(rowData):    
    # Select date and store in dateString then remove date
    dateString = rowData.name
    #rowData = rowData.drop('Index')
    
    # Check if original row data before clustering fails
    hasFailed = checkFailed(rowData)
    
    if hasFailed == False:
        # Clean dataset of plugged tubes - hyperparameter pluggedTubeHP defined above
        rowData = rowData[rowData < pluggedTubeHP]
        # Clean dateset by removing outliers with a z score greater than hyperparameter defined above
        rowData = rowData[(np.abs(stats.zscore(rowData)) < zScoreHP_1)]
    
        # Convert rowData dataframe to numpy array for processing
        rowData = rowData.reset_index().values
        
        # Convert np array to floats
        rowData = rowData.astype(np.float)
    
    return {'Date': dateString, 'Data': rowData}

##### FUNCTION TO CHECK FAILED CONDITIONS #####
def checkFailed(data):
    # Defining a flag variable to catch failed regressions
    hasFailed = False
    
    # Set failed flag if cluster doesn't meet minimum cluster size
    if (len(data) < minimumArraySize):
        hasFailed = True
    elif (all(type(i) == str for i in data)):
        hasFailed = True
    # Set failed flag if froth cluster doesn't meet the minimum froth density threshold (this catches flush scenarios when no middlings is found)
    elif np.mean(np.array(data)) < minimumFrothThreshold or np.mean(np.array(data)) > pluggedTubeHP:
        hasFailed = True
        
    return hasFailed

##### DATA CLUSTERING #####
def clustering(rowData):
    # Defining # of clusters = gas phase + froth phase + middlings phase
    # If no gas phase exists only froth + middlings phase exists - namely for JPM PSC
    if np.amin(rowData[:,1]) > 50:
        numClusters = 2
    else:
        numClusters = 3
    
    # Initialize variables to hold data
    headSpace = numClusters - 1
    froth = numClusters - 1
    middlings = numClusters - 1
    
    # Call the scaling function prior to clustering
    #scaledData = scaleData(rowData) -- disabled for now
    scaledData = rowData
    
    # Cluster data using kMeans
    kmeans = KMeans(n_clusters = numClusters)
    kmeans.fit(scaledData)
    clusterLabels = kmeans.labels_
    
    # Print info on kMeans
    #print(kmeans.cluster_centers_)
    #print(kmeans.labels_)
    
    # Overlap the cluster label with the rowData
    # [:,None] creates an axis of length 1 allow the two arrays to concatenate, axis = 1 stacks the two rows
    rowData = np.concatenate((rowData, clusterLabels[:,None]), axis=1)
    
    # Define empty lists to hold cluster data
    x = {i:[] for i in range(0,numClusters)}
    y = {i:[] for i in range(0,numClusters)}
    
    # Iterate through each cluster and add the data to each cluster
    for i in range(0, len(rowData)):
        for j in range(0, numClusters):
            if rowData[i,2] == j:
               x[j].append(rowData[i,0])
               y[j].append(rowData[i,1])
               break

    # Final clean algorithm to clean the froth + middlings layers -- iterate through each cluster and remove outliers
    for i in range(0, numClusters):
        j = 0
        while True:
            # Exit loop if we are at the last index or list length is only 1
            if j >= (len(x[i])) or len(x[i]) == 1:
                break
            # Calculate the z score of the entry relative to the z-score threshold for the second filter zScoreHP_2
            # Pass filter over 'x' values i.e. if tube 1,2,3,40 were in the same cluster - the 40th tube should be removed
            # Pass filter over 'y' values i.e. if there is an anomalous tube reading 1500 in the middlings cluster it should be removed
            if abs(x[i][j] -  np.mean(np.array(x[i])))/np.std(np.array(x[i])) < zScoreHP_2:
                if abs(y[i][j] -  np.mean(np.array(y[i])))/np.std(np.array(y[i])) < zScoreHP_2:
                    j += 1
                    continue    
                else:
                    del x[i][j]
                    del y[i][j]
                    j += 1
            else:
                del x[i][j]
                del y[i][j]
                j += 1

    # Rank bulk densities to determine which cluster is the headspace, and whether the froth and middlings exist
    for i in range(0, round(numClusters/2)):
        for j in range(round(numClusters/2),numClusters):
            # Calculate the bulk density difference between each cluster
            bulkDifference = abs((np.mean(np.array(y[i]))-np.mean(np.array(y[j]))))
            if (bulkDifference > bulkDifferenceThreshold) and (numClusters > 2): # only run initial compairson if there are more than 2 clusters
                if np.mean(np.array(y[i])) > np.mean(np.array(y[j])):
                    headSpace = j 
                else:
                    headSpace = i

            else: # for 2 clusters - simply compare the two clusters to determine froth/middlings layer
                if np.mean(np.array(y[i])) > np.mean(np.array(y[j])):
                    middlings = i
                    froth = j
                else:
                    middlings = j
                    froth = i
    # Return cluster assignments + labels
    clusterLabels = [headSpace, froth, middlings]
    clusterData = rowData
    
    return {'Froth X': x[froth], 'Froth Y': y[froth], 'Middlings X': x[middlings], 'Middlings Y': y[middlings], 'Head X': x[headSpace], 'Head Y': y[headSpace], 'Clustered Data': clusterData, 'Clustered Labels': clusterLabels}

##### SLOPE METHOD ALGORITHM #####
def slopeMethod(mode, rawData = None):
    # Define a results list
    results = []
    
    #if mode == "Live":
        ### Convert live data to a pandas dataframe with a single line
    
    
    # Loop through each timestamp
    for j in range(0,len(rawData.index)):
        lineData = []
    
        # Call cleaning function
        origData = rawData.iloc[ j , : ]
        # Before cleaning ensure list contains only ints or floats
        origData = origData.astype(float)
        '''
        if (isinstance(x, str) for x in origData):
            hasFailed = True
        else:
        '''
        # Store clean data
        rowData = dataClean(origData)
        # Store date
        dateString = rowData['Date']
        # Pass filtered + scaled row data to clustering function
        rowData = clustering(rowData['Data'])
        clusterLabels = rowData['Clustered Labels']
        clusterData = rowData['Clustered Data']
        
        #xHead = rowData['Head X']
        #yHead = rowData['Head Y'] 
        xFroth = rowData['Froth X']
        yFroth = rowData['Froth Y']
        xMiddlings = rowData['Middlings X']
        yMiddlings = rowData['Middlings Y']
        
        # Pass clustered data to check if clustering failed
        hasFailed = checkFailed(yFroth)
        if hasFailed == False:
            hasFailed = checkFailed(yMiddlings)

        if hasFailed == False:
            # Calculate a paired difference statistics between middlings and froth bulk densities
            pairedDifferenceStat = abs((np.mean(np.array(yMiddlings))-np.mean(np.array(yFroth)))/np.sqrt((np.std(np.array(yMiddlings))**2/len(yMiddlings))+(np.std((np.array(yFroth)))**2/len(yFroth))))
            
            # Temp array to store array reversal for weighted linear regression
            # Values furthest away from the interface are weighted more
            tempArray = xMiddlings
            tempArray = list(reversed(tempArray))
        
            # Perform linear regression on the middlings and froth clusters
            # Linear regression is weighted so bundles near the interface are weighted more
            # Weighted linear regression - weights the error more on certain samples - multipled to the error
            middlingsRegression = LinearRegression().fit(np.array(xMiddlings).reshape(-1,1), np.array(yMiddlings), sample_weight=tempArray)
            frothRegression = LinearRegression().fit(np.array(xFroth).reshape(-1,1), np.array(yFroth), sample_weight=np.array(xFroth))
            
            # DEFINITION OF CLEAR INTERFACE = DISCONTINOUS BREAK @ FROTH/TAILINGS INTERFACE
            # Discontinous break would mean slopes of the regressed lines SHOULD NOT INTERSECT 
            calculatedInterfaceLoc = ((middlingsRegression.intercept_)-(frothRegression.intercept_))/((frothRegression.coef_)-(middlingsRegression.coef_))
            interfaceLoc = xMiddlings[0]
            
            ### RULES BASED APPROACH ###
            # Lost interface = combination of "Discontinous Break" + Bulk Density Difference
            # This method is replaced by the neural network in this current revision
            # Threshold on intersection is +-20 tubes away from the identified interface location 
            '''
            if (calculatedInterfaceLoc > interfaceLoc - slopeThreshold and calculatedInterfaceLoc < interfaceLoc + slopeThreshold) or pairedDifferenceStat < pairedDifferenceThreshold:
                interfaceFound = False
                #print(str(dateString) + ' ' + str(False))
            else:
                interfaceFound = True
                #print(str(dateString) + ' ' + str(True))
            '''
            
            ### NEURAL NETWORK APPROACH ###
            # Gather and normalize the feature matrix
            x1 = pairedDifferenceStat
            x2 = interfaceLoc
            x3 = np.rint(calculatedInterfaceLoc.item())
            x4 = frothRegression.coef_
            x5 = middlingsRegression.coef_
            
            featureMatrix = featureNormalize(x1,x2,x3,x4,x5)
            
            # Forward pass normalized feature matrix
            output = neuralNetwork.feedForward(featureMatrix)
            output = np.rint(output.item())
            
            # Aggregate slope line data to be passed back to GUI for rendering
            lineData = {'Froth Slope': frothRegression.coef_.item(), 'Froth Intercept': frothRegression.intercept_, 'Middlings Slope': middlingsRegression.coef_.item(), 'Middlings Intercept': middlingsRegression.intercept_}
            
        else:
            #interfaceFound = False
            output = 0

        # Append results to a list
        results.append({'Date': dateString, 'Output': output, 'Original Data': origData, 'Line Data': lineData, 'Clustered Data': clusterData, 'Clustered Labels': clusterLabels})
    
    return results

### NEURAL NETWORK ALGORITHM ###

class Layer:
    def __init__(self, inputs, neurons, weights=None, bias=None):
        self.weights = weights if weights is not None else np.random.rand(inputs, neurons)
        self.bias = bias if bias is not None else np.random.rand(neurons)
        self.activation = None
        # error is the error of a specific layer
        self.error = None
        # delta is the error applied to a specific layer
        self.delta = None
    
    def activate(self, inputs):
        # Take the dot product of the weights and the input layer plus the bias (Wx + bias)
        inputs = inputs.astype(np.float)
        activationStep = np.dot(inputs, self.weights) + self.bias

        # Apply the activation function to the linear function
        activationStep = sigmoid(activationStep)
        self.activation = activationStep
        return self.activation

# Define the sigmoid function
def sigmoid(x):
  return 1/(1+np.exp(-x))

# Define the derivative function
def sigmoidDerivative(x):
    # does not include sigmoid functions in this derivative because the arguments being passed have already been 'activated'
  return x*(1-x)

class tcNeuralNetwork:
    # Initializing the neutral network
    def __init__(self):
        self.layers = []
        
    def addLayer(self, layer):
        self.layers.append(layer)

    def feedForward(self, x):
        # For each layer activate each layer via weights + activation function
        
        # Initialize the first layer
        layerActivated = []
        
        for layer in self.layers:
            # If it is the first layer - activate the first layer using the inputs
            if layer == self.layers[0]:
                layerActivated = layer.activate(x)
            # Otherwise use the previously activated layer to propagate forward
            else:
                layerActivated = layer.activate(layerActivated)
            
        return layerActivated
    
### Feature Matrix Normalization ###
def featureNormalize(pairedDifference,interfaceLoc,interfaceCalc,frothSlope,middlingsSlope):
    # Standardized by z-score of training data
    x1 = (pairedDifference - 35.17292)/47.93997
    # Ratio of total number of bundle tubes
    x2 = (interfaceLoc - 38.85535)/9.265923
    #x2 = interfaceLoc/88
    # Ratio of total number of bundle tubes - outliers removed
    x3 = (interfaceCalc - 47.67535)/2665.761
    #x3 = max(-122,min(interfaceCalc,188))/88
    # Standardized by z-score of training data - outliers removed
    x4 = (frothSlope - 7.553541)/20.8127
    #x4 = (max(-4.1,min(frothSlope,14.1))-5.041326)/3.67972
    # Standardized by z-score of training data - outliers removed
    x5 = (middlingsSlope - 2.200836)/12.57529
    #x5 = (max(2.4,min(middlingsSlope,-.02))-1.074205)/0.614206
    return(np.reshape(np.array([x1,x2,x3,x4,x5]),(1,5)))

### INITIALIZE OF TRAINED NEURAL NETWORK ###
neuralNetwork = tcNeuralNetwork()
neuralNetwork.addLayer(Layer(5,5))

neuralNetwork.layers[0].weights = np.reshape(np.array([[1.375257474911567357e+00, 1.451120568510164688e+01, 4.275053096926535900e+00, -1.041353279382135888e+01, 1.545821653837993193e+00],[2.353637882592137132e+00, 8.169718813378478162e-01, 5.308047061244600684e-01, 3.892475442782613038e-01, -7.252898185439175194e+00],
[-3.704208613109351234e+00, -6.836034366438082932e-01, 4.932752949530536668e-01, -2.059680539935874410e+00, 1.421854189343936259e+00],[4.976417269327407800e-01, 5.486206071916693183e+00, 8.444012175118970731e+00, -1.394744370294817917e-02, -3.853010931696865704e+00],[1.151442925598014178e+01, -1.002254269630725947e+00, 9.789561413924154465e+00, 6.444063987042179420e+00, -9.854353321039792668e-01]]),(5,5))

#neuralNetwork.layers[0].bias = np.reshape(np.matrix([3.75161896,3.87023158,-7.18419753,-1.5488733,7.5123864]),(-1,5))
neuralNetwork.layers[0].bias = np.reshape(np.array([8.836939095361451280e-01, 3.935642762365443748e+00, -1.905100809985709631e+00, -6.779992992728617551e+00, -7.058399212778666332e+00]),(5,))

neuralNetwork.addLayer(Layer(5,1))
neuralNetwork.layers[1].weights = np.reshape(np.array([-4.555109782426061571e+00,7.613444070946428610e+00,-9.437799007631676673e+00,6.230011229255802085e+00,-2.866939801904996976e+00]),(5,1))

neuralNetwork.layers[1].bias = np.reshape(np.array([-8.530813939258018452e-01]),(1,-1))


### INITIALIZE GUI ###
window = tk.Tk()
myWindow = interfaceWindow(window)
window.title('PSC Interface Detection Tool')
window.geometry("1000x800+10+20")


window.mainloop()

#canvas.get_tk_widget().pack(side=tk.RIGHT, fill='y')


