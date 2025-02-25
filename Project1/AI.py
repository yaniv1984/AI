from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from huggingface_hub import login

login("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")

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")




#agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())
#response = agent.run("write a selenium test in headful mode open the browser for https://www.saucedemo.com/ website to preform login ")
#print(response)