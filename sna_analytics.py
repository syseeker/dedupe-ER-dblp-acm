import logging
import operator
import community
import networkx as nx
from networkx.algorithms import approximation as approx
from sna_io import SNA_GraphIO

class SNA_Analytics:
    def __init__(self, g, gout):
        self.g = g
        self.network_prop = {}
        self.top_prop = {}
        self.io = SNA_GraphIO(gout)
    
    def _update_graph_prop(self, attr_name, data):
        """Write graph properties to output file"""
        self.network_prop[attr_name] = data
                
    def _update_top_prop(self, attr_name, data):
        """Write top N results to output file"""
        self.top_prop[attr_name] = data
        
    def _update_node_prop_nodeall(self, attr_name, data):
        """Update node properties with value"""
        nx.set_node_attributes(self.g, data, attr_name)
            
    def _update_node_prop_nodespec(self, attr_name, nodels):
        """Update node properties with binary value, depending if the node ID exists in nodels"""
        for k in nx.nodes(self.g):
            if k in nodels:
                self.g.node[k][attr_name] = 1
            else:
                self.g.node[k][attr_name] = 0
                
    def _update_edge_prop_nodeall(self, attr_name, data):    
        """Update edge properties with value"""
        nx.set_edge_attributes(self.g, data, attr_name)
     
    #----------------------------------------------------------
    def analyse_network_info(self):
        self._update_graph_prop('network_info', nx.info(self.g))
        
    def analyse_avg_path_length(self):
        avg_path_length = nx.average_shortest_path_length(self.g)
        self._update_graph_prop('avg_path_length', avg_path_length)
    
    def analyse_radius(self):  
        radius = nx.radius(self.g)        
        self._update_graph_prop('radius', radius)
    
    def analyse_diameter(self):
        diameter = nx.diameter(self.g)        
        self._update_graph_prop('diameter', diameter)
        
    def analyse_avg_clustering(self):    
        avg_clustering = nx.average_clustering(self.g)        
        self._update_graph_prop('avg_clustering', avg_clustering)
        
    def analyse_transitivity(self):
        transitivity = nx.transitivity(self.g)        
        self._update_graph_prop('transitivity', transitivity)
        
    def analyse_density(self):
        density = nx.density(self.g)        
        self._update_graph_prop('density', density)
        
    def analyse_node_connectivity(self):
        logging.info("load node_connectivity to nodes...")  
        node_connectivity = approx.node_connectivity(self.g)
        self._update_graph_prop('nodeconnectivity', node_connectivity)
    
    def analyse_avg_degree_connectivity(self):
        avg_degree_connectivity = nx.average_degree_connectivity(self.g)
        logging.info("avg_degree_connectivity: ", avg_degree_connectivity)
        self._update_graph_prop('avg_degree_connectivity', avg_degree_connectivity)
        
    def analyse_partition_n_modularity(self):
        logging.info("load partition to nodes...")  
        partition = community.best_partition(self.g)
        modularity = community.modularity(partition, self.g)
        self._update_graph_prop('modularity', modularity)
        self._update_node_prop_nodeall('partition', partition)
        
    def analyse_center(self):    
        center = nx.center(self.g)
        self._update_node_prop_nodespec('center', center)
        
    def analyse_eccentricity(self):    
        logging.info("load eccentricity into nodes...")
        eccentricity = nx.eccentricity(self.g)
        self._update_node_prop_nodeall('eccentricity', eccentricity)
        
    def analyse_pagerank(self):    
        logging.info("load page rank to nodes...")  
        pagerank = nx.pagerank(self.g)    
        self._update_node_prop_nodeall('pagerank', pagerank)
        
    def analyse_degree_centrality(self):    
        logging.info("load degree centrality to nodes...")  
        deg_centrality = nx.degree_centrality(self.g)    
        self._update_node_prop_nodeall('degcentrality', deg_centrality)
    
    def analyse_closeness_centrality(self):    
        logging.info("load closeness centrality to nodes...")  
        closeness_centrality = nx.closeness_centrality(self.g)
        self._update_node_prop_nodeall('closenesscentrality', closeness_centrality)
        
    def analyse_betweenness_centrality(self):    
        logging.info("load betweenness centrality to nodes...")  
        btwness_centrality = nx.betweenness_centrality(self.g)
        self._update_node_prop_nodeall('btwnesscentrality', btwness_centrality)
        
    def analyse_katz_centrality(self):    
        try:
            # Katz centrality
            logging.info("load katz centrality to nodes...")  
            katz_centrality = nx.katz_centrality(self.g, max_iter=100000)
            self._update_node_prop_nodeall('katzcentrality', katz_centrality)
        except (nx.NetworkXError, nx.PowerIterationFailedConvergence):
            print ("Failed: katz_centrality \n")
    
    def analyse_edge_betweenness_centrality(self):    
        logging.info("load betweenness centrality to edges...")  
        edge_betweenness_centrality = nx.edge_betweenness_centrality(self.g)
        self._update_edge_prop_nodeall('edgebetweennesscentrality', edge_betweenness_centrality)
        
    def analyse_triangle(self):
        logging.info("load triangles to nodes...")  
        triangles = nx.triangles(self.g)
        self._update_node_prop_nodeall('triangles', triangles)
        
    def analyse_clustering(self):
        logging.info("load clustering to nodes...")  
        clustering = nx.clustering(self.g)
        self._update_node_prop_nodeall('clustering', clustering)
    
    def analyse_square_clustering(self):
        logging.info("load square_clustering to nodes...")  
        square_clustering = nx.square_clustering(self.g)
        self._update_node_prop_nodeall('squareclustering', square_clustering)
        
    #----------------------------------------------------------
    def get_center(self):
        if not nx.get_node_attributes(self.g, 'center'):
            logging.warn("Run analyse_center() first...")            
        else:
            center = [k for k, v in nx.get_node_attributes(self.g, 'center').iteritems() if v==1]
            res = [(str(center[i]),self.g.node[center[i]]['name']) for i in range(len(center))]
            self._update_top_prop('center', res)            
                
        
    def get_top_eccentricity(self, threshold):
        if not nx.get_node_attributes(self.g, 'eccentricity'):
            logging.warn("Run analyse_eccentricity() first...")            
        else:
            eccentricity = sorted(nx.get_node_attributes(self.g, 'eccentricity').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in eccentricity]
            self._update_top_prop('eccentricity', res)
                    
    def get_top_pagerank(self, threshold):
        if not nx.get_node_attributes(self.g, 'pagerank'):
            logging.warn("Run analyse_pagerank() first...")            
        else:
            pagerank = sorted(nx.get_node_attributes(self.g, 'pagerank').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in pagerank]
            self._update_top_prop('pagerank', res)
                
    def get_top_degree_centrality(self, threshold):
        if not nx.get_node_attributes(self.g, 'degcentrality'):
            logging.warn("Run analyse_degree_centrality() first...")            
        else:
            degcentrality = sorted(nx.get_node_attributes(self.g, 'degcentrality').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in degcentrality]
            self._update_top_prop('degcentrality', res)
            
    def get_top_closeness_centrality(self, threshold):
        if not nx.get_node_attributes(self.g, 'closenesscentrality'):
            logging.warn("Run analyse_closeness_centrality() first...")            
        else:
            closenesscentrality = sorted(nx.get_node_attributes(self.g, 'closenesscentrality').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in closenesscentrality]
            self._update_top_prop('closenesscentrality', res)
                
    def get_top_betweenness_centrality(self, threshold):
        if not nx.get_node_attributes(self.g, 'btwnesscentrality'):
            logging.warn("Run analyse_betweenness_centrality() first...")            
        else:
            btwnesscentrality = sorted(nx.get_node_attributes(self.g, 'btwnesscentrality').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in btwnesscentrality]
            self._update_top_prop('btwnesscentrality', res)
            
    def get_top_katz_centrality(self, threshold):
        if not nx.get_node_attributes(self.g, 'katzcentrality'):
            logging.warn("Run analyse_katz_centrality() first...")            
        else:
            katzcentrality = sorted(nx.get_node_attributes(self.g, 'katzcentrality').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in katzcentrality]
            self._update_top_prop('katzcentrality', res)
                
    def get_top_clustering(self, threshold):
        if not nx.get_node_attributes(self.g, 'clustering'):
            logging.warn("Run analyse_clustering() first...")            
        else:
            clustering = sorted(nx.get_node_attributes(self.g, 'clustering').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in clustering]
            self._update_top_prop('clustering', res)
            
    def get_top_square_clustering(self, threshold):
        if not nx.get_node_attributes(self.g, 'squareclustering'):
            logging.warn("Run analyse_square_clustering() first...")            
        else:
            squareclustering = sorted(nx.get_node_attributes(self.g, 'squareclustering').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in squareclustering]
            self._update_top_prop('squareclustering', res)
            
    def get_top_edges_betweenness_centrality(self, threshold):
        if not nx.get_edge_attributes(self.g, 'edgebetweennesscentrality'):
            logging.warn("Run analyse_edge_betweenness_centrality() first...")            
        else:
            edgesbtwnesscentrality = sorted(nx.get_edge_attributes(self.g, 'edgebetweennesscentrality').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k[0], k[1], v, self.g.node[k[0]]['name'], self.g.node[k[1]]['name']) for k, v in edgesbtwnesscentrality]
            self._update_top_prop('edgesbtwnesscentrality', res)
                    
    def get_top_triangle(self, threshold):  
        if not nx.get_node_attributes(self.g, 'triangles'):
            logging.warn("Run analyse_triangle() first...")            
        else:  
            triangle = sorted(nx.get_node_attributes(self.g, 'triangles').items(), key=operator.itemgetter(1), reverse=True)[:threshold]
            res = [(k, v, self.g.node[k]['name']) for k, v in triangle]
            self._update_top_prop('triangles', res)
                    
    #-------------------------------------------------------------
    def analyse_network(self):
        """Analyse Network"""         
        # TODO: analyse network based on input list. Eg. analyse partition if partition is set in input...        
        if not nx.is_connected(self.g):
            logging.critical("Disconnected network. Analysis halt.")
            return        
        #TODO: read from ..._prop and do not re-analyse if the information already exist
        self.analyse_network_info()
        self.analyse_density()    
        self.analyse_avg_path_length()        
        self.analyse_radius()    
        self.analyse_diameter()    
        self.analyse_transitivity()    
        self.analyse_node_connectivity()
        self.analyse_partition_n_modularity()  
        self.analyse_avg_clustering()    
        self.analyse_avg_degree_connectivity() 
        
        if not nx.get_node_attributes(self.g, 'center'):
            self.analyse_center() 
            
        if not nx.get_node_attributes(self.g, 'eccentricity'):
            self.analyse_eccentricity()
            
        if not nx.get_node_attributes(self.g, 'pagerank'):
            self.analyse_pagerank()
            
        if not nx.get_node_attributes(self.g, 'degcentrality'):
            self.analyse_degree_centrality() 
            
        if not nx.get_node_attributes(self.g, 'closenesscentrality'):
            self.analyse_closeness_centrality() 
            
        if not nx.get_node_attributes(self.g, 'btwnesscentrality'):
            self.analyse_betweenness_centrality() 
            
        #if not nx.get_node_attributes(self.g, 'katzcentrality'):
         #   self.analyse_katz_centrality() 
            
        if not nx.get_edge_attributes(self.g, 'edgebetweennesscentrality'):
            self.analyse_edge_betweenness_centrality() 
                    
        if not nx.get_node_attributes(self.g, 'triangle'):
            self.analyse_triangle() 
        
        if not nx.get_node_attributes(self.g, 'clustering'):
            self.analyse_clustering() 
            
        if not nx.get_node_attributes(self.g, 'squareclustering'):
            self.analyse_square_clustering() 
                                
    def analyse_top_nodes(self, threshold):  
        """Analyse top N network properties"""              
        self.get_center()
        self.get_top_eccentricity(threshold)
        self.get_top_pagerank(threshold)
        self.get_top_degree_centrality(threshold)
        self.get_top_closeness_centrality(threshold)
        self.get_top_betweenness_centrality(threshold)
        self.get_top_katz_centrality(threshold)
        self.get_top_edges_betweenness_centrality(threshold)
        self.get_top_triangle(threshold)
        self.get_top_clustering(threshold)
        self.get_top_square_clustering(threshold)
                
    #-------------------------------------------------------------
    def get_graph(self):
        return self.g
    
    def write_gml(self):
        self.io.write_gml(self.g)
        
    def write_graph_in_csv(self):
        self.io.write_graph_csv(self.network_prop, 
                                self.g.nodes(data=True), 
                                self.g.edges(data=True))
        
    def read_graph_in_csv(self):
        pass
    
    def write_graph_in_json(self):
        self.io.write_graph_json(self.network_prop, 
                                self.g.nodes(data=True), 
                                self.g.edges(data=True))
        
    def read_graph_in_json(self, fout=None):
        return self.io.read_graph_json(fout)
    
    def write_graph_in_web_json(self):
        return self.io.write_graph_web_json(self.network_prop, 
                                            self.g.nodes(data=True), 
                                            self.g.edges(data=True))
        
    def read_graph_in_web_json(self, web_data):
        return self.io.read_graph_web_json(web_data)
    
    def write_top_prop_in_csv(self, fout=None):
        self.io.write_top_csv(self.top_prop, fout)
        
    def write_top_prop_in_json(self, fout=None, json_key=None):
        self.io.write_top_json(self.top_prop, fout, json_key)
        
    def read_top_prop_in_json(self, fout=None):
        return self.io.read_top_json(fout)
    
    def write_top_prop_in_web_json(self, json_key=None):
        return self.io.write_top_web_json(self.top_prop, json_key)
        
    def read_top_prop_in_web_json(self, web_data):
        return self.io.read_top_web_json(web_data)
        
    
    