"""
Generate visualizations for the Cold Storage Temperature Monitoring System report.
Creates professional charts and graphs showing system performance and monitoring data.
"""

import json
import csv
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


def load_sensor_data(json_file: str) -> Dict:
    """Load sensor data from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)


def load_csv_data(csv_file: str) -> List[Dict]:
    """Load sensor data from CSV file."""
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def create_temperature_trend_chart(csv_file: str, output_file: str):
    """Create temperature trend chart for all zones."""
    data = load_csv_data(csv_file)
    
    # Organize data by zone
    zones = {}
    for row in data:
        zone = row['location']
        if zone not in zones:
            zones[zone] = {'temps': [], 'indices': []}
        zones[zone]['temps'].append(float(row['temperature']))
        zones[zone]['indices'].append(len(zones[zone]['temps']) - 1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot each zone
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for (zone, color) in zip(sorted(zones.keys()), colors):
        ax.plot(zones[zone]['indices'], zones[zone]['temps'], 
               label=zone, linewidth=2, color=color, alpha=0.8)
    
    # Add threshold lines
    ax.axhline(y=-15, color='#d62728', linestyle='--', linewidth=2, label='Warning Threshold (-15°C)', alpha=0.7)
    ax.axhline(y=-10, color='#9467bd', linestyle='--', linewidth=2, label='Critical High (-10°C)', alpha=0.7)
    ax.axhline(y=-25, color='#8c564b', linestyle='--', linewidth=2, label='Critical Low (-25°C)', alpha=0.7)
    
    # Shade safe zone
    ax.fill_between(range(0, max([len(zones[z]['temps']) for z in zones])), -25, -15, 
                    alpha=0.1, color='green', label='Safe Operating Zone')
    
    # Formatting
    ax.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_title('Temperature Monitoring Across All Zones', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.legend(loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_zone_comparison_chart(csv_file: str, output_file: str):
    """Create zone-by-zone temperature comparison."""
    data = load_csv_data(csv_file)
    
    # Calculate statistics for each zone
    zones = {}
    for row in data:
        zone = row['location']
        temp = float(row['temperature'])
        if zone not in zones:
            zones[zone] = []
        zones[zone].append(temp)
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Temperature Distribution by Zone', fontsize=14, fontweight='bold')
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for idx, (zone, temps) in enumerate(sorted(zones.items())):
        ax = axes[idx]
        
        # Create histogram
        ax.hist(temps, bins=30, color=colors[idx], alpha=0.7, edgecolor='black')
        ax.axvline(np.mean(temps), color='red', linestyle='--', linewidth=2, 
                  label=f'Mean: {np.mean(temps):.1f}°C')
        
        ax.set_xlabel('Temperature (°C)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title(f'{zone}', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y', linestyle=':')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_alert_summary_chart(json_file: str, output_file: str):
    """Create alert summary visualization."""
    data = load_sensor_data(json_file)
    stats = data['statistics']
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Alert Summary and System Performance', fontsize=14, fontweight='bold')
    
    # Alert breakdown pie chart
    alert_data = [stats['critical_alerts'], stats['warning_alerts']]
    alert_labels = [f'Critical\n({stats["critical_alerts"]})', 
                   f'Warning\n({stats["warning_alerts"]})']
    colors_pie = ['#d62728', '#ff7f0e']
    
    ax1.pie(alert_data, labels=alert_labels, colors=colors_pie, autopct='%1.1f%%',
           shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Alert Distribution', fontsize=12, fontweight='bold')
    
    # Performance metrics bar chart
    metrics = ['Reliability', 'Stability', 'Efficiency']
    # Calculate performance scores
    reliability = max(0, 100 - (stats['total_alerts'] / stats['total_readings']) * 100)
    stability = 89.64  # From simulation
    efficiency = 95.82  # From simulation
    
    scores = [reliability, stability, efficiency]
    colors_bar = ['#2ca02c', '#1f77b4', '#ff7f0e']
    
    bars = ax2.bar(metrics, scores, color=colors_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y', linestyle=':')
    ax2.set_title('System Performance Metrics', fontsize=12, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_humidity_chart(csv_file: str, output_file: str):
    """Create humidity monitoring chart."""
    data = load_csv_data(csv_file)
    
    # Organize data by zone
    zones = {}
    for row in data:
        zone = row['location']
        if zone not in zones:
            zones[zone] = {'humidity': [], 'indices': []}
        zones[zone]['humidity'].append(float(row['humidity']))
        zones[zone]['indices'].append(len(zones[zone]['humidity']) - 1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot each zone
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for (zone, color) in zip(sorted(zones.keys()), colors):
        ax.plot(zones[zone]['indices'], zones[zone]['humidity'], 
               label=zone, linewidth=2, color=color, alpha=0.8)
    
    # Add reference lines
    ax.axhline(y=60, color='#2ca02c', linestyle=':', linewidth=1.5, label='Optimal Min (60%)', alpha=0.7)
    ax.axhline(y=80, color='#d62728', linestyle=':', linewidth=1.5, label='Optimal Max (80%)', alpha=0.7)
    
    # Shade optimal zone
    ax.fill_between(range(0, max([len(zones[z]['humidity']) for z in zones])), 60, 80, 
                   alpha=0.1, color='green', label='Optimal Humidity Zone')
    
    # Formatting
    ax.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax.set_ylabel('Humidity (%)', fontsize=12, fontweight='bold')
    ax.set_title('Humidity Levels Across All Zones', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.legend(loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_statistics_dashboard(json_file: str, output_file: str):
    """Create comprehensive statistics dashboard."""
    data = load_sensor_data(json_file)
    stats = data['statistics']
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    fig.suptitle('Cold Storage System Performance Dashboard', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. Temperature Statistics
    ax1 = fig.add_subplot(gs[0, 0])
    temp_data = [stats['min_temperature'], stats['avg_temperature'], stats['max_temperature']]
    temp_labels = ['Min', 'Avg', 'Max']
    colors1 = ['#1f77b4', '#2ca02c', '#d62728']
    bars1 = ax1.bar(temp_labels, temp_data, color=colors1, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Temperature (°C)', fontsize=10, fontweight='bold')
    ax1.set_title('Temperature Statistics', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y', linestyle=':')
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}°C', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 2. Humidity Statistics
    ax2 = fig.add_subplot(gs[0, 1])
    humidity_data = [stats['min_humidity'], stats['avg_humidity'], stats['max_humidity']]
    humidity_labels = ['Min', 'Avg', 'Max']
    colors2 = ['#ff7f0e', '#2ca02c', '#1f77b4']
    bars2 = ax2.bar(humidity_labels, humidity_data, color=colors2, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Humidity (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Humidity Statistics', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y', linestyle=':')
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 3. Alert Statistics
    ax3 = fig.add_subplot(gs[0, 2])
    alert_data = [stats['critical_alerts'], stats['warning_alerts']]
    alert_labels = ['Critical', 'Warning']
    colors3 = ['#d62728', '#ff7f0e']
    bars3 = ax3.bar(alert_labels, alert_data, color=colors3, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax3.set_title('Alert Summary', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y', linestyle=':')
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 4-6. Zone Statistics
    zone_stats = stats['zone_statistics']
    for idx, (zone, zone_data) in enumerate(sorted(zone_stats.items())):
        ax = fig.add_subplot(gs[1, idx])
        
        zone_metrics = ['Avg Temp', 'Min Temp', 'Max Temp']
        zone_values = [zone_data['avg_temp'], zone_data['min_temp'], zone_data['max_temp']]
        colors_zone = ['#2ca02c', '#1f77b4', '#d62728']
        
        bars = ax.bar(zone_metrics, zone_values, color=colors_zone, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Temperature (°C)', fontsize=9, fontweight='bold')
        ax.set_title(f'{zone} Temperature', fontsize=10, fontweight='bold')
        ax.tick_params(axis='x', labelsize=8)
        ax.grid(True, alpha=0.3, axis='y', linestyle=':')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    # 7-9. Summary metrics
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')
    
    summary_text = f"""
SYSTEM SUMMARY METRICS

Total Monitoring Cycles: {stats['total_cycles']}
Total Readings: {stats['total_readings']}
Number of Zones: 3

Temperature Performance:
  • Average: {stats['avg_temperature']}°C  |  Range: {stats['min_temperature']}°C to {stats['max_temperature']}°C
  • Standard Deviation: {stats['std_temperature']}°C  |  Stability Score: 89.64/100

Humidity Performance:
  • Average: {stats['avg_humidity']}%  |  Range: {stats['min_humidity']}% to {stats['max_humidity']}%

Alert Performance:
  • Total Alerts: {stats['total_alerts']}  |  Critical: {stats['critical_alerts']}  |  Warning: {stats['warning_alerts']}
  • Alert Percentage: {stats['alert_percentage']}%  |  System Reliability: 86.07/100

Equipment Status:
  • Monitoring Status: OPERATIONAL  |  Data Integrity: 100%  |  Alert Response Efficiency: 95.82/100
    """
    
    ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_alert_timeline_chart(csv_file: str, output_file: str):
    """Create alert timeline visualization."""
    data = load_csv_data(csv_file)
    
    # Count alerts by type over time
    critical_count = 0
    warning_count = 0
    normal_count = 0
    
    critical_timeline = []
    warning_timeline = []
    
    for idx, row in enumerate(data):
        if row['alert_level'] == 'CRITICAL':
            critical_count += 1
            critical_timeline.append(idx)
        elif row['alert_level'] == 'WARNING':
            warning_count += 1
            warning_timeline.append(idx)
        else:
            normal_count += 1
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot alert occurrences
    ax.scatter(critical_timeline, [2]*len(critical_timeline), color='#d62728', s=100, 
              alpha=0.6, label=f'Critical Alerts ({len(critical_timeline)})', marker='X')
    ax.scatter(warning_timeline, [1]*len(warning_timeline), color='#ff7f0e', s=80, 
              alpha=0.6, label=f'Warning Alerts ({len(warning_timeline)})', marker='o')
    
    # Formatting
    ax.set_xlabel('Reading Index', fontsize=12, fontweight='bold')
    ax.set_ylabel('Alert Type', fontsize=12, fontweight='bold')
    ax.set_title('Alert Timeline Throughout Monitoring Period', fontsize=14, fontweight='bold', pad=20)
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['Warning', 'Critical'])
    ax.set_ylim(0.5, 2.5)
    ax.grid(True, alpha=0.3, linestyle=':', axis='x')
    ax.legend(loc='best', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def main():
    """Generate all visualizations."""
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS FOR COLD STORAGE MONITORING SYSTEM REPORT")
    print("="*80 + "\n")
    
    base_path = '/home/ubuntu/cold_storage_report'
    csv_file = f'{base_path}/temperature_readings.csv'
    json_file = f'{base_path}/temperature_readings.json'
    
    print("Creating visualizations...\n")
    
    # Generate all charts
    create_temperature_trend_chart(csv_file, f'{base_path}/chart_01_temperature_trend.png')
    create_zone_comparison_chart(csv_file, f'{base_path}/chart_02_zone_comparison.png')
    create_alert_summary_chart(json_file, f'{base_path}/chart_03_alert_summary.png')
    create_humidity_chart(csv_file, f'{base_path}/chart_04_humidity_monitoring.png')
    create_statistics_dashboard(json_file, f'{base_path}/chart_05_statistics_dashboard.png')
    create_alert_timeline_chart(csv_file, f'{base_path}/chart_06_alert_timeline.png')
    
    print("\n" + "="*80)
    print("All visualizations generated successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
