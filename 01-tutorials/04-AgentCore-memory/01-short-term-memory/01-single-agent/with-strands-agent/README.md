# Strands Agents with AgentCore Memory (Short-Term Memory)


## Introduction

This tutorial demonstrates how to build a **personal agent** using Strands agents with AgentCore **short-term memory** (Raw events) within a single conversation without without explicit context management. The agent remembers recent conversations in the session using `get_last_k_turns` and can continue conversations seamlessly when user returns. 

For tutorial on how to implement a **multi-agent system with shared memory** using AWS AgentCore Memory and the Strands framework check [here](../../02-multi-agent/with-strands-agent/) and for how to integrate Amazon Bedrock AgentCore Memory capabilities with a conversational AI agent using LangGraph framework check [here](../with-langgraph-agent).


### Tutorial Details

| Information         | Details                                                                          |
|:--------------------|:---------------------------------------------------------------------------------|
| Tutorial type       | Short Term Conversational                                                        |
| Agent type          | Personal Agent                                                                   |
| Agentic Framework   | Strands Agents                                                                   |
| LLM model           | Anthropic Claude Sonnet 3.7                                                      |
| Tutorial components | AgentCore Short-term Memory, AgentInitializedEvent and MessageAddedEvent hooks   |
| Example complexity  | Beginner                                                                         |

You'll learn to:
- Use short-term memory for conversation continuity
- Retrieve last K conversation turns
- Web search tool for real-time information
- Initialize agents with conversation history

## Architecture
<div style="text-align:left">
    <img src="architecture.png" width="65%" />
</div>

## Prerequisites

- Python 3.10+
- AWS credentials with AgentCore Memory permissions
- AgentCore Memory role ARN
- Access to Amazon Bedrock models

## Tutorial Key Features

- Using Strands Agents
- Using short-term memory for conversation continuity within a single conversation session
- Using `get_last_k_turns` for conversation history
- Implement memory hooks for automatic context storage and retrieval