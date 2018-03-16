Description of Visualizations

Visualization #1: Our first visualization is an interactive bar plot that plots
the total number of students that have declared each major. The user can choose
to visualize only males, only females, or all students. NCWIT involvement
(number of students at schools with Academic Alliance or Extension Services)
is distinguished by color. The tooltip shows the total number of students who
graduated and left the institution. We chose to update the y-axis range depending on the information being shown because there are about 6 times as many males as females, so the female-only display would result in a very small visualization if we were to keep the y-axis range constant. This visualization does not include the element of time.

Visualization #2: Our second visualization is an interactive line graph that
plots the ratio of females to males each year. The user can choose to visualize
the sex ratio for the number of new enrollments, total graduated, or left
institution. There are separate lines that represent different types of NCWIT
involvement (Academic Alliance or Extension Services), and these lines can be
toggled on or off by clicking on them in the legend. We chose to keep the y-axis range constant for all of the possible attributes because we are visualizing a ratio between males and females that we expect to remain similar across these attributes.

Visualization #3: Our third visualization is an interactive line graph that
distinguishes between schools that offer Bachelor’s degrees only, Bachelor’s and
Master’s degrees, or Bachelor’s, Master’s, and Ph.D. degrees. The user can
choose to visualize the number of female new enrollments, total graduated, or
left institution each year. These data are normalized by the number of
institutions, and the tooltip shows the number of institutions for each year.
We chose to update the y-xis range depending on the information being shown because
there are about 9 times as many females enrolled per institution than females
who left per institution, so the "left institution" display would result in
a very small visualization if we were to keep the y-axis range constant.

Design Process

We started the design process by using Tableau to explore the data. In doing so,
we realized that there was a significant amount of missing data, and chose to
focus on attributes that were missing the least amount of data. We refined these
initial exploratory visualizations and brainstormed ideas about how to add
interactivity.

Team Roles

Emily was responsible for initial exploration of the data set using Tableau. She
also compiled information about the visualizations and design process. Shruthi
was responsible for creating our first visualization. Shantanu was responsible
for creating our second visualizations. Andrew was responsible for creating our
third visualization. All members were involved with deciding which attributes
to visualize and how to visualize them. We used a bar plot for the first
visualization to maintain distinction between majors, while we used line graphs
for the second and third visualizations to create a sense of continuity over
time.

How to Run the Project

Make sure you have python3 installed.
Also install bokeh with pip3.
After changing directory to the project folder, run "bokeh serve --show visualization1.py" (similarly for 2 & 3).

