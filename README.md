# Groq + MLflow Tracking Example

[MLflow](https://mlflow.org/) is an open-source platform developed by Databricks to assist in building better Generative AI (GenAI) applications.

MLflow provides a tracing feature that enhances model observability in your GenAI applications by capturing detailed information about the requests you make to the models within your applications. Tracing provides a way to record the inputs, outputs, and metadata associated with each intermediate step of a request, enabling you to easily pinpoint the source of bugs and unexpected behaviors.

The MLflow integration with Groq includes the following features:

- Tracing Dashboards: Monitor your interactions with models via Groq API with dashboards that include inputs, outputs, and metadata of spans
- Automated Tracing: A fully automated integration with Groq, which can be enabled by running mlflow.groq.autolog()
- Easy Manual Trace Instrumentation: Customize trace instrumentation through MLflow's high-level fluent APIs such as decorators, function wrappers and context managers
- OpenTelemetry Compatibility: MLflow Tracing supports exporting traces to an OpenTelemetry Collector, which can then be used to export traces to various backends such as Jaeger, Zipkin, and AWS X-Ray
- Package and Deploy Agents: Package and deploy your agents with Groq LLMs to an inference server with a variety of deployment targets
- Evaluation: Evaluate your agents using Groq LLMs with a wide range of metrics using a convenient API called mlflow.evaluate()


This example demonstrates how to track and monitor your Groq API calls with MLflow's automatic logging and experiment tracking capabilities.

![MLflow Traces](./mlflow-traces.png)

## Overview

This application demonstrates how to integrate Groq API calls with MLflow for comprehensive experiment tracking and model monitoring. Built as a complete, end-to-end template that you can fork, customize, and deploy for production ML workflows.

**Key Features:**
- 🤖 Groq API integration for fast LLM inference
- 📊 MLflow automatic logging and experiment tracking
- 🔧 Local file-based tracking with optional remote server support
- 📈 Automatic instrumentation of Groq API calls
- 🎯 Token usage, latency, and response tracking
- Sub-second response times, efficient concurrent request handling, and production-grade performance powered by Groq

## Architecture

**Tech Stack:**
- **AI Infrastructure:** Groq API for fast LLM inference
- **Experiment Tracking:** MLflow for logging and monitoring
- **Backend:** Python with automatic instrumentation
- **Storage:** Local file system (with optional remote tracking server)

## Quick Start

### Prerequisites
- Python 3.10.16 or higher
- Groq API key ([Create a free GroqCloud account and generate an API key here](https://console.groq.com/keys))
- Optional: MLflow tracking server for remote logging

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd groq-mlflow
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file in the project root
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the example**
   ```bash
   uv run python main.py
   # Or with python directly
   python main.py
   ```

## Features

### Automatic Logging
With `mlflow.groq.autolog()`, every Groq API call is automatically tracked:

- **Request/Response Logging**: All prompts and completions
- **Performance Metrics**: Latency, tokens per second, total tokens
- **Model Parameters**: Temperature, max tokens, model name
- **Cost Tracking**: Token usage for cost analysis
- **Error Tracking**: Automatic error capture and logging

### Experiment Organization
```python
# Set experiment name for organized tracking
mlflow.set_experiment("Groq")

# All runs will be grouped under this experiment
```

### Local vs Remote Tracking
```python
# Local file-based tracking (default)
mlflow.set_tracking_uri(f"file://{pathlib.Path.cwd() / 'mlruns'}")

# Or connect to remote MLflow server
# mlflow.set_tracking_uri("http://localhost:5000")
```

## Usage

### Basic Example
```python
import mlflow
import groq
import os

# Enable automatic logging
mlflow.groq.autolog()

# Create Groq client
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Make API call - automatically logged
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Viewing Results
1. **Local UI**: Run `mlflow ui` in your project directory
2. **Navigate to**: http://localhost:5000
3. **Explore**: Experiments, runs, metrics, and artifacts

## Observability Features

![MLflow Tracking Interface](./mlflow-traces.png)

With this setup, you'll get:

- **Experiment Tracking**: Organize runs by experiment name
- **Parameter Logging**: Model settings, prompt templates, system messages
- **Metrics Tracking**: Response time, token counts, cost estimates
- **Artifact Storage**: Save prompts, responses, and model outputs
- **Run Comparison**: Compare different models and parameters
- **Model Registry**: Version and deploy your best configurations

## Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)
- `MLFLOW_TRACKING_URI`: MLflow tracking server URI (optional)
- `MLFLOW_EXPERIMENT_NAME`: Default experiment name (optional)

### Supported Models
The example uses `llama-3.1-8b-instant` by default, but you can use any Groq-supported model:
- `llama-3.1-8b-instant`
- `llama-3.3-70b-versatile`
- `meta-llama/llama-4-scout-17b-16e-instruct`
- `meta-llama/llama-4-maverick-17b-128e-instruct`

## Customization
This template is designed to be a foundation for you to get started with. Key areas for customization:
- **Model Selection:** Update Groq model configuration in `main.py`
- **Experiment Organization:** Customize experiment names and run tags
- **Tracking Server:** Configure remote MLflow server for team collaboration
- **Custom Metrics:** Add domain-specific metrics and evaluations

## Advanced Usage

### Custom Metrics and Tags
```python
with mlflow.start_run():
    # Your Groq API calls here
    
    # Log custom metrics
    mlflow.log_metric("custom_score", 0.95)
    
    # Add tags for organization
    mlflow.set_tag("model_version", "v1.0")
    mlflow.set_tag("use_case", "customer_support")
```

### Batch Processing with Tracking
```python
def process_batch(messages):
    with mlflow.start_run(run_name="batch_processing"):
        results = []
        for i, message in enumerate(messages):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": message}]
            )
            results.append(response)
            mlflow.log_metric(f"batch_item_{i}_tokens", len(response.choices[0].message.content))
        return results
```

### Remote Tracking Server
```python
# Connect to remote MLflow server
mlflow.set_tracking_uri("http://your-mlflow-server:5000")

# Or use MLflow Cloud/Databricks
mlflow.set_tracking_uri("databricks://profile-name")
```

## Troubleshooting

1. **Missing API Key**: Ensure `GROQ_API_KEY` is set in your `.env` file
2. **MLflow UI Issues**: Run `mlflow ui --host 0.0.0.0` for network access
3. **Permission Errors**: Check write permissions for the `mlruns` directory
4. **Dependencies**: Run `uv sync` to ensure all packages are installed

## Next Steps
### For Developers
- **Create your free GroqCloud account**: Access official API docs, the playground for experimentation, and more resources via [Groq Console](https://console.groq.com).
- **Build and customize**: Fork this repo and start customizing to build out your own application.
- **Get support**: Connect with other developers building on Groq, chat with our team, and submit feature requests on our [Groq Developer Forum](community.groq.com).

### For Founders and Business Leaders
- **See enterprise capabilities**: This template showcases production-ready AI that can handle realtime business workloads with comprehensive tracking and monitoring.
- **Discuss Your needs**: [Contact our team](https://groq.com/enterprise-access/) to explore how Groq can accelerate your AI initiatives.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
Created with Groq API and MLflow integration for production-ready LLM tracking and monitoring.
