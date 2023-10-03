import openai
import json

class OpenAISession:
    def __init__(self):
        self.messages = []
        self.functions = [
                        {
                        "name": "create_tree",
                        "description": "Writes a tree given a dictionary representing directed edges, where each key is the starting node and each value is a list of destination nodes.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "edges": {
                                    "type": "object",
                                    "description": "Dictionary representing directed edges of a graph, where each key-value pair corresponds to a starting node and a list of destination nodes."
                                    }
                                },
                            "required": [
                                "edges"
                            ]
                        }
                    },
                        {
                        "name": "print_tuples",
                        "description": "Prints a list of tuples",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "tuples_list": {
                                   "type": "object",
                                   "description": "List of tuples to be printed."
                                },
                            },
                            "required": [
                                "tuples_list"
                            ]

                        }
                    },

                        {
                        "name": "print_dict",
                        "description": "Prints a dictionary.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "topics": {
                                    "type": "object",
                                    "description": "Dictionary where each key is a topic from a list of topics and each value is a brief string description of the topic."
                                    }
                                },
                            "required": [
                                "topics"
                            ]
                        }
                    }

                ]
    
    def add_system_command(self, command):
        msg = {"role": "system",
               "content": f"{command}"}
        self.messages.append(msg)

    def execute_chat_completion(self, msg, max_tokens, temperature):
        self.messages.append(msg)
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        self.messages.append(response['choices'][0]['message'])
        return response['choices'][0]['message']['content']

    def execute_function_call(self, msg, function_to_call, max_tokens, temperature, **kwargs):
        if 'temp' in kwargs and kwargs.get('temp') is True:
            temp_msg = []
            temp_msg.append(msg)
            response = openai.ChatCompletion.create(
                    model='gpt-4',
                    messages=temp_msg,
                    functions=self.functions,
                    function_call={"name" : function_to_call},
                    max_tokens=max_tokens,
                    temperature=temperature
                    )
            print(response)
            return response['choices'][0]['message']['function_call']['arguments']

        self.messages.append(msg)
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages,
            functions=self.functions,
            function_call={"name" : function_to_call},
            max_tokens=max_tokens,
            temperature=temperature
        )
        self.messages.append(response['choices'][0]['message'])
        return response['choices'][0]['message']['function_call']['arguments']
    
        
