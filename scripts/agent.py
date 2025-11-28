import asyncio
from talk_with_wiski.agents.talk_with_wiski_agent import WISKIAgent
from dotenv import load_dotenv
from pathlib import Path
from pydantic_ai import AgentRunResult
from talk_with_wiski.models.base import AgentResponse


async def main():
    file = Path(__file__)
    load_dotenv(file.parent.parent / "env" / ".env")
    agent = WISKIAgent()
    prompt = "Analyseer voor het meetpunt Dintelsas de beschikbare data"
    result: AgentRunResult = await agent.ask(prompt)
    response: AgentResponse = result.output
    with open(file.parent / "example.md", "w", encoding="utf-8") as f:
        f.write(response.markdown_text)


if __name__ == "__main__":
    asyncio.run(main())
