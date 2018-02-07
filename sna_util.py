import os
import json
import logging
import networkx as nx
from glob import glob
from networkx.exception import NetworkXError

class SNA_Util:
    def __init__(self):
        pass 
    
    def create_dir(self, fpath):
        try:
            if not os.path.exists(fpath):
                os.makedirs(fpath)
                logging.info("create directory at %s" %fpath)                
            else:
                self.write_csv(fpath+'testdir.log', ['test'])
        except OSError:
            logging.error("Fail to create dir at %s" %fpath)
            
    def get_list_of_files_in_dir(self, fpath):
        """Retrieve all filenames in a given folder"""
        all_files = [y for x in os.walk(fpath) for y in glob(os.path.join(x[0], '*'))]
        flist = []
        for f in all_files:
            flist.append(os.path.basename(f))
        return flist
    
    def read_csv(self, fname):
        try:
            fptr = open(fname)
            data = fptr.readlines()
            fptr.close()
        except (IOError):        
            logging.error("file not found: %s" %fname)
        return data
        
    def write_csv(self, fname, data): 
        """Write data into given file"""       
        try:
            mfile = open(fname+'.csv', 'a')
            mfile.write(",".join(map(str, data)))
            mfile.write('\n')                
            mfile.close()                  
        except (IOError):        
            logging.error("file not found: %s" %fname)
                          
    def read_gml(self, fname)  :          
        """read gml"""
        pass
            
    def write_gml(self, g, fname):
        """write to gml"""
        try:
            #reload(sys)
            #sys.setdefaultencoding('ascii')    
            nx.write_gml(g, fname + '.gml')
        except (NetworkXError):  
            logging.error("Error write_gml")         
            
    def write_graphml(self, g, fname):
        """write to graph_ml"""  
        try:  
            nx.write_graphml(g, fname)
        except NetworkXError:  
            print ("Error write_graphml")
            
    def write_json(self, json_out, data_dict):
        """Write data in dictionary to JSON format"""        
        if len(data_dict):
            fout = open(json_out+'.json', 'w')
            json.dump(data_dict, fout)
            fout.write('\n')
                    
    def read_json(self, json_in):
        with open(json_in) as data_file:
            res = json.load(data_file)                     
        return res  
    
    def write_web_json(self, data_dict):
        """Write data in web JSON format"""
        return json.dumps(data_dict)        
            
    def read_web_json(self, web_data):
        return json.loads(web_data)

    