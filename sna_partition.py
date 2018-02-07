import logging
import community
import networkx as nx

class SNA_Partition:
    """This class provides two different ways for partition-based analysis: 
        (a) create partition from graph; 
        (b) retrieve and analyse partition from a JSON"""
        
    def __init__(self):
        self.partition = {}
    
    def get_partition(self):
        """Retrieve all partitions"""
        return self.partition
    
    def get_number_of_partition(self):
        return len(self.partition)
    
    def _populate_nodes_in_partition(self):
        self.partition_nodes = {}
        for k, v in self.partition.iteritems():    
            self.partition_nodes[k] = []
            for n in v:
                self.partition_nodes[k].append(n['label'])
                
    def get_descending_sorted_partition(self):
        """Sort and return partition"""
        return sorted(self.partition.items(), key=lambda x: len(x[1]), reverse=True)
            
    def get_descending_sorted_partition_by_ranking(self, g, idx=0):
        """Sort and return partition subgraph by ranking"""
        sorted_partition_ls = sorted(self.partition.items(), key=lambda x: len(x[1]), reverse=True)
        return nx.subgraph(g, [a.values()[0] for a in sorted_partition_ls[idx][1]])
    
#---------------------------------------
                
    def create_partition(self, g):
        """Partition graph"""
        logging.info("clustering nodes into partitions...")  
        node_dict = community.best_partition(g)
        self._populate_partition(node_dict)
        return self.partition
    
    def get_partition_subgraph(self, g, pid): 
        """Given a full graph and a partition ID, return a subgraph of all nodes in the partition"""       
        if self.partition:
            return nx.subgraph(g, self.get_nodes_in_partition(pid))
        else:
            logging.error("No partition information found.")
    
    def _populate_partition(self, node_dict):
        """Given dictionary of node with its partition, create inverse dict"""
        self.partition = {}
        for k, v in node_dict.iteritems():
            if v not in self.partition:
                self.partition[v] = [{'label': k}]
            else:
                self.partition[v].append({'label': k})
        self._populate_nodes_in_partition()     
    
    def get_nodes_in_partition(self, pid):
        """Return list of nodes in partition"""
        if self.partition_nodes:
            return self.partition_nodes[pid]
        else:
            return None
        
#---------------------------------------    
    def load_partition_from_node_prop(self, node_prop):
        """Given a node list with node's partition, return a dictionary of partition. 
        For each partition, a list of node properties is returned. 
        Each list element consist of a dictionary of node id and name. 
        {partition_id:[{id, name}]}"""
        self.partition = {}
        for n in node_prop:
            label = n.get('label')
            name = n.get('name')
            node_type = n.get('ntype')
            community = n.get('partition')            
            if community is None:
                if 'other' not in self.partition:
                    self.partition['other'] = [{'label':label, 'ntype':node_type, 'name':name}]
                else:
                    self.partition['other'].append({'label':label, 'ntype':node_type, 'name':name})
            else:
                if community not in self.partition:
                    self.partition[community] = [{'label':label, 'ntype':node_type, 'name':name}]
                else:
                    self.partition[community].append({'label':label, 'ntype':node_type, 'name':name})
        self._populate_nodes_in_partition()
        return self.partition
    
        