# (Keep the same imports and respond() function from Phase 2)

# ... [Insert imports and respond() function here] ...

demo = gr.ChatInterface(
    fn=respond,
    title="Concurrent AI Assistant"
)

# TODO 1: Enable the queue system so the app doesn't crash under heavy traffic.
# Set default_concurrency_limit to handle a specific number of requests at a time.
demo.queue(...)


if __name__ == "__main__":
    demo.launch()
