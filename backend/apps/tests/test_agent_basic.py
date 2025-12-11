from apps.agents.agent import create_stock_agent_executor


def main():
    agent_executor = create_stock_agent_executor()

    result = agent_executor.invoke({
        "input": "Fetch recent daily prices for AAPL."
    })

    print("\nFINAL RESULT:")
    print(result)


if __name__ == "__main__":
    main()
