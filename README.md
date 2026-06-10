---
title: System Design Agents Hub
emoji: 🤖
colorFrom: indigo
colorTo: red
sdk: docker
app_file: app.py
pinned: false
---


# AI Agent Design Patterns with Gemini API

**Author:** Mahmoud Yasser

This repository provides clean, production-ready implementations of core **AI Agent Design Patterns** using the official Google GenAI SDK (`google-genai`) and Gemini models. These architectures help transition from single-prompt interactions to robust, multi-step agentic workflows.

---

## 🚀 Overview of Implemented Patterns

Complex tasks are best handled by dividing them into specialized sub-tasks. This project demonstrates 4 foundational architectural patterns for orchestrating LLMs:

| Pattern | Script Name | Description | Key Advantage |
| :--- | :--- | :--- | :--- |
| **1. Prompt Chaining** | `my_learning_prompt_chaining.py` | Sequences a complex task into linear steps, where the output of one step becomes the input for the next. | Enhances control, improves accuracy, and structures content generation (Outline ➡️ Expand ➡️ Conclude). |
| **2. Routing** | `router_design_patteren.py` | Analyzes incoming user requests and programmatically routes them to the ideal prompt or persona. | Maximizes efficiency and relevance by targeting specific domains (e.g., Math, Translation). |
| **3. Parallelization** | `parallization_methode.py` | Runs multiple independent LLM requests simultaneously using asynchronous execution (`asyncio`). | Minimizes overall latency significantly when tasks do not depend on one another. |
| **4. Orchestrator-Workers** | `orchesterator_agent.py` | A central LLM (Orchestrator) breaks down a task, delegates sub-tasks to parallel workers, and synthesizes their outputs. | Autonomously solves complex, non-linear problems with built-in API quota error handling. |

---

## 🛠️ Prerequisites & Setup

### 1. Installation
All scripts utilize the modern `google-genai` library. Install it using pip:

```bash
pip install google-genai -q
```

### 2. API Key Configuration
The codebase is configured to look for the Gemini API key in your environment variables or Google Colab secrets:

```python
import os
from google.colab import userdata

os.environ["GEMINI_API_KEY"] = userdata.get('gemini')
```
*If running locally, set the environment variable via terminal:* `export GEMINI_API_KEY="your_api_key_here"`

---

## 📂 Deep Dive into Codebases

### 👥 1. Prompt Chaining
* **File:** `my_learning_prompt_chaining.py`
* **How it works:** It processes text generation in a 3-stage pipeline:
  * `outline()`: Generates a 3-bullet-point framework.
  * `expand()`: Expands each point into 2-3 sentences.
  * `conclusion()`: Synthesizes a concluding summary.

### 🔀 2. Routing Design Pattern
* **File:** `router_design_patteren.py`
* **How it works:** Evaluates the user input prefix (e.g., `math:` or `translate:`), conditionally adjusts the system instructions/personas, and executes the highly targeted call via `gemini-2.5-flash`.

### ⚡ 3. Parallelization Method
* **File:** `parallization_methode.py`
* **How it works:** Leverages the asynchronous client (`client.aio`) and `asyncio.gather` to concurrently execute three distinct roles—Researcher, Curator, and Planner—returning a unified overview instantly.

### 🎭 4. Orchestrator-Workers
* **File:** `orchesterator_agent.py`
* **How it works:** 1. **Orchestrator:** Uses `gemini-2.0-flash` to split an objective into exactly 3 raw sub-tasks.
  2. **Workers:** Uses `gemini-2.5-flash` to execute the sub-tasks in parallel.
  3. **Synthesizer:** Aggregates everything into a polished, comprehensive final guide.
* **Resilience:** Implements an exponential backoff loop to catch `429 (Quota Limit)` exceptions, pausing and retrying intelligently instead of crashing.

---

## 🎯 Running the Code

Execute any pattern file directly from your terminal or within a Jupyter/Colab notebook cell:

```bash
python orchesterator_agent.py
```

## 📝 License
This repository is open-source and available under the MIT License. Feel free to use these architectural patterns to power your automated AI workflows!
