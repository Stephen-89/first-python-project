import plotly.express as px

# Sample data: Gapminder dataset
df = px.data.gapminder().query("year == 2007")

# Create an interactive scatter plot
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", 
                 hover_name="country", log_x=True, size_max=60)

# Show the plot
fig.show()