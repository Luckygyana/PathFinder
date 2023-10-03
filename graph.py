import openai
import asyncio
import json
from openai_session import OpenAISession

class Graph:
    def __init__(self, topic):
        self.topic = topic
        self.edges = {}
        self.nodes = []
        self.session = OpenAISession()
        openai.api_key = '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'

    def generate_graph(self):
        self.session.add_system_command('Consider what the user is already familiar with and try to productively build upon the knowledge. However, the topics the user knows do not necessarily need to be in the graph. Think step by step. Provide a rigorous roadmap for the user. Maximum Length of the graph should not exceed more than five.')
        msg = {"role" : "user",
               "content" : f"I want to learn about how to start with {self.topic}. Please help me generate a curriculum in the form of a directed graph of topics I must learn to master {self.topic}. In the graph, each topic should lead to one to three other topics. Limit the maximum length of a path on the graph to five. Stay focused on the topic of {self.topic}. Think step by step."}
        graph = self.session.execute_function_call(msg, 'create_tree', 3000, 0.1)
        print(graph)
        self.edges = json.loads(graph)
        print(self.edges)
        msg = {"role" : "user",
               "content" : f"I would like to know more about the following list of education/idea/project topics: {self.edges.keys()}. These topics are with respect to {self.topic}. Please create a dictionary where the keys are the topics in the list and the values are descriptions of each topic with respect to {self.topic}."}
        desc = self.session.execute_function_call(msg, 'print_dict', 6000, 0.3)
        desc = json.loads(desc)
        print(desc)
        print("STARTING NOW")
        
        return self.edges, desc

    def rank_nodes(self):
        msg = {"role" : "user",
               "content" : f"I have a curriculum about {self.topic} in the form of a directed graph. The directed graph is represented by a dictionary in which the keys are topics and the values are lists of topics, and each key-value pair represents edges from the key to each of the elements in its value. An edge from one topic to another denotes that the second topic depends on the first. Please print the curriculum graph in order from most foundational to least foundational, keeping in mind the directed edges. Do this by calling the print_tuples function, which takes a list of tuples as an argument. The topics in each tuple should be roughly the same level of complexity.\n\nHere is the curriculum graph: {self.edges}"}
        ranking = self.session.execute_function_call(msg, 'print_tuples', 3000, 0.2, temp=True)
        print(ranking)
        try:
            return json.loads(ranking)["tuples"]
        except:
            return eval(ranking)