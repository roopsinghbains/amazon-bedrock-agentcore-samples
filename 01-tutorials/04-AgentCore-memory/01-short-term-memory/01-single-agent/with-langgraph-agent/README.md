# LangGraph Agents with AgentCore Memory (Short-Term Memory)

## Introduction
This tutorial demonstrates how to integrate Amazon Bedrock AgentCore Memory capabilities with a conversational AI agent using LangGraph framework. We'll focus on **short-term memory** retention within a single conversation session - allowing an agent to recall information from earlier in the conversation without explicit context management.For tutorial on how to integrate Amazon Bedrock AgentCore Memory capabilities with a conversational AI agent using Strands framework check [here](../with-strands-agent/)


## Tutorial Details

| Information         | Details                                                                          |
|:--------------------|:---------------------------------------------------------------------------------|
| Tutorial type       | Short Term Conversational                                                        |
| Agent usecase       | Personal Fitness                                                                 |
| Agentic Framework   | Langgraph                                                                        |
| LLM model           | Anthropic Claude Sonnet 3                                                        |
| Tutorial components | AgentCore Short-term Memory, Langgraph, Memory retrieval via Tool                |
| Example complexity  | Beginner                                                                         |


## Tutorial Architecture

In this tutorial we will integrate LangGrap with AgentCore Memory. 

We will create a memory store using the AgentCore Memory SDK and incorporate it into LangGraph structured workflow as memory tool.

<div style="text-align:left">
    <img src="architecture.png" width="65%" />
</div>

## Prerequisites

- Python 3.10+
- AWS account with appropriate permissions
- AWS IAM role with appropriate permissions for AgentCore Memory
- Access to Amazon Bedrock models


### Scenario Context

In this example, we'll create a "**Personal Fitness Coach**" that can remember workout details, fitness goals, physical limitations, and exercise preferences as they are mentioned throughout the conversation. This assistant will demonstrate how effective short-term memory management enables a more natural and personalized fitness coaching experience without requiring users to repeatedly state their information.

## Key Features

1. Create a AgentCore Memory resource for an AI agent
2. Build a LangGraph workflow with memory integration
3. Implement memory tools for conversation history retrieval
4. Create an agent that intelligently uses memory when needed
5. Test memory persistence across agent instances

