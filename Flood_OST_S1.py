import os
import datetime
import glob
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import numpy as np
from whitebox.WBT.whitebox_tools import WhiteboxTools
wbt = WhiteboxTools()




class Sentinel1Flood:
    def __init__(self,in_path,out_path):
        self.in_path  = in_path
        self.out_path = out_path
        self.nrows = None
        self.ncols = None
        self.geotransform = None
        self.proj = None
        self.change_array = None
        self.maj_input_name = None
        self.ras2poly_input_name = None
        
        
    def change(self,out_change_name = ""):
        pre_image  = os.path.normpath(glob.glob(self.in_path+'*pr*.tiff',recursive = True)[0])
        post_image = os.path.normpath(glob.glob(self.in_path+'*po*.tiff',recursive = True)[0])
        
        raster_pre=gdal.Open(pre_image)
        raster_post=gdal.Open(post_image)

        pre_band = raster_pre.GetRasterBand(1)
        post_band = raster_post.GetRasterBand(1)
        
        gtpost =raster_post.GetGeoTransform()
        gtpre =raster_pre.GetGeoTransform()

        #Pre and post top(x,y) bottom(x,y) co-ordinates
        post_bound  = [gtpost[0], gtpost[3], gtpost[0] + (gtpost[1] * raster_post.RasterXSize), gtpost[3] + (gtpost[5] * raster_post.RasterYSize)]
        pre_bound   = [gtpre[0] , gtpre[3] , gtpre[0]  + (gtpre[1]  * raster_pre.RasterXSize) , gtpre[3]  + (gtpre[5]  * raster_pre.RasterYSize)]
        
        #Finding the intersection boundry
        intersection = [max(post_bound[0], pre_bound[0]), min(post_bound[1], pre_bound[1]), min(post_bound[2], pre_bound[2]), max(post_bound[3], pre_bound[3])]

        post_bound_pix = [abs(round((gtpost[0]-intersection[0])/gtpost[1])),abs(round((gtpost[3]-intersection[1])/gtpost[5])),
                  abs(round((gtpost[0]-intersection[2])/gtpost[1])),abs(round((gtpost[3]-intersection[3])/gtpost[5]))]

        pre_bound_pix = [abs(round((gtpre[0]-intersection[0])/gtpre[1])),abs(round((gtpre[3]-intersection[1])/gtpre[5])),
                 abs(round((gtpre[0]-intersection[2])/gtpre[1])),abs(round((gtpre[3]-intersection[3])/gtpre[5]))]
        
        post_intersect = post_band.ReadAsArray(post_bound_pix[0],post_bound_pix[1],post_bound_pix[2] - post_bound_pix[0],
                                               post_bound_pix[3] - post_bound_pix[1],post_bound_pix[2] - post_bound_pix[0],
                                               post_bound_pix[3] - post_bound_pix[1],buf_type=gdal.GDT_Float32)

        pre_intersect = pre_band.ReadAsArray(pre_bound_pix[0],pre_bound_pix[1],pre_bound_pix[2] - pre_bound_pix[0],
                                             pre_bound_pix[3] - pre_bound_pix[1],pre_bound_pix[2] - pre_bound_pix[0], 
                                             pre_bound_pix[3] - pre_bound_pix[1],buf_type=gdal.GDT_Float32)

        self.nrows = pre_bound_pix[3] - pre_bound_pix[1]
        self.ncols = pre_bound_pix[2] - pre_bound_pix[0]
        
        #Getting the  change image using the numpy array operations
        #import numpy as np
        self.change_array = np.subtract(post_intersect,pre_intersect)
        
        
        self.geotransform=([intersection[0],gtpost[1],gtpost[2],intersection[1],gtpost[2], gtpost[5]]) 
        self.proj = raster_pre.GetProjection()
        
        output_raster = gdal.GetDriverByName('GTiff').Create(self.out_path+out_change_name+".tiff",self.ncols, self.nrows, 1 ,gdal.GDT_Float32)  # Open the file
        output_raster.SetGeoTransform(self.geotransform)  
        #srs = osr.SpatialReference()                
        #srs.ImportFromEPSG(4326)                                                                                                         
        output_raster.SetProjection(self.proj)  
        output_raster.GetRasterBand(1).WriteArray(self.change_array) 
        output_raster.FlushCache()
        
        
        

        print("Change was successfully executed")
        
        #return (nrows,ncols,geotransform,proj,change)
        
    def thresholding(self,threshold_value,out_thresh_name=""):       
        
        #Threshold calculation
        threshold = np.where(self.change_array < threshold_value , 1,0)
        
        output_raster2 = gdal.GetDriverByName('GTiff').Create(self.out_path+out_thresh_name+"_"+str(threshold_value)+".tiff",self.ncols, self.nrows, 1 ,gdal.GDT_Byte)  # Open the file
        output_raster2.SetGeoTransform(self.geotransform)  
        #srs = osr.SpatialReference()                
        #srs.ImportFromEPSG(4326)                                                                                                         
        output_raster2.SetProjection(self.proj)  
        output_raster2.GetRasterBand(1).WriteArray(threshold) 
        output_raster2.FlushCache()
        
        self.maj_input_name = out_thresh_name+"_"+str(threshold_value)+".tiff"
        print("successfully executed")
        
    def maj_filtering(self,filter_size,out_maj_name):   
        #Printing the running status
        def my_callback(value):             
            if not "%" in value:
                print(value)

        #Majority filter        
        wbt.majority_filter(self.out_path+self.maj_input_name,
                    self.out_path+self.maj_input_name[:-5]+out_maj_name+"_"+str(filter_size)+".tiff", 
                    filterx=filter_size, filtery=filter_size, callback=my_callback) 
        
        self.ras2poly_input_name = self.maj_input_name[:-5]+out_maj_name+"_"+str(filter_size)+".tiff"
        
        
    def ras2poly(self,out_poly_name):
        
        #Printing the running status
        def my_callback(value):             
            if not "%" in value:
                print(value)
        
        wbt.raster_to_vector_polygons(self.out_path+self.ras2poly_input_name, 
                                   self.out_path+self.ras2poly_input_name[:-5]+"_"+out_poly_name+".shp", 
                                    callback=my_callback)       
            