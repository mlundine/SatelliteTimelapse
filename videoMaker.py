#==========================================================#
# videos from satellite images
#==========================================================#

# Kilian Vos WRL 2018
# coast sat code modifed by Mark Lundine 2021

#%% 1. Initial settings

# load modules
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from coastsat import SDS_download, SDS_preprocess
import cv2
from os.path import isfile, join

def makeVideo(frameFolder, vidPath):
    pathIn= frameFolder
    pathOut = vidPath
    fps = 2
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    for i in range(len(files)):
        filename=os.path.join(pathIn,files[i])
##        sat = os.path.splitext(filename)[0][-2:]
##        if sat=='S2':
##            continue
##        print(filename)
        #reading each frame
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    
def main(polygon, dates, sat_list, sitename, vidType):
    # filepath where data will be stored
    filepath_data = os.path.join(os.getcwd(), 'data')

    # put all the inputs into a dictionnary
    inputs = {
        'polygon': polygon,
        'dates': dates,
        'sat_list': sat_list,
        'sitename': sitename,
        'filepath': filepath_data,
            }
        
    #%% 2. Retrieve images
        
    ### retrieve satellite images from GEE
    metadata = SDS_download.retrieve_images(inputs)
    ##
    ### if you have already downloaded the images, just load the metadata file
    metadata = SDS_download.get_metadata(inputs)   
    ##
    ###%% 3. Batch island contour detection
    ##    
    ### settings for the sand contour mapping
    settings = { 
        # general parameters:
        'cloud_thresh': 0.5,        # threshold on maximum cloud cover
        'output_epsg': 3857,        # epsg code of spatial reference system desired for the output
        # quality control:        
        'check_detection_sand_poly': True, # if True, uses sand polygon for detection and shows user for validation 
        'save_figure': True,               # if True, saves a figure showing the mapped shoreline for each image
        # add the inputs defined previously
        'inputs': inputs,
        # [ONLY FOR ADVANCED USERS] shoreline detection parameters:
        'min_beach_area': 50,       # minimum area (in metres^2) for an object to be labelled as a beach
        'buffer_size': 100,         # radius (in metres) of the buffer around sandy pixels considered in the shoreline detection
        'min_length_sl': 500,       # minimum length (in metres) of shoreline perimeter to be valid
        'cloud_mask_issue': False,  # switch this parameter to True if sand pixels are masked (in black) on many images
        'sand_color': 'default',    # 'default', 'dark' (for grey/black sand beaches) or 'bright' (for white sand beaches)
    }
    ##
    ### [OPTIONAL] preprocess images (cloud masking, pansharpening/down-sampling)
    SDS_preprocess.save_jpg(metadata, settings, vidType)
    videoName = os.path.join(filepath_data, sitename, sitename + '.avi')
    imageFolder = os.path.join(filepath_data, sitename, 'jpg_files', 'preprocessed')
    makeVideo(imageFolder, videoName)
    



