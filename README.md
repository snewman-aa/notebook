# Notebook app for NLP Systems

## Installation

Make sure you have at least python 3.11 installed. 
Then, in the project directory run the following command to install the package:

```bash
pip install -e .
```

This will include the following dependencies:
```
fastapi[standard]>=0.115.8,
flask>=3.1.0,
streamlit>=1.42.0,
uvicorn>=0.34.0
```

## Usage

### Flask
To run the flask app, use the following command:
```bash
flask-app
```

### FastAPI
To run the FastAPI app, use the following command:
```bash
fast-app
```

### Streamlit
To run the Streamlit app, use the following command:
```bash
stream-app
```