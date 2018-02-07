import logging
import networkx as nx
from collections import namedtuple

class SNA_Graph:
    def __init__(self):
        self.g = None
        self.gnode = namedtuple('Node_Desc', 'label name type optional_attrs')
        self.gedge = namedtuple('Edge_Desc', 'src dst rel optional_attrs')

    def create_node(self, label, name, node_type, optional_attrs=None):
        return self.gnode(label, name, node_type, optional_attrs)
    
    def create_edge(self, src, dst, rel, optional_attrs=None):
        return self.gedge(src, dst, rel, optional_attrs)

    def create_graph(self, graph_name, nodels, edgels): 
        self.g = nx.Graph(name=graph_name)
        for (label, name, node_type, optional_attrs) in nodels:
            if optional_attrs is None:
                self.g.add_node(label, name=name, ntype=node_type)
            else:
                self.g.add_node(label, name=name, ntype=node_type, attr_dict=optional_attrs)                
        for (src, dst, rel, optional_attrs) in edgels:
            if self.g.has_edge(src, dst):
                w = self.g.get_edge_data(src, dst)['weight']
                self.g.add_edge(src, dst, weight=w+1)  # NOTE: distance = 1/weight
                #logging.info("More than 1 edge exists between %s and %s, only the first relationship is retained." %(src, dst))
            else:
                if optional_attrs is None:
                    self.g.add_edge(src, dst, rel=rel, weight=1)
                else:
                    self.g.add_edge(src, dst, rel=rel, weight=1, attr_dict=optional_attrs)
        return self.g          

    def get_graph(self): 
        return self.g

