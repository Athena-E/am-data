import matplotlib.pyplot as plt

def plot_sensor_data(df, sensor_id, day, col1='co2', col2=None):
    """
    Plots two columns of data for a single sensor on a given day using dual y-axes.
    
    Args:
        df (pd.DataFrame): The DataFrame containing sensor data.
        sensor_id (int or str): The ID of the sensor to plot.
        day (str): The date to filter the data (format: 'YYYY-MM-DD').
        col1 (str): The first column to plot (default: 'co2'), will be on left y-axis
        col2 (str): The second column to plot (default: 'temperature'), will be on right y-axis
    """
    # Filter for the selected sensor and date
    df_filtered = df[(df['sensor_id'] == sensor_id) & 
                    (df['date_group'].dt.strftime('%Y-%m-%d') == day)]
    
    if df_filtered.empty:
        print(f"No data found for sensor {sensor_id} on {day}.")
        return
    
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot first column on primary y-axis
    color1 = 'royalblue'
    ax1.set_xlabel("Time", fontsize=12)
    ax1.set_ylabel(col1, color=color1, fontsize=12)
    line1 = ax1.plot(df_filtered['timestamp'], df_filtered[col1], 
                     color=color1, label=col1)
    ax1.tick_params(axis='y', labelcolor=color1)

    lines = line1
    
    if col2:
    # Create secondary y-axis and plot second column
        ax2 = ax1.twinx()
        color2 = 'darkred'
        ax2.set_ylabel(col2, color=color2, fontsize=12)
        line2 = ax2.plot(df_filtered['timestamp'], df_filtered[col2], 
                        color=color2, label=col2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # Add title
        plt.title(f"{col1} and {col2} for Sensor {sensor_id} on {day}", 
                fontsize=14, pad=20)
        
        lines = line1 + line2

    plt.title(f"{col1} for Sensor {sensor_id} on {day}", 
                fontsize=14, pad=20)


    # Combine legends from both axes
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    
    # Set x-axis limits and format
    plt.xlim(df_filtered['timestamp'].min(), df_filtered['timestamp'].max())
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    
    # Add grid but only for the primary axis
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    plt.show()
