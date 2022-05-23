# LSGI3315 Group 6's Project - Task 3 Group Task (70% of total mark of Project)
# Task 3 (Bonus): Using matplotlib Package to depict the line graph of transportation accessibility

# Group mate 1: Wei Jun, Kenny - 20084091D
# Group mate 2: Tang Justin Hayse Chi Wing G. - 20016345D

# Import the matplotlib and other Python Package/ Module
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import interp1d

# plt.style.use('dark_background')

x_labels = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]  # Labelling X-Axis
y_labels = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]  # Labelling Y-Axis

x_1 = np.array([20, 40, 60, 80, 100, 150, 200])
y_1 = np.array([17, 52, 76, 84, 88, 94, 97])

x_2 = np.array([20, 40, 60, 80, 100, 150, 200])
y_2 = np.array([20, 60, 87, 89, 92, 96, 97])

x_3 = np.array([20, 40, 60, 80, 100, 150, 200])
y_3 = np.array([16, 52, 85, 90, 95, 97, 97])

x_4 = np.array([20, 40, 60, 80, 100, 150, 200])
y_4 = np.array([6, 29, 45, 62, 82, 97, 100])

x_5 = np.array([20, 40, 60, 80, 100, 150, 200])
y_5 = np.array([4, 7, 21, 54, 79, 96, 96])

x_6 = np.array([20, 40, 60, 80, 100, 150, 200])
y_6 = np.array([0, 25, 55, 70, 91, 100, 100])

x_7 = np.array([20, 40, 60, 80, 100, 150, 200])
y_7 = np.array([0, 0, 0, 0, 0, 4, 8])

x_1_new = np.linspace(x_1.min(), x_1.max())
x_2_new = np.linspace(x_2.min(), x_2.max())
x_3_new = np.linspace(x_2.min(), x_3.max())
x_4_new = np.linspace(x_2.min(), x_4.max())
x_5_new = np.linspace(x_2.min(), x_4.max())
x_6_new = np.linspace(x_2.min(), x_4.max())
x_7_new = np.linspace(x_2.min(), x_4.max())

# Determine the line is linear or quadratic
f = interp1d(x_1, y_1, kind='linear')  # quadratic
y_1_smooth = f(x_1_new)

f = interp1d(x_2, y_2, kind='linear')
y_2_smooth = f(x_2_new)

f = interp1d(x_3, y_3, kind='linear')
y_3_smooth = f(x_3_new)

f = interp1d(x_4, y_4, kind='linear')
y_4_smooth = f(x_4_new)

f = interp1d(x_5, y_5, kind='linear')
y_5_smooth = f(x_5_new)

f = interp1d(x_6, y_6, kind='linear')
y_6_smooth = f(x_6_new)

f = interp1d(x_7, y_7, kind='linear')
y_7_smooth = f(x_7_new)


# Determine the color and other characteristics for the lines
plt.plot(x_1_new, y_1_smooth, '--', color='red')
plt.scatter(x_1, y_1, color='red', marker=',')
#
plt.plot(x_2_new, y_2_smooth, '--', color='orange')
plt.scatter(x_2, y_2, color='orange', marker=',')

plt.plot(x_3_new, y_3_smooth, '--', color='gold')
plt.scatter(x_3, y_3, color='gold', marker=',')

plt.plot(x_4_new, y_4_smooth, '--', color='lime')
plt.scatter(x_4, y_4, color='lime', marker=',')

plt.plot(x_5_new, y_5_smooth, '--', color='forestgreen')
plt.scatter(x_5, y_5, color='forestgreen', marker=',')

plt.plot(x_6_new, y_6_smooth, '--', color='blue')
plt.scatter(x_6, y_6, color='blue', marker=',')

plt.plot(x_7_new, y_7_smooth, '--', color='purple')
plt.scatter(x_7, y_7, color='purple', marker=',')

# Title of line graph
plt.title('LSGI3315 GIS Engineering\nGroup 6 - Bonus Part\nEvaluating the Transportation Accessibility of\nDifferent Sports and Outdoor Facilities in Hong Kong')

# X axis
plt.xlabel('Searching Distance (Meter)')

# Y axis
plt.ylabel('Percentage of the Facility(s) within the Searching Distance')


# The components of the legend
patch1 = mpatches.Patch(color='red', label='Basketball Court')
patch2 = mpatches.Patch(color='orange', label='Badminton Count')
patch3 = mpatches.Patch(color='gold', label='Fitness Centre')
patch4 = mpatches.Patch(color='lime', label='Park Garden')
patch5 = mpatches.Patch(color='forestgreen', label='Sports Ground')
patch6 = mpatches.Patch(color='blue', label='Swimming Pool')
patch7 = mpatches.Patch(color='purple', label='Country Park')
# The location and the items to be shown
plt.legend(handles=[patch1, patch2, patch3, patch4, patch5, patch6, patch7], loc='center right', title='Legend', title_fontsize=14)

# The shadow of the line (if necessary)
plt.fill_between(x_1, y_1, color='dodgerblue', alpha=0)
plt.fill_between(x_2, y_2, color='dodgerblue', alpha=0)
plt.fill_between(x_3, y_3, color='dodgerblue', alpha=0)
plt.fill_between(x_4, y_4, color='dodgerblue', alpha=0)
plt.fill_between(x_5, y_5, color='dodgerblue', alpha=0)
plt.fill_between(x_6, y_6, color='saddlebrown', alpha=0)
plt.fill_between(x_7, y_7, color='saddlebrown', alpha=0)

plt.xticks(x_labels)
plt.yticks(y_labels)

ax = plt.gca()
ax.set_xlim([15, 205])  # The range of X axis
ax.set_ylim([-1.5, 101.5])  # The range of Y axis
ax.ticklabel_format(style='plain')
# plt.axhline(y=90, color='black', linestyle='--')  # add the straight line if necessary
plt.margins(100)
plt.grid(True)

print('The line graph of transportation accessibility is generated!')
plt.show()  # plot the line graph
