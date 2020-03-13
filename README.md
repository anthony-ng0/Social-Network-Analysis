### Background

Social network analysis is the process of investigating social structures through the use of networks
and graph theory. One of the common ways to analyze social networks is through the use of Ego Nets. 

Ego Nets are networks that consist of a central node("Ego") and it's connecting nodes("Alters"). A property of these nodes are known as features. Examples of features could consist of gender, location, or educational institution. Nodes with common features form groups known as "Circles". 

With this network of nodes, known as a "Graph", we can use a perform a variety of methods that can tell us a lot about a social network. Within this program, we can find and calculate a measure of the similarity within circles as well as use Krackhardt and Stern’s EI index for the Ego to find a ratio that represents the overall homophily and heterophily. You can also perform structural analysis by finding the effective size and redundancy of the Ego Net. The ratio of effective size and redundancy is known as the Efficiency.

### Usage 
- Network Analysis.py (Driver Program): Given data of input for a particular Ego Net, we have the option to perform the various methods of   analysis described above.
- Egonet.py : Contains the class definition of the "Ego Net".
- Node.py: Contains the class definition of a "Node".
- Feature.py: Contains the class definition of a "Feature".
- Circle.py: Contains the class definition of a "Circle".

Included are various files that represent two data networks identified by "3980" and "1234". The data includes the features and connections of the alters, circles and ego.

