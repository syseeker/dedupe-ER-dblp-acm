import operator
import networkx as nx
from sna_error import SNA_Error
from collections import Counter

class SNA_ConnectedComponent:
    def __init__(self, g):
        self.g = g
                                
    def get_number_of_connected_component(self):
        """Get number of connected component of the given graph"""
        try:
            if not nx.is_directed(self.g):    
                num_connected_component = nx.number_connected_components(self.g)                
                return num_connected_component
            else:
                raise SNA_Error('SNA_DIRECTED_GRAPH_CANT_FIND_CONNECTED_COMPONENT')
        except (SNA_Error):
            return 'SNA_DIRECTED_GRAPH_CANT_FIND_CONNECTED_COMPONENT' 
    
    def get_descending_sorted_connected_component(self):
        """Sort and return connected component"""
        return sorted(nx.connected_components(self.g), key=len, reverse=True)
            
    def get_descending_sorted_connected_component_by_ranking(self, idx=0):
        """Sort and return connected component by ranking"""
        sorted_conncomp_ls = sorted(nx.connected_components(self.g), key=len, reverse=True)
        return nx.subgraph(self.g, sorted_conncomp_ls[idx])
    
    def get_connected_component_by_size(self):
        """Get number of component with x size"""
        conn_size = [len(c) for c in nx.connected_components(self.g)]    
        sorted_count_conncomp = sorted(Counter(conn_size).items(), key=operator.itemgetter(0))
        return sorted_count_conncomp
            
        