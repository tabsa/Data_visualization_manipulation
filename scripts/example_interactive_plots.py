# Interactive plots using Altair package

#%% Import packages
import numpy as np
import pandas as pd
import altair as alt
from pathlib import Path
import streamlit as st

#%% Class section
@st.cache()
def get_data(file, cols, n_sample=1000):
    df = pd.read_csv(file, usecols=cols) # Read the file
    return df[(df.Price < 3_000_000) & (df.Landsize < 1200)].sample(n_sample).reset_index(drop=True) # Filter the DataFrame

class dashboard:
    def __init__(self, dir, file):
        self.cols_name = ['Price', 'Landsize', 'Distance', 'Type', 'Regionname']
        self.file_path = dir / file
        self.df = get_data(self.file_path, self.cols_name) # Get df with n_sample = 1000 as default (you can change it)

    def run_dash(self):
        self.sec_head_title() # First section
        self.sec_exploratory_analysis() # Second section
        self.sec_interactive_plots() # Third section
        self.sec_final_analysis() # Last section
        return 0

    def sec_head_title(self):
        st.title('Interactive plots with Altair package')
        st.write('Altair is a powerful library in terms of data transformations and creating interactive plots. '
                 'We will test **Altair functions** with the dataset available on Kaggle about the *Melbourne housing info*.')
        st.markdown("""
            Three components with Altair package:
            -   **Selection:** Captures interactions from the user. In other words, it selects a part of the visualization
            -   **Condition:** Changes or customizes the elements based on the selection. In order to see an action, we need to attach a selection to a condition
            -   **Bind:** It is a property of the selection and creates a two-way binding between a selection and input
            """)

    def sec_exploratory_analysis(self):
        st.header('Static visualization')
        st.write('Before starting on the interactive plots, it is better to briefly show the code with the basic **Altair syntax**:')
        with st.echo(code_location='below'):
            scatter_fig = alt.Chart(self.df).mark_circle(size=50).encode(
                                    x = 'Price', y = 'Distance', color = 'Type'
                                    ).properties(height=350, width=500)
            st.write(scatter_fig)
        st.markdown('''
            The data can be in the form of a DataFrame, then describe the type of visualization (e.g. mark_circle, mark_line, and so on).
            The encode function specifies what to plot in the given DataFrame, our example (x=Price, y=Distance color=Type).
            Finally, we specify certain *properties* like **height** and **width**.
        ''')

    def sec_interactive_plots(self):
        st.header('Dynamic visualization in plots')
        st.write('Some part of the plot seems too overlapped in terms of the dots. It would look better if we can also view data points that belong to a specific type.')
        with st.echo(code_location='below'):
            sel_option = alt.selection_multi(fields=['Type'], bind='legend') # Select option with binding_selection into the 'legend'
            scatter_fig = alt.Chart(self.df).mark_circle(size=50).encode(
                x = 'Price', y = 'Distance', color = 'Type',
                opacity = alt.condition(sel_option, alt.value(1), alt.value(0.1)) # Add the sel_option with removing the rest through opacity property
            ).properties(height=350, width=500).add_selection(sel_option)
            st.write(scatter_fig)
        st.markdown('''
        The second example will create a scatter plot and a histogram using the *distance*, *Landsize* and *Price* features. 
        The histogram will be updated based on the selected area on the scatter plot.
        ''')
        with st.echo(code_location='below'):
            sel_option = alt.selection_interval() # Interval allows us to select an area on the plot
            # Normal scatter plot for Landsize vs Distance
            scatter_graph = alt.Chart(self.df).mark_circle(size=50).encode(
                x = 'Landsize', y = 'Distance', color = 'Type'
            ).properties(height=350, width=400).add_selection(sel_option)
            # The histogram will be created through the selection_intervale as a transform filter
            hist_graph = alt.Chart(self.df).mark_bar().encode(
                alt.X('Price:Q', bin=True), alt.Y('count()') # Filter based on the selection (X = Price, Y = hist)
            ).properties(height=350, width=250).transform_filter(sel_option)
            fig = scatter_graph | hist_graph # Merge the 2 plots
            st.write(fig)
        st.markdown('''
        The histogram is updated based on the data points of the **selected area** on the scatter plot (try to select different areas). 
        Thus, we are able to see the Price distribution of the selected area. **Remember**: 
        -   We can use other plots besides the histogram, the applications are endless and what is important is the *transform_filter* used in the **hist_graph**.
        -   Other **selection functions** can be used in this application, like the one used above (selection_multi)
        -   This is done through the selection (alt.selection_interval or others) and condition (alt.transform_filter) that are available as **Altair functions**
        ''')
    def sec_final_analysis(self):
        st.header('Alternative interaction on the plots')
        st.write('Final example that switches the roles on the two plots above, in order to better understand the concepts of the selection and condition properties:')
        with st.echo(code_location='below'):
            # Same sel_option (selection_interval)
            sel_option = alt.selection_interval()
            scatter_graph = alt.Chart(self.df).mark_circle(size=50).encode(
                x = 'Landsize', y = 'Distance', color = 'Type'
            ).properties(height=350, width=400).transform_filter(sel_option)
            hist_graph = alt.Chart(self.df).mark_bar().encode(
                alt.X('Price:Q', bin=True), alt.Y('count()')
            ).properties(height=350, width=250).add_selection(sel_option)
            fig = hist_graph | scatter_graph
            st.write(fig)
        st.title('Takeaway messages')
        st.markdown('''
        -   Endless applications with the *selection* and *condition* properties
        -   **Altair** is quite flexible in terms of adding interactive components to the visualiation
        -   Example plots could be functions where some properties change depending on input parameters for an **agile implementation**
        -   As with any other subject, practice makes perfect!!!
        ''')

#%% Main script
if __name__ == '__main__':
    wok_dir = Path.cwd()
    file = 'Data/melb_data.csv'
    app = dashboard(wok_dir, file) # Call the dashboard class
    app.run_dash()
