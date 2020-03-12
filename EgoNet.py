import Circle

class EgoNet:
    def __init__(self,ego,ego_net_features):
        self.__ego = ego #Represents the Ego node for the EgoNet. type - Node object
        self.__social_network = {} # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__social_network[ego] = set() # Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__alter_node_count = 0 # Represents the total number of alter nodes connected to our Ego
        self.__circles = {} #Represents the circles formed in our EgoNet. type - dict where key = circle name		      and value = list of Node objects in the circle
        self.__ego_net_features = ego_net_features # Represents the features for our Ego Net. type - dict where key = feature			           position in feature file (type - int) and value = tuple of feature name and			          feature id. This does not contain Feature objects but just strings. 

    def get_alter_node(self,node_id):
        '''
        Iterates through each key in the social_network dictionary
        if the given node_id equals the key/ego id
        Returns: Node object
        '''
        #Iterates through each key in the social_network dictionary
        for key in self.__social_network.keys():
            #If the node_id equals the id of the node
            if node_id == key.get_id():
                #Returns key/node
                return key
        else:
            return None
    
    def get_ego(self):
        '''
        Returns: The ego which is of type Node
        '''
        #Returns ego
        return self.__ego
    
    def get_circle_names(self):
        '''
        Initializes a list to be used for names
        Iterates through keys in the circle dictionary
            Appends the name/keys to the circle_list
        Returns: List of circle_names
        '''
        self.circle_names = []
        #Iterates through the names in the circle dictionary
        for key in self.__circles.keys():
            #Appends the names to the list
            self.circle_names.append(key)
        return self.circle_names

    def get_circle(self, circle_name):
        '''
        Iterates through the items in the circle_dictionary
        If the key equals the circle_name
            Returns the value/list of node objects
        '''
        #Iterates through items in dictionary
        for k,v in self.__circles.items():
            #If key equals the circle_name
            if k == circle_name:
                return v
    
    def get_alters(self):
        '''
        Returns the alters that are connected to the ego
        '''
        #Returns alters that are connected to the ego using social_network dict
        return self.__social_network[self.__ego]

    def get_alter_node_count(self):
        '''
        Returns the alter_node_count
        '''
        #Returns the alter_node_count
        return self.__alter_node_count

    def get_ego_net_features(self):
        '''
        Returns the ego_net features
        '''
        #Returns the ego_net features dictionary 
        return self.__ego_net_features

    def get_ego_net_feature(self, feature):
        '''
        Returns the feature information in the feature dictionary
        '''
        #Returns the feature_tuple containing the feature name and id
        return self.__ego_net_features[feature]

    def get_feature_pos(self, feature_name, feature_id):
        '''
        Takes in the feature name and feature id as parameters
        Initializes a list
        Appends the feature name and id to that list and convert to tuple
        Iterates through the items in ego_net_feature dictionary
        If the value(tuple) in the feature dictionary equalss the created tuple
            Returns the key which is the feature_position
        Else:
            Return None
        '''
        #Appends the name and id to an empty list
        feature_list = []
        feature_list.append(feature_name)
        feature_list.append(feature_id)
        #Convert to tuple
        feature_tuple = tuple(feature_list)
        #Iterates through the items in the feature dictionary
        for k,v in self.__ego_net_features.items():
                #Checks if the value in the dictionary is equal to the tuple
                if v == feature_tuple:
                    return k
        else:
            return None
        
    def get_alter_connections(self, alter):
        '''
        Returns: the node objects that are connected to the given alter
        '''
        #Returns the value from the given key of the social network dict
        return self.__social_network[alter]
        
    def add_circle(self, circle_name, alters):
        '''
        Creates an object of the Circle Class and uses that as a value
        with the circle name as key and updates the current circle dictionary
        Returns: None
        '''
        self.__circles[circle_name] = Circle.Circle(circle_name,alters)
    
    def add_connection_between_alters(self,alter1,alter2):
        '''
        Takes in alter1 and alter2 as parameters
        Adds alter1 to the social_network dictionary 
        Puts alter2 and ego into a set and has that as the value in the dictionary
        Adds alter2 to the social_network dictionary 
        Puts alter1 and ego into a set and has that as the value in the dictionary
        Returns: None
        '''
        #If alter1 is not in the social network dictionary
        if alter1 not in self.__social_network:
            #Puts alter2 and ego into a set and has that as the value in the dictionary
            alter_list = []
            alter_list.append(alter2)
            alter_list.append(self.__ego)
            alter_set = set(alter_list)
            self.__social_network[alter1]= alter_set
        #Elif alter1 is in the social network dictionary
        elif alter1 in self.__social_network:
            for k,v in self.__social_network.items():
                if alter1 == k:
                    #Puts alter2 and ego into a set and has that as the value in the dictionary
                    alter_list = list(v)
                    alter_list.append(alter2)
                    alter_list.append(self.__ego)
                    alter_set = set(alter_list)     
                    self.__social_network[alter1]= alter_set
        #If alter2 is not in the social network dictionary
        if alter2 not in self.__social_network:
            #Puts alter1 and ego into a set and has that as the value in the dictionary
            alter_list = []
            alter_list.append(alter1)
            alter_list.append(self.__ego)
            alter_set = set(alter_list)
            self.__social_network[alter2]= alter_set
        #Elif alter1 is in the social network dictionary
        elif alter2 in self.__social_network:
            for k,v in self.__social_network.items():
                if alter2 == k:
                    #Puts alter1 and ego into a set and has that as the value in the dictionary
                    alter_list = list(v)
                    alter_list.append(alter1)
                    alter_list.append(self.__ego)
                    alter_set = set(alter_list)  
                    self.__social_network[alter2] = alter_set

    def add_alter_node(self, alter):
        '''
        Iterates through the items in the social network dictionary
            If the key equals ego:
                Appends the current alter to the connected alter list of the ego
                Updates the social network dictionary with the new alter set
        If the alter is not in the social_network dictionary:
            Adds the alter to the social_network as a key and the ego as value
        Update Node count
        Returns: None
        '''
        #Iterates through each item in the social network dictionary
        for k,v in self.__social_network.items():
            #If the key equals the ego
            if k == self.__ego:
                alter_list = list(v)
                alter_list.append(alter)
                alter_set = set(alter_list)
                #Update the dictionary
                self.__social_network[self.__ego]= alter_set
        #If the alter is not in the social_network dictionary
        if alter not in self.__social_network:
            alter_list = []
            alter_list.append(self.__ego)
            alter_set = set(alter_list)
            #Updates dictionary with the alter as key and ego as value
            self.__social_network[alter]= alter_set 
        #Updates node count
        self.__alter_node_count += 1

    def __eq__(self,other):
        '''True if all attributes are equal.'''
        return (self.__ego == other.__ego)\
            and (self.__social_network == other.__social_network) \
            and (self.__alter_node_count == other.__alter_node_count) \
            and (self.__circles == other.__circles) \
            and (self.__ego_net_features == other.__ego_net_features)
            
    def __str__(self):
        '''Returns a string representation for printing.'''
        st = f"Ego: {self.__ego}\n"
        st+= f"Social Network: {self.__social_network}\n"
        st+= f"Circles: {self.__circles}"
        return st

    __repr__ = __str__
    
