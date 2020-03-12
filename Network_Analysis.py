'''
Computer Project 11

Algorithm:
    Call the main function
        Call the get_ego_net_files function to initialize file pointers
        Call get_ego_net_features function to initialize feature dictionary
        Create the ego by creating an instance of the Node class
        Create FacebookNet by creating an instance of the EgoNet class
        Call the add_alters_to_ego_net function to add alters to FaceBookNet
        Call the add_connections_to_ego_net function to add connections
        Call the add_circles_to_ego_net function to add circles to FaceBookNet
        Use while loop to create a looping prompt with choices
            If choice == 1:
                Prompt for circle_name
                Call the calculate_circle_similarity function 
            Elif choice == 2:
                Call the calculate_ego_net_effective_size function
            Elif Choice == 3:
                Prompt for feature name and ID
                Call the calculate_ego_E_I_index function
            Elif Choice == 4:
                calculate_ego_net_efficiency
            Elif Choice == "q"
                Exit the program
            Else:
                Reprompt for choices
'''
from EgoNet import EgoNet
from Node import Node
from Feature import Feature
from Circle import Circle
from operator import itemgetter

def get_ego_net_files():
    '''
    Prompt for user ID to generate EgoNet
    Use While Loop to check for invalid inputs
        Use Try-Except to catch the FileNotFoundError
        Initializes five file pointers
        Returns: the user id and the five file pointers
    '''
    y1 = "_ego_features.txt"
    y2 = "_ego_net_features.txt"
    y3 = "_alters_features.txt"
    y4 = "_ego_net_connections.txt"
    y5 = "_circles.txt"
    x = input("Enter user id to generate EgoNet: ")
    #While loop to check for invalid input
    while True:
        try:
            fp1 = open(x+y1)
            fp2 = open(x+y2)
            fp3 = open(x+y3)
            fp4 = open(x+y4)
            fp5 = open(x+y5)

            return (int(x),fp1,fp2,fp3,fp4,fp5)
        #Catches FileNotFoundError
        except FileNotFoundError:
            print("File not found for ego_id: ",x)
            x = input("Enter user id to generate EgoNet: ")

def get_ego_net_features(fp):
    '''
    Initializes a dictionary to be used for the features
    Uses for loop to iterate through each line in file pointer
        Isolates the feature position, id, and feature_name
        Creates a tuple of the feature name and feature id
        Sets values for the feature dictionary using feature position as 
        the key and the tuple as the value
    Returns: The feature dictionary
    '''
    #Intializes dictionary
    feature_dict = {}
    #Iterates through each line in the file pointer
    for line in fp:
        #Strips each line
        line.strip("\n")
        #Splits the line into a list separated by spaces
        data_list = line.split()
        #Isolates the feature position,id and name
        feature_pos = int(data_list[0])
        feature_id = (data_list[3])
        #Sections off the line that contains the feature name using a list
        feature_data_list = data_list[1].split(";")
        feature_name_list = []
        feature_name_list.append(feature_data_list[0])
        feature_name_list.append(feature_data_list[1])
        #Uses the join method to join together and isolates the feature_name
        if feature_data_list[1] != "id" and feature_data_list[1] != "anonymized":
            feature_name = "_".join(feature_name_list)
        else: 
            feature_name = feature_data_list[0]
        #Creates a tuple of the feature_name and feature_id
        feature_list = []
        feature_list.append(feature_name)
        feature_list.append(feature_id)
        feature_tuple = tuple(feature_list)
        #Creates keys and values for the feature_dictionary
        feature_dict[feature_pos] = feature_tuple 
    return feature_dict
        
def add_ego_net_features_to_ego(ego, ego_feature_file, ego_net_features):
    '''Reads a one-line file of features for the ego node'''
    line_list = ego_feature_file.readline().split()    # read one line
    # i is the index, digit is the value
    for i,digit in enumerate(line_list):   
        # in order to add a feature we must create a Feature instance
        ego.add_feature(i,Feature(ego_net_features[i][1], ego_net_features[i][0],int(digit)))
    return ego

def add_alters_to_ego_net(ego_net,alter_features_file,ego_net_features):
    '''
    Iterates through each line in the features_file using for loop
        Splits each line into a list separated by spaces
        Isolates the alter_id, and the alter values in the line_list
        Creates a Node object using the alter_id and the number of features
        For each value in the alter_values
            Use the alter add_feature method to add features to that alter
        Add the node/alter to the ego_net
    Returns: ego_net
    '''
    #Iterates through each line in the feature_fil;e
    for line in alter_features_file:
        #Splits line into a list
        a_list = line.split()
        #Isolates values
        alter_id = int(a_list[0])
        line_list = a_list[1:]
        #Creates an node object and assigning it to alter
        alter = Node(alter_id, len(line_list))
        #Iterates through each value in the alter_values list
        for i,digit in enumerate(line_list):
            # in order to add a feature we must create a Feature instance
            alter.add_feature(i,Feature((ego_net_features[i][1]), ego_net_features[i][0],int(digit)))
        #Add the alter to the ego_net
        ego_net.add_alter_node(alter)
    return ego_net

def add_connections_to_ego_net(ego_net,connections_file):
    '''
    Iterates through each line in the connections_file using for loop
        Splits the line into a list
        Isolates the alter id's from the connection_list
        Retrieves the alter_node using the alter_ids from the ego_net
        Use the add_connection_between_alters method in the ego_net class
    Returns: ego_net
    '''
    #Iterates through each line in the file
    for line in connections_file:
        #Splits the line into a list
        connection_list = line.split()
        #Isolates id's
        alter1_id = int(connection_list[0])
        alter2_id = int(connection_list[1])
        #Retrieves the node object using ego_net method
        alter1 = ego_net.get_alter_node(alter1_id)
        alter2 = ego_net.get_alter_node(alter2_id)
        #Adds connections between alters using ego_net method
        ego_net.add_connection_between_alters(alter1,alter2)
    return ego_net
    
def add_circles_to_ego_net(ego_net,circles_file):
    '''
    Iterates through each line in circles_file
    Splits the line into a list
    Separates the alter_ids using a list
    Initializes a node_list
        Iterates through each id in the id_list
            Retrieves the node object using the ego_net method and the node_id
            Appends the node to the node_list
            Converts the node_list into a set
        Uses ego_net method to add a circle using the node_set
    Returns ego_net
    '''
    #Iterates through each line in the circles_file
    for line in circles_file:
        #Splits the line into a list
        circle_list = line.split()
        #Isolates the circle_name and the alter ids
        circle_name = circle_list[0]
        circle_alter_ids = circle_list[1:]
        #Initializes node list
        node_list = []
        #Iterates through each id in the alter ids list
        for node_id in circle_alter_ids:
            #Converts to integer
            node_id = int(node_id)
            #Retrieves node object
            node = ego_net.get_alter_node(node_id)
            #Appends node to list and converts to set
            node_list.append(node)
            node_set = set(node_list)
        #Add circle to the ego_net using the add_circle method
        ego_net.add_circle(circle_name,node_set)
    return ego_net

def calculate_circle_similarity(ego_net,circle_name):
    '''
    Retrieves the feature_dictionary using get_ego_net_features
    Retrieves the circle using get_circle method
    Retrieves the alters using circle, get_alters method
    Intializes similarity dictionary
    Iterates through features in feature dictionary
        Initalizes feature_sum to 0
        Iterates through each alter in the circle_alters list
            Retrieves feature_value for each alter
            Sums the feature_sum
        Inserts values for similarity dictionary using the feature
        as key and feature_sum as value
    Returns: The similarity dictionary
    '''
    #Retrieves features from the ego_net
    feature_dict = ego_net.get_ego_net_features()
    #Retrieves the circle using circle_name from ego_net
    circle = ego_net.get_circle(circle_name)
    #Retrieves the alters in that circle using get_alters method
    circle_alters = circle.get_alters()
    similarity_dict = {}
    #Iterates through the features in the feature dictionary
    for key in feature_dict:
        feature_sum = 0
        #Iterates through the alters in the circle_alters list
        for alter in circle_alters:
            #Retrieves the feature_value for each feature
            feature_value = alter.get_feature_value(key)
            #Sums the feature values
            feature_sum += feature_value
        #Adds values to the similarity dictionary for each key
        similarity_dict[key] = feature_sum
    return similarity_dict

def calculate_ego_E_I_index(ego_net,feature_name,feature_id):
    '''
    Retrieves the feature position using specified feature name and id
    Retrieves the set of alters using method get_alters from ego_net
    Initializes E and I value
    Iterates through each node in alters_set
        Retrieves the feature_value for the given feature position
        Sums the feature values to I
        Sums the feature values for 0, to E
    Calculate the EI index using the given formula
    Returns EI_index
    '''
    #Retrieves feature position
    feature_pos = ego_net.get_feature_pos(feature_name,feature_id)
    #Retrieves alters_set
    alters_set = ego_net.get_alters()
    #Initializes E and I values
    I = 0
    E = 0
    #Iterates through nodes in the alters_set
    for node in alters_set:
        #Retrieves the feature_value for the node using feature position
        feature_value = node.get_feature_value(feature_pos)
        #Sums the I value
        I += feature_value
        if feature_value == 0:
            #Sums the E value if the value is 0
            E += 1
    #Calculates EI_index
    EI_index = float((E-I)/(E+I))
    return EI_index
   
def calculate_ego_net_effective_size(ego_net):
    '''
    Retrieves the alter count using get_alter_node_count method
    Retrieves the set of alters in the ego_net using get_alters method
    Iterates through each node in the alters_set
        Retrieves the alter_connections for each node in the set
            Iterates through each node in the alter connections
                Adds 1 for each connection
            Adds the connections for the total connections
    Calculates redundancy
    Calculates effective size using node_count and redundancy
    Returns: Effective size
    '''
    #Retrieves the alter_count and the alters_set
    node_count = ego_net.get_alter_node_count()
    alters_set = ego_net.get_alters()
    total_connections = 0
    #Iterates through each node in the alters_set
    for node in alters_set:
        connections = 0
        #Gets connections for each node
        alter_connections = ego_net.get_alter_connections(node)
        #Iterates through the nodes in the connections
        for node in alter_connections:
            connections += 1
        total_connections += connections
    #Calculates redundancy
    redundancy = total_connections / node_count
    redundancy = redundancy - 1
    #Calculates effective size
    effsize = node_count - redundancy
    return effsize

def calculate_ego_net_efficiency(ego_net):
    '''
    Retrieves the alter count using get_alter_node_count method
    Retrieves the set of alters in the ego_net using get_alters method
    Iterates through each node in the alters_set
        Retrieves the alter_connections for each node in the set
            Iterates through each node in the alter connections
                Adds 1 for each connection
            Adds the connections for the total connections
    Calculates redudancy
    Calculates effective size using node_count and redundancy
    Calculates efficiency using node count and effective size
    Returns: Efficiency
    '''
    node_count = ego_net.get_alter_node_count()
    alters_set = ego_net.get_alters()
    total_connections = 0
    for node in alters_set:
        connections = 0
        alter_connections = ego_net.get_alter_connections(node)
        for node in alter_connections:
            connections += 1
        total_connections += connections
    
    redundancy = total_connections / node_count
    redundancy = redundancy - 1
    effsize = node_count - redundancy
    efficiency = effsize / node_count
    return efficiency
    
def print_choices():
    print("Choices for Ego Net calculation: ")
    print("1 - Top 5 similar features in a circle")
    print("2 - Calculate effective size of Ego Net")
    print("3 - Calculate circle E/I index")
    print("4 - Calculate Ego Net efficiency")
    print("q/Q - Quit ")

def main():
    ego_id,ego_feature_file,ego_net_features_file,alter_features_file,connections_file,circles_file=get_ego_net_files()
    ego_net_features = get_ego_net_features(ego_net_features_file)

    ego = Node(ego_id,len(ego_net_features))

    ego = add_ego_net_features_to_ego(ego,ego_feature_file,ego_net_features)

    FacebookNet = EgoNet(ego,ego_net_features)

    FacebookNet = add_alters_to_ego_net(FacebookNet,alter_features_file,ego_net_features)

    FacebookNet = add_connections_to_ego_net(FacebookNet,connections_file)

    FacebookNet = add_circles_to_ego_net(FacebookNet,circles_file)

    while True:
        print_choices()
        choice = input("Enter choice: ").strip()
        circle_names = FacebookNet.get_circle_names()
        if choice == "1":
            circle_name = input("Enter circle name to calculate similarity: ")
            circle_size = (FacebookNet.get_circle(circle_name).get_circle_size())
            if circle_name in circle_names:
                similarity_dict = calculate_circle_similarity(FacebookNet,circle_name)
            else:
                print("Circle name not in Ego Net's circles. Please try again!")
                continue
            similarity_dict = dict(sorted(similarity_dict.items(),key=itemgetter(1),reverse=True)[:5])
            for feature_pos in similarity_dict:
                feature_name_id = FacebookNet.get_ego_net_feature(feature_pos)
                feature_similarity = (similarity_dict[feature_pos])/(circle_size)
                print(f"Feature: {feature_name_id}")
                print(f"Feature Similarity in {circle_name}: {feature_similarity} \n")
            print()
        elif choice == '2':
            print(f"Effective size of the Ego Net is: {calculate_ego_net_effective_size(FacebookNet)}")
            print()
        elif choice == '3':
            feature_name = input("Enter feature name to calculate E/I index: ")
            feature_id = (input(f"Enter id for {feature_name} to calculate E/I index: "))
            e_i_index = calculate_ego_E_I_index(FacebookNet,feature_name,feature_id)
            if e_i_index < 0:
                print(f"Ego is more homophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()
            else:
                print(f"Ego is more heterophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()

        elif choice == '4':
            ego_net_efficiency = calculate_ego_net_efficiency(FacebookNet)
            print("The efficiency of the Ego Net is: {:.2f}%".format(100*ego_net_efficiency))
            print()

        elif choice in 'qQ':
            break
        else:
            print("Incorrect Choice. Please try again.")
            continue
    ego_feature_file.close()
    ego_net_features_file.close()
    alter_features_file.close()
    connections_file.close()

if __name__ == "__main__":
   main()
