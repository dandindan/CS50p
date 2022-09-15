#Bokeh Libraries
from bokeh.io import output_file
from bokeh.plotting import figure, show

#render the static HTML to file called out_file
output_file('output_file_test.html', title='Empty Bokeh figure')

#set up a geneic figure()object
fig = figure()

# See what it look like
show(fig)
