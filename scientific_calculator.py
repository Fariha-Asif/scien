import streamlit as st
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

# Set Plotly renderer for Streamlit
pio.renderers.default = "iframe_connected"

# Title of the App
st.title("📟 Scientific Calculator with Graphing")

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

# Function to sanitize the expression by replacing Unicode minus signs
def sanitize_expression(expression):
    return expression.replace('−', '-')

# Function to evaluate the expression safely
def eval_expression(expression, x_value=None):
    expression = sanitize_expression(expression)
    local_dict = allowed_names.copy()
    if x_value is not None:
        local_dict['x'] = x_value
    try:
        return eval(expression, {"__builtins__": {}}, local_dict)
    except Exception as e:
        raise e

# Function to plot the expression using Plotly
def plot_function(expression):
    expression = sanitize_expression(expression)
    x = np.linspace(-10, 10, 400)
    try:
        y = eval_expression(expression, x_value=x)
    except Exception as e:
        st.error(f"Error in expression: {e}")
        return
    if not isinstance(y, (list, np.ndarray)) or not np.all(np.isfinite(y)):
        st.error("Error: Invalid function.")
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=expression))
    fig.update_layout(title=f'Plot of {expression}', xaxis_title='x', yaxis_title='y')
    st.plotly_chart(fig, use_container_width=True)

# Function to add value to the expression
def add_to_expression(value):
    st.session_state.expression += value

# Function to clear the current expression
def clear_expression():
    st.session_state.expression = ""

# Function to calculate the result of the expression
def calculate_expression():
    expression = st.session_state.expression
    if not expression:
        st.warning("Please enter an expression.")
        return
    try:
        result = eval_expression(expression)
        st.session_state.history.append(f"{expression} = {result}")
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

# Function to plot the current expression
def plot_expression():
    expression = st.session_state.expression
    if not expression:
        st.warning("Please enter an expression to plot.")
        return
    plot_function(expression)

# Create the layout for buttons and display the current expression
st.text_input("Expression:", st.session_state.expression, key='expr_input', disabled=True)

# Calculator Buttons Layout
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.button('7', on_click=add_to_expression, args=('7',))
    st.button('4', on_click=add_to_expression, args=('4',))
    st.button('1', on_click=add_to_expression, args=('1',))
    st.button('0', on_click=add_to_expression, args=('0',))
    st.button('pi', on_click=add_to_expression, args=(str(np.pi),))
    st.button('exp', on_click=add_to_expression, args=('exp(',))

with col2:
    st.button('8', on_click=add_to_expression, args=('8',))
    st.button('5', on_click=add_to_expression, args=('5',))
    st.button('2', on_click=add_to_expression, args=('2',))
    st.button('.', on_click=add_to_expression, args=('.',))
    st.button('x', on_click=add_to_expression, args=('x',))
    st.button('abs', on_click=add_to_expression, args=('abs(',))

with col3:
    st.button('9', on_click=add_to_expression, args=('9',))
    st.button('6', on_click=add_to_expression, args=('6',))
    st.button('3', on_click=add_to_expression, args=('3',))
    st.button('(', on_click=add_to_expression, args=('(',))
    st.button('^', on_click=add_to_expression, args=('**',))
    st.button(')', on_click=add_to_expression, args=(')',))

with col4:
    st.button('/', on_click=add_to_expression, args=('/',))
    st.button('*', on_click=add_to_expression, args=('*',))  # Multiplication button
    st.button('-', on_click=add_to_expression, args=('-',))  # Minus button
    st.button('log', on_click=add_to_expression, args=('log(',))
    st.button('=', on_click=calculate_expression)  # Equals button

with col5:
    st.button('sin', on_click=add_to_expression, args=('sin(',))
    st.button('cos', on_click=add_to_expression, args=('cos(',))
    st.button('tan', on_click=add_to_expression, args=('tan(',))
    st.button('sqrt', on_click=add_to_expression, args=('sqrt(',))
    st.button('plot', on_click=plot_expression)
    st.button('clear', on_click=clear_expression)

# Display Calculation History
if st.session_state.history:
    st.subheader("📝 Calculation History")
    for entry in reversed(st.session_state.history[-10:]):
        st.write(entry)
