import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

demographics = pd.read_csv('C:/Users/gcat9/OneDrive/Desktop/DATA 501/Capstone Data/demographics_clean.csv').drop(columns=['Unnamed: 0'])
chemicals = pd.read_csv('C:/Users/gcat9/OneDrive/Desktop/DATA 501/Capstone Data/chemicals_clean.csv').drop(columns=['Unnamed: 0'])
occupation = pd.read_csv('C:/Users/gcat9/OneDrive/Desktop/DATA 501/Capstone Data/occupation_clean.csv', low_memory=False).drop(columns=['Unnamed: 0'])
mortality = pd.read_csv('C:/Users/gcat9/OneDrive/Desktop/DATA 501/Capstone Data/mortality_clean.csv').drop(columns=['Unnamed: 0'])

nhanes_merged = pd.merge(demographics, chemicals, on=['SEQN', 'SEQN_new', 'SDDSRVYR'], how='outer')
nhanes_merged = pd.merge(nhanes_merged, occupation, on=['SEQN', 'SEQN_new', 'SDDSRVYR'], how='outer')
nhanes_merged = pd.merge(nhanes_merged, mortality, on=['SEQN', 'SEQN_new', 'SDDSRVYR'], how='outer')

# PFAS variables
pfas_variables = [
    'VNURXPFBA', 'LBXPFBS', 'VNURXPFBS', 
    'VNURXPFHA', 'LBXPFHS', 'VNURXPFHS', 'VNURXGENX'
]

# Set the style of seaborn
sns.set(style="whitegrid", palette="pastel")

# Determine the number of rows needed for the subplots
n_rows = len(pfas_variables) // 2 + len(pfas_variables) % 2

# Create a figure with subplots
fig, axes = plt.subplots(nrows=n_rows, ncols=2, figsize=(12, 5 * n_rows))
axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

# Loop through the variables and create a histogram for each
for i, var in enumerate(pfas_variables):
    # Create a histogram plot
    ax = sns.histplot(data=nhanes_merged, x=var, kde=True, color='blue', ax=axes[i], binwidth=0.1)
    
    # Set the title with appropriate spacing to prevent overlapping
    ax.set_title(f'Distribution of {var.replace("VNURX","").replace("LBX","")}', fontsize=12, pad=3)
    
    # Set labels
    ax.set_xlabel('Concentration (ng/mL)', fontsize=8)
    ax.set_ylabel('Frequency', fontsize=8)
    
    # Set x-axis limits based on the data quantiles to better fit the distribution
    ax.set_xlim(left=nhanes_merged[var].min(), right=nhanes_merged[var].quantile(0.975))  # Adjust as needed

# Remove empty subplots if the number of variables is odd
if len(pfas_variables) % 2 != 0:
    fig.delaxes(axes[-1])

# Adjust the layout
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.3)  # Adjust spacing between plots

# Display the plot
plt.show()


# # Set the style and context for the plot
# sns.set(style="whitegrid", context='talk')

# # Create the boxplot
# ax = sns.boxplot(data=nhanes_merged, x='DMDHRGND', y='VNURXPFBA', palette='pastel')

# # Add mean line
# meanlineprops = {'linestyle':'-', 'linewidth':2, 'color':'red'}
# sns.boxplot(data=nhanes_merged, x='DMDHRGND', y='VNURXPFBA', showmeans=True, meanline=True, meanprops=meanlineprops, palette='pastel')

# # Update the labels and title
# ax.set_title('PFBA Concentrations by Gender', fontsize=18)
# ax.set_xlabel('Gender', fontsize=14)
# ax.set_ylabel('Concentration (ng/mL)', fontsize=14)

# # Set gender category names
# ax.set_xticklabels(['Male', 'Female'])

# # Despine the plot for a cleaner look
# sns.despine()

# # Display the plot
# plt.tight_layout()
# plt.show()

# Set the style and context for the plot
sns.set(style="whitegrid", context='talk')

# Determine the number of rows needed for the subplots
n_rows = len(pfas_variables) // 2 + len(pfas_variables) % 2

# Create a figure with subplots
fig, axes = plt.subplots(nrows=n_rows, ncols=2, figsize=(14, 10))  # Adjust figsize as needed
axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

# Loop through the variables and create a boxplot for each
for i, var in enumerate(pfas_variables):
    ax = axes[i]
    sns.boxplot(data=nhanes_merged, x='DMDHRGND', y=var, palette='pastel', ax=ax)

    # Calculate the means for each gender within the variable
    means = nhanes_merged.groupby('DMDHRGND')[var].mean().values

    # Draw mean lines and add labels to the right side of the lines
    for j, mean in enumerate(means):
        # Add a horizontal line for the mean
        ax.axhline(mean, color='red', linestyle='-', linewidth=2, xmin=j-0.45, xmax=j+0.45)
        # Add a text label for the mean value
        ax.text(j+0.2, mean, f'{mean:.2f}', ha='left', va='bottom', color='blue', fontsize=10)

    # Update the title for each subplot
    ax.set_title(f'{var} Concentrations by Gender', fontsize=14)
    
    # Remove the xlabel
    ax.set_xlabel('')
    ax.set_ylabel('Concentration (ng/mL)', fontsize=12)

    # Set gender category names for each subplot
    ax.set_xticklabels(['Male', 'Female'])

# Remove empty subplots if the number of PFAS variables is odd
if len(pfas_variables) % 2 != 0:
    fig.delaxes(axes[-1])

# Adjust the layout and spacing
plt.tight_layout()
plt.subplots_adjust(hspace=0.4, wspace=0.3)  # Adjust spacing between plots

# Display the plot
plt.show()


# # Set the style and context for the plot
# sns.set(style="whitegrid", context='talk')

# # Create the boxplot
# ax = sns.boxplot(data=nhanes_merged, x='DMDHRGND', y='VNURXPFBA', palette='pastel')

# # Calculate the means
# means = nhanes_merged.groupby('DMDHRGND')['VNURXPFBA'].mean().values

# # Draw mean lines and add labels to the left side of the lines
# for i, mean in enumerate(means):
#     # Add a horizontal line for the mean
#     ax.axhline(mean, color='red', linestyle='-', linewidth=2, xmin=i-0.45, xmax=i+0.45)
#     # Add a text label for the mean value
#     ax.text(i+0.2, mean, f'{mean:.2f}', ha='left', va='bottom', color='blue', fontsize=10)

# # Update the labels and title
# ax.set_title('PFBA Concentrations by Gender', fontsize=18)
# ax.set_xlabel('Gender', fontsize=14)
# ax.set_ylabel('Concentration (ng/mL)', fontsize=14)

# # Set gender category names
# ax.set_xticklabels(['Male', 'Female'])

# # Despine the plot for a cleaner look
# sns.despine()

# # Display the plot
# plt.tight_layout()
# plt.show()


# Filter the dataset to exclude 'Refused' and 'Don't know' responses
filtered_data = nhanes_merged[nhanes_merged['DMDBORN4'].isin([1, 2])]

# Create the pairplot with the filtered data
pair_plot = sns.pairplot(data=filtered_data, vars=pfas_variables, 
                         hue='DMDBORN4', palette='Set1', 
                         markers=["o", "s"])

# Set the title
pair_plot.fig.suptitle('Pairwise Relationships Between PFAS Variables and Birthplace', size=16)
pair_plot._legend.set_title('Birthplace')
pair_plot._legend.set_label(['US', 'Other'])

# Adjust the layout to prevent the title from overlapping
plt.subplots_adjust(top=0.9)

# Display the plot
plt.show()

