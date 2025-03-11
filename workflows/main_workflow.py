from langgraph.graph import StateGraph
from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.data_collection.stock_data_agent import fetch_stock_data
from agents.data_collection.fundamentals_agent import fetch_fundamentals
from agents.data_collection.news_sentiment_agent import fetch_news_sentiment
from typing import Dict, Any
from config.logging_config import logger

def main_workflow(ticker: str) -> Dict[str, Any]:
    """Orchestrates the data collection workflow."""
    supervisor = SupervisorAgent(api_type="gemini")
    context = {"ticker": ticker, "step": "start"}
    
    logger.info(f"\nStarting workflow for ticker: {ticker}")
    logger.info("----------------------------------------")
    
    step_count = 0

    try:
        while not supervisor.is_work_complete(context):
            step_count += 1
            next_step = supervisor.decide_next_step(context)
            
            logger.info(f"\nStep {step_count}: {next_step}")
            logger.info("Processing...")

            if next_step == "fetch_stock_data":
                logger.info("Fetching stock data...")
                stock_data = fetch_stock_data(ticker)
                if stock_data is None:
                    raise ValueError("Failed to fetch stock data")
                context["stock_data"] = stock_data
                context["step"] = "stock_data_fetched"
                logger.info("Stock data fetched successfully")

            elif next_step == "fetch_fundamentals":
                logger.info("Fetching fundamentals...")
                fundamentals = fetch_fundamentals(ticker)
                if fundamentals is None:
                    raise ValueError("Failed to fetch fundamentals")
                context["fundamentals"] = fundamentals
                context["step"] = "fundamentals_fetched"
                logger.info("Fundamentals fetched successfully.")

            elif next_step == "fetch_news_sentiment":
                logger.info("Fetching news sentiment...")
                news_sentiment = fetch_news_sentiment(ticker)
                if news_sentiment is None:
                    raise ValueError("Failed to fetch news sentiment")
                context["news_sentiment"] = news_sentiment
                context["step"] = "news_sentiment_fetched"
                logger.info("News sentiment fetched successfully.")
            
            elif next_step == "complete":
                logger.info("Workflow completed.")
                break

            else:
                logger.error(f"Unknown step: {next_step}")
                raise ValueError(f"Unknown step: {next_step}")

            logger.info(f"Updated context: {context}")
            logger.info("----------------------------------------")
            
    except Exception as e:
        print(f"Error in {next_step}: {str(e)}")
        logger.exception(f"Workflow failed at step {next_step}: {str(e)}")
        raise

    logger.info(f"\nWorkflow completed successfully!")
    logger.info(f"Total steps executed: {step_count}")
    return context
