## Lab 06 map generation toolbox
## Sam Iles 03-02-2024

import arcpy
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarageSize]


class GarageSize(object):
    def __init__(self):
        """Define the tool."""
        self.label = "Garage Area"
        self.description = "Classifies the given garages by area. Larger area classes are denoted by darker colors."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Parameters: input project, 
        layer to classify, output location, 
        and output project name."""

        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLoc",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input" #input to the tool: user will be inputing where to send result
        )
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputName",
            datatype="GPString",
            parameterType="Required",
            direction="Input" #input to the tool: user will be inputing where to send result
        )
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        #1: define progressor variables
        readTime = 2.5
        start = 0
        max = 100
        step = 33

        #2: setup progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime)
        #add message to results pane
        arcpy.AddMessage("Validating Project File...")

        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)
        campus = project.listMaps('Map')[0] #gets the first map

        #increment progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        for layer in campus.listLayers(): #Loop thru available layers in the map
            if layer.isFeatureLayer:      #Check if feature layer
                symbology = layer.symbology #just making copy for easier syntax, and in case any mistakes happen
                if hasattr(symbology, 'renderer'): #verify symbology has the attribute "renderer"
                    if layer.name == parameters[1].valueAsText: #user inputed 

                        arcpy.SetProgressorPosition(start + 2*step) #increment progressor
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        symbology.updateRenderer('GraduatedColorsRenderer')
                        symbology.renderer.classificationField = "Shape_Area"
                        symbology.renderer.breakCount = 5
                        symbology.renderer.colorRamp = project.listColorRamps('Greens (5 Classes)')[0]
                        layer.symbology = symbology
                    else:
                        print("NOT Structures")
        
        #increment progressor
        arcpy.SetProgressorPosition(start + 3*step)
        arcpy.SetProgressorLabel("Finishing up...")
        time.sleep(readTime)
        arcpy.AddMessage("Finishing up...")

        project.saveACopy(parameters[2].valueAsText + '\\' + parameters[3].valueAsText + '.aprx')
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
