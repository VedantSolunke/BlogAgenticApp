from src.states.blogstate import Blog, BlogState
from langchain_core.messages import SystemMessage, HumanMessage

class BlogNode:
    """
    A class to represent the blog node

    """

    def __init__(self, llm):
        self.llm = llm
            
    
    def title_creation(self, state:BlogState):
        """
        Generate a title for the blog post based on the topic and current language
        """
        if "topic" in state and state["topic"]:
            topic = state["topic"]
            prompt = """
                You are a professional blog writer. Generate a catchy and engaging title for a blog post based on the following topic: {topic}.
                use markdown formatting.
            """
            
            system_message = prompt.format(topic=topic)
            response = self.llm.invoke(system_message)
            
            return {"blog" : {"title" : response.content}}
        
    def content_creation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            topic = state["topic"]
            system_prompt = """
                You are a professional blog writer. Generate a detailed and informative blog post based on the following topic: {topic}.
                use markdown formatting.
            """
            
            system_message = system_prompt.format(topic=topic)
            response = self.llm.invoke(system_message)
            
            return {"blog" : { "title": state["blog"]["title"], "content" : response.content}}
        
    def translation(self, state:BlogState):
        """
        Translate the blog post into the specified language
        """
        translate_prompt = """
        Translate the following content into {current_language} while maintaining the original meaning and context.
        -adapt cultural references and idiomatic expressions to be appropriate for the target language. {current_language} is the language specified in the state.
        
        ORIGINAL CONTENT:
        {blog_content}
        """
        
        blog_content = state["blog"]["content"]
        messages = [
            SystemMessage(
                "You are a professional blog translator. Translate the supplied blog "
                "content into the requested language. Preserve Markdown formatting "
                "and return only the translated blog content."
            ),
            HumanMessage(translate_prompt.format(current_language=state["current_language"], blog_content=blog_content))
        ]
        
        translation_response = self.llm.invoke(messages)
        return {
            "blog": Blog(
                title=state["blog"]["title"],
                content=translation_response.content,
            )
        }
    
    def route(self, state:BlogState):
        """
        Route the flow based on the specified language in the state
        """
        return {"current_language" : state['current_language']}
    
    def route_decision(self, state:BlogState):
        """
        Determine the next node based on the specified language in the state
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "spanish":
            return "spanish"
        else:
            return state["current_language"]