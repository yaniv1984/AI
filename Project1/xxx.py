import os
import asyncio
import sched
import time

import browser_use.browser.context
from browser_use import Agent
from browser_use.agent.views import ActionResult
from browser_use.controller.service import Controller
from gradio.themes.builder_app import history
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import BrowserContext
from pydantic import SecretStr, BaseModel

# Disable anonymized telemetry (optional)
os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Set the API Key using environment variables
os.environ["GEMINI_API_KEY"] = "AIzaSyA2SOqDkETpurEvy2Hn9L5JZzfHRGVaPRc"  # Store safely, do not hardcode in code

# get the agent to provide data for assertion
class CheckResult(BaseModel):
    login_status : str
    user_name : str
    password : str


controller = Controller(output_model=CheckResult)

#playwright rapper browserContaxt
@controller.action('get url of the page')
async def get_attr_url(browser : browser_use.browser.context.BrowserContext):
    print("ffffffffffffffffffff")
    page = await browser.get_current_page()
    current_url = page.url
    #attr = await page.get_by_text("Accounts Overview").get_attribute('id')
    print(current_url)

    #return ActionResult(extracted_content=f'the url is{current_url} nad attr is {attr}')

async def playwright_with_browser_use():
    task = ('Open website https://parabank.parasoft.com/parabank/index.htm and preform login'
    'get url of the page')

    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")  # Fetch from environment
    )

    # Initialize and Run the Agent with use_vision
    agent = Agent(task, llm , controller=controller , use_vision=True)
    history = await agent.run()  # Ensure the agent is executed properly
    history.save_to_file('agentresults.json')
    test_results = history.final_result()
    print(test_results)
    validate_result = CheckResult.model_validate_json(test_results)
    time.sleep(3)
    print(validate_result.login_status)
    #assert validate_result.login_status == "Successful"
    assert validate_result.user_name == "john"
    assert validate_result.password == "demo"

# Run the async function
if __name__ == "__main__":
    asyncio.run(playwright_with_browser_use())
