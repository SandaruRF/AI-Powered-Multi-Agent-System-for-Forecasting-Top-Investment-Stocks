from langgraph import Graph, Node, Edge
from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.data_collection.stock_data_agent import fetch_stock_data
from agents.data_collection.fundamentals_agent import fetch_fundamentals
from agents.data_collection.news_sentiment_agent import fetch_news_sentiment

def main_workflow(ticker: str):
    supervisor = SupervisorAgent()
    context = {"ticker": ticker, "step": "start"}

    while not supervisor.is_work_complete(str(context)):
        next_step = supervisor.decide_next_step(str(context))

        if next_step == "fetch_stock_data":
            context["stock_data"] = fetch_stock_data(ticker)
        elif next_step == "fetch_fundamentals":
            context["fundamentals"] = fetch_fundamentals(ticker)
        elif next_step == "fetch_news_sentiment":
            context["news_sentiment"] = fetch_news_sentiment(ticker)
        # .... other steps ...

    print("Workflow completed successfully.")
