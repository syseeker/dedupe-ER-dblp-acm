from sna_util import SNA_Util

class SNA_GraphIO:
    def __init__(self, gout=None):
        self.io = SNA_Util()        
        self.gout = gout
            
    def write_gml(self, g): 
        """Write graph to GML format"""
        self.io.write_gml(g, self.gout)
    
    def write_graph_csv(self, network_prop, node_prop, edge_prop):
        """Write graph to CSV format"""
        if len(network_prop):
            for k, v in network_prop.iteritems():
                self.io.write_csv(self.gout+'_prop', [k, str(v)])
                
        if len(node_prop):
            keys = node_prop[0][1].keys() 
            headers = ['node_id']
            headers.extend(keys)
            self.io.write_csv(self.gout+'_nodes', headers)            
            for n, attr in node_prop:
                data = [n]                
                for k in headers[1:len(headers)-1]:
                    data.append(attr.get(k))
                self.io.write_csv(self.gout+'_nodes', data)
            
        if len(edge_prop):
            keys = edge_prop[0][2].keys()
            headers = ['source', 'target']
            headers.extend(keys)                      
            self.io.write_csv(self.gout+'_edges', headers)
            for s, d, attr in edge_prop:                
                data = [s, d]
                for k in headers[2:len(headers)-1]:
                    data.append(attr.get(k))
                self.io.write_csv(self.gout+'_edges', data)
                
    def read_graph_csv(self):
        pass
    
    def write_graph_json(self, network_prop, node_prop, edge_prop):
        """Write graph to JSON format"""
        data_dict = {}
        data_dict['network'] = [network_prop]
        data_dict['nodes'] = []
        for n, attr in node_prop:
            res = {}
            res = attr
            res['label'] = n                
            data_dict['nodes'].append(res)
        data_dict['edges'] = []
        for s, d, attr in edge_prop:
            res = {}
            res = attr
            res['source'] = s
            res['target'] = d                     
            data_dict['edges'].append(res)
        self.io.write_json(self.gout+'_graph', data_dict)
        
    def read_graph_json(self, fout=None):
        """Read graph in JSON format, return in dict"""
        if fout is None:
            fname = self.gout+'_graph.json'
        else:
            fname = fout
        data = self.io.read_json(fname)
        res = {}
        res['network'] = data.get('network')[0]
        res['nodes'] = data.get('nodes')
        res['edges'] = data.get('edges')
        return res
                     
    def write_graph_web_json(self, network_prop, node_prop, edge_prop):
        """Write graph to JSON format in Web"""        
        data_dict = {}
        data_dict['network'] = [network_prop]
        data_dict['nodes'] = []
        for n, attr in node_prop:
            res = {}
            res = attr
            res['label'] = n                
            data_dict['nodes'].append(res)
        data_dict['edges'] = []
        for s, d, attr in edge_prop:
            res = {}
            res = attr
            res['source'] = s
            res['target'] = d                     
            data_dict['edges'].append(res)
        return self.io.write_web_json(data_dict)
        
    def read_graph_web_json(self, web_data):
        """Read graph from JSON format in Web, and return in dict"""
        res = None
        if len(web_data):
            data = self.io.read_web_json(web_data)  
            res = {}          
            res['network'] = data.get('network')[0]
            res['nodes'] = data.get('nodes')
            res['edges'] = data.get('edges')
        return res
            
    #-------------------------------------------------------------
    def write_top_csv(self, top_prop, fout=None):    
        for k, v in top_prop.iteritems():
            for val in v:
                if fout is None:
                    fname = self.gout+'_top_'+str(k)
                else:
                    fname = fout
                self.io.write_csv(fname, val)
                
    def write_top_json(self, top_prop, fout=None, json_key=None):
        if fout is None:
            fname = self.gout+'_top'
        else:
            fname = fout            
                        
        top_dict = {}
        if json_key is None:            
            top_dict['top'] = []
        else:
            top_dict['top_'+json_key] = []
                        
        for k, v in top_prop.iteritems():
            if json_key is None:            
                top_dict['top'].append({k:v})
            else:
                top_dict['top_'+json_key].append({k:v})
        self.io.write_json(fname, top_dict)
                        
    def read_top_json(self, fout=None):
        """Read top in JSON format, return in dict"""
        if fout is None:
            fname = self.gout+'_top.json'
        else:
            fname = fout                       
        data = self.io.read_json(fname)     
        res = {}
        res['top'] = data['top'][0]  
        return res  
    
    def write_top_web_json(self, top_prop, json_key=None):
        """"""
        top_dict = {}
        if json_key is None:            
            top_dict['top'] = []
        else:
            top_dict['top_'+json_key] = []                        
        for k, v in top_prop.iteritems():
            if json_key is None:            
                top_dict['top'].append({k:v})
            else:
                top_dict['top_'+json_key].append({k:v})                        
        return self.io.write_web_json(top_dict)
    
    def read_top_web_json(self, web_data):
        """"""
        res = None
        if len(web_data):
            data = self.io.read_web_json(web_data)            
            if len(data.get('top')):
                res = {}
                res['top'] = data['top'][0]  
        return res
