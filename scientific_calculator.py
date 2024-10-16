# app.py

import streamlit as st
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

# Set Plotly renderer for Streamlit
pio.renderers.default = "iframe_connected"

# Title of the App
st.title("📟 Scientific Calculator with Plotting")

# Initialize Session State for expression and history
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Define allowed names for safe evaluation
allowed_names = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'sqrt': np.sqrt,
    'log': np.log,
    'exp': np.exp,
    'abs': np.abs,
    'pi': np.pi,
    'e': np.e,
    'factorial': lambda x: np.math.factorial(int(x)),
    'asin': np.arcsin,
    'acos': np.arccos,
    'atan': np.arctan,
    'floor': np.floor,
    'ceil': np.ceil,
    'round': np.round,
    'x': None  # Placeholder for plotting
}

def sanitize_expression(expression):
    """
    Replace Unicode minus signs with standard hyphen-minus.
    """
    return expression.replace('−', '-')

def eval_expression(expression, x_value=None):
    """
    Safely evaluate the mathematical expression using allowed names.
    If x_value is provided, include it in the evaluation context.
    """
    # Sanitize the expression
    expression = sanitize_expression(expression)
    
    # Update 'x' in allowed_names if plotting
    local_dict = allowed_names.copy()
    if x_value is not None:
        local_dict['x'] = x_value
    
    try:
        return eval(expression, {"__builtins__": {}}, local_dict)
    except Exception as e:
        raise e

def plot_function(expression):
    """
    Plot the mathematical function using Plotly.
    """
    # Sanitize the expression
    expression = sanitize_expression(expression)
    
    # Create a range of x values
    x = np.linspace(-10, 10, 400)
    
    try:
        # Evaluate y using the expression with x as a NumPy array
        y = eval_expression(expression, x_value=x)
    except Exception as e:
        st.error(f"Error in expression: {e}")
        return
    
    # Check if y is a valid array
    if not isinstance(y, (list, np.ndarray)):
        st.error("Error: The expression must be a function of 'x'.")
        return
    
    # Check if y has finite values
    if not np.all(np.isfinite(y)):
        st.error("Error: The expression resulted in non-finite values (NaN or Inf).")
        return
    
    # Create the plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=expression))
    fig.update_layout(
        title=f'Plot of {expression}',
        xaxis_title='x',
        yaxis_title='y',
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def add_to_expression(value):
    """
    Add a value to the current expression.
    """
    st.session_state.expression += value

def clear_expression():
    """
    Clear the current expression.
    """
    st.session_state.expression = ""

def calculate_expression():
    """
    Evaluate the current expression and display the result.
    """
    expression = st.session_state.expression
    if not expression:
        st.warning("Please enter an expression to evaluate.")
        return
    try:
        result = eval_expression(expression)
        st.session_state.history.append(f"{expression} = {result}")
        st.success(f"Result: {result}")
    except ZeroDivisionError:
        st.error("Math Error: Division by zero is undefined.")
    except SyntaxError:
        st.error("Syntax Error: Please check the expression for correct syntax.")
    except NameError:
        st.error("Name Error: Ensure all functions and variables are correctly spelled.")
    except Exception as e:
        st.error(f"Error: {e}")

def plot_expression():
    """
    Plot the current expression.
    """
    expression = st.session_state.expression
    if not expression:
        st.warning("Please enter an expression to plot.")
        return
    try:
        plot_function(expression)
    except Exception as e:
        st.error(f"Error: {e}")

# Display the current expression
st.text_input("Expression:", st.session_state.expression, key='expr_input', disabled=True)

# Calculator Buttons Layout
button_labels = [
    ['7', '8', '9', '/', 'sin'],
    ['4', '5', '6', '*', 'cos'],
    ['1', '2', '3', '-', 'tan'],
    ['0', '.', '(', ')', 'sqrt'],
    ['pi', 'x', '^', 'log', 'plot'],
    ['exp', 'abs', '+', '=', 'clear']
]

# Create buttons in a grid layout
for row in button_labels:
    cols = st.columns(len(row))
    for idx, label in enumerate(row):
        btn = cols[idx].button(label)
        if btn:
            if label == '=':
                calculate_expression()
            elif label == 'plot':
                plot_expression()
            elif label == 'clear':
                clear_expression()
                st.success("Cleared the expression.")
            elif label == 'pi':
                add_to_expression(str(np.pi))
            elif label in ['sin', 'cos', 'tan', 'sqrt', 'log', 'exp', 'abs']:
                add_to_expression(label + '(')
            elif label == '^':
                add_to_expression('**')
            else:
                add_to_expression(label)

# Display History
if st.session_state.history:
    st.subheader("📝 Calculation History")
    for entry in reversed(st.session_state.history[-10:]):
        st.write(entry)
