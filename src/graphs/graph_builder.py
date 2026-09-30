from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on a given topic
        """
        self.blog_node_obj = BlogNode(self.llm)
        
        ## Nodes
        
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_creation", self.blog_node_obj.content_creation)
        
        ## Edges
        
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_creation")
        self.graph.add_edge("content_creation", END)
        
        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph to generate blogs based on a given language
        """
        self.blog_node_obj = BlogNode(self.llm)
                
        ## Nodes
        
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_creation", self.blog_node_obj.content_creation)
        self.graph.add_node("hindi_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}))
        self.graph.add_node("spanish_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "spanish"}))
        self.graph.add_node("route", self.blog_node_obj.route)

        ## Edges and conditional edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_creation")
        self.graph.add_edge("content_creation", "route")
        
        ### Conditional edges for routing based on language
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                'hindi': "hindi_translation",
                'spanish': "spanish_translation",
            }
        )
        self.graph.add_edge("hindi_translation", END)
        self.graph.add_edge("spanish_translation", END)
               
        return self.graph
    
    def setup_graph(self, usecase):
        """
        Setup the graph with the necessary nodes and edges
        """
        if usecase == "topic":
            return self.build_topic_graph().compile()
        
        if usecase == "language":
            return self.build_language_graph().compile()
        
        return self.graph.compile()
    
    
## Below code is for the langsmith langgraph studio
llm = GroqLLM().get_llm()

## get the graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()