## Introduction

This tutorial demonstrates how to implement a **multi-agent system with shared memory** using AWS AgentCore Memory and the Strands framework. While our previous examples focused on single-agent memory, this tutorial explores how multiple specialized agents can work together while accessing a common memory store.

For Single Agent memory please check 
- [Strands Agents with AgentCore Memory (Short-Term Memory)](../../01-short-term-memory/01-single-agent/with-strands-agent/)
- [Langgraph Agents with AgentCore Memory (Short-Term Memory)](../../01-short-term-memory/01-single-agent/with-langgraph-agent/)

## Tutorial Details

| Information         | Details                                                                          |
|:--------------------|:---------------------------------------------------------------------------------|
| Tutorial type       | Short Term Conversational                                                        |
| Agent usecase       | Travel Planning Assistant                                                        |
| Agentic Framework   | Strands Agents                                                                   |
| LLM model           | Anthropic Claude Sonnet 3                                                        |
| Tutorial components | AgentCore Short-term Memory, Strands Agents, Memory retrieval via Tool           |
| Example complexity  | Beginner                                                                         |




### Scenario context

In this example, we'll create a **Travel Planning System** with:
1. A Flight Booking Assistant specialized in air travel
2. A Hotel Booking Assistant focused on accommodations
3. A Travel Coordinator that delegates to these specialized agents

This approach demonstrates how complex domains can be broken down into specialized agents that share memory the same memory store.

## Tutorial Architecture

In this Tutorial, we will describe how to set up a shared memory resource that multiple agents can access. In our example we will perform following tasks - 

- Create specialized agents as tools with their own memory access
- Implement a coordinator agent that delegates to specialized agents
- Maintain conversation context across multiple agent interactions

<div style="text-align:left">
    <img src="architecture.png" width="65%" />
</div>



