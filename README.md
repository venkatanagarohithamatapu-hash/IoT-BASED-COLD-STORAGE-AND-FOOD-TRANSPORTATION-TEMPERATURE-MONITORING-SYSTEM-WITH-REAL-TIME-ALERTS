# IoT-Based Cold Storage and Food Transportation Temperature Monitoring System

## Project Overview

This project implements a comprehensive IoT-based temperature monitoring system designed to ensure food safety and quality throughout the cold chain. The system continuously monitors environmental conditions in cold storage facilities and refrigerated transportation units, providing real-time alerts when temperatures deviate from safe operating ranges.

## System Architecture

The system consists of the following key components:

### 1. Temperature Sensors
- Simulates realistic temperature readings with natural fluctuations
- Supports multiple monitoring zones (Zone A, Zone B, Zone C)
- Includes anomaly simulation for equipment malfunctions and door openings

### 2. Humidity Sensors
- Monitors relative humidity levels in storage environments
- Provides continuous humidity tracking across all zones

### 3. Alert Generation System
- Multi-tiered alert system (Normal, Warning, Critical)
- Configurable temperature thresholds
- Automatic alert logging with timestamps

### 4. Equipment Monitoring
- Tracks cooling equipment operational status
- Simulates maintenance requirements and offline events
- Provides equipment reliability metrics

### 5. Data Analysis and Visualization
- Comprehensive statistical analysis of temperature trends
- Professional visualization dashboards
- Performance metrics calculation

## Files Included

### Core Python Modules

1. **cold_storage_monitoring.py** (600+ lines)
   - Main simulation engine
   - Sensor classes: TemperatureSensor, HumiditySensor
   - Alert system: AlertGenerator
   - Equipment monitoring: EquipmentMonitor
   - Main controller: ColdStorageMonitoringSystem
   - Performance analysis: SystemPerformanceAnalyzer

2. **generate_visualizations.py** (500+ lines)
   - Chart generation functions
   - Temperature trend visualization
   - Zone comparison analysis
   - Alert summary dashboards
   - Humidity monitoring charts
   - Statistics dashboard creation
   - Alert timeline visualization

3. **generate_report.py** (400+ lines)
   - Word document generation
   - Professional formatting
   - Chapter structure implementation
   - Image embedding
   - Table of contents creation

### Data Files

- **temperature_readings.csv**: Raw sensor readings in CSV format
- **temperature_readings.json**: Structured sensor data with metadata
- **alert_history.csv**: Complete alert event log

### Visualization Output

- **chart_01_temperature_trend.png**: Temperature monitoring across all zones
- **chart_02_zone_comparison.png**: Zone-by-zone temperature distribution
- **chart_03_alert_summary.png**: Alert statistics and performance metrics
- **chart_04_humidity_monitoring.png**: Humidity levels across zones
- **chart_05_statistics_dashboard.png**: Comprehensive performance dashboard
- **chart_06_alert_timeline.png**: Alert occurrence timeline

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Required Packages

```bash
pip install -r requirements.txt
```

The following packages are required:

- python-docx (for Word document generation)
- matplotlib (for data visualization)
- numpy (for numerical computations)

## Usage

### Running the Simulation

```bash
python3 cold_storage_monitoring.py
```

This will:
- Execute 1000 monitoring cycles across 3 zones
- Generate 3000 sensor readings
- Create alert events based on temperature thresholds
- Export data to CSV and JSON formats
- Display comprehensive statistics

### Generating Visualizations

```bash
python3 generate_visualizations.py
```

This will create 6 professional visualization charts:
1. Temperature trend monitoring
2. Zone comparison histograms
3. Alert summary dashboard
4. Humidity monitoring chart
5. Statistics dashboard
6. Alert timeline

### Generating the Report

```bash
python3 generate_report.py
```

This will generate a comprehensive Word document report including:
- Executive summary
- Organization overview
- Cold chain management concepts
- Problem assessment
- System implementation details
- Results and performance evaluation
- Embedded visualizations
- References

## Key Features

### Real-Time Monitoring
- Continuous temperature and humidity tracking
- Multi-zone simultaneous monitoring
- Precise timestamp recording

### Intelligent Alert System
- Warning threshold alerts for early detection
- Critical threshold alerts for immediate action
- Comprehensive alert history logging

### Data Analysis
- Statistical computation of temperature trends
- Humidity level analysis
- Equipment performance tracking
- System reliability scoring

### Visualization
- Professional-grade charts and graphs
- Trend analysis visualizations
- Performance dashboard
- Alert timeline representation

### Compliance and Reporting
- Automatic data export (CSV and JSON)
- Comprehensive performance metrics
- Audit trail of all events
- Professional report generation

## System Performance Metrics

Based on the simulation results:

| Metric | Value |
|--------|-------|
| Total Monitoring Cycles | 1000 |
| Total Readings | 3000 |
| Average Temperature | -16.77°C |
| Temperature Range | -23.31°C to -2.28°C |
| Average Humidity | 65.14% |
| Total Alerts | 418 |
| Critical Alerts | 35 |
| Warning Alerts | 383 |
| System Reliability Score | 86.07/100 |
| Temperature Stability Score | 89.64/100 |
| Alert Response Efficiency | 95.82/100 |

## Configuration

### Temperature Thresholds

The system uses the following default thresholds:

- **Optimal Range**: -18°C (standard freezer temperature)
- **Warning Threshold**: -15°C (approaching unsafe levels)
- **Critical High**: -10°C (too warm, spoilage risk)
- **Critical Low**: -25°C (dangerously cold)

These thresholds can be customized when initializing the ColdStorageMonitoringSystem:

```python
system = ColdStorageMonitoringSystem(
    num_zones=3,
    temp_warning_high=-15.0,
    temp_critical_high=-10.0,
    temp_critical_low=-25.0
)
```

## Output Files

After running the simulation, the following files are generated:

1. **temperature_readings.csv** - Detailed sensor readings
2. **temperature_readings.json** - Structured data with statistics
3. **alert_history.csv** - Complete alert log
4. **chart_*.png** - Visualization files (6 charts)
5. **IoT_Cold_Storage_Internship_Report.docx** - Final report

## Evaluation Criteria Coverage

This project addresses all 9 evaluation criteria (PC1-PC9):

- **PC1**: Problem analysis with key parameters and target community
- **PC2**: Functional and non-functional requirements evaluation
- **PC3**: Complete solution design and feasibility assessment
- **PC4**: Implementation plan with milestones and resource allocation
- **PC5**: Justified technology stack selection
- **PC6**: Full working solution with 1500+ lines of Python code
- **PC7**: Comprehensive testing through 1000-cycle simulation
- **PC8**: Detailed performance evaluation with metrics
- **PC9**: Technical skills demonstrated throughout project

## Future Enhancements

1. **Machine Learning Integration**: Predictive maintenance using historical data
2. **GPS Tracking**: Real-time location tracking for transportation units
3. **Advanced Protocols**: NB-IoT and LoRaWAN support for wider coverage
4. **Blockchain Integration**: Immutable compliance records
5. **Mobile App**: Real-time monitoring via smartphone
6. **Cloud Integration**: AWS/Azure cloud platform connectivity
7. **Advanced Analytics**: Anomaly detection algorithms
8. **Multi-language Support**: Internationalization for global deployment

## Technical Skills Demonstrated

- Python programming (OOP, data structures, file I/O)
- IoT system design and architecture
- Sensor integration and data acquisition
- Real-time data processing and analysis
- Alert system design and implementation
- Data visualization and reporting
- Statistical analysis
- Document generation and formatting
- System testing and validation

## Support and Documentation

For detailed information about the system implementation, refer to the comprehensive internship report included in this package: **IoT_Cold_Storage_Internship_Report.docx**

The report contains:
- Detailed system architecture
- Implementation methodology
- Performance analysis
- Visual representations of results
- Evaluation against all criteria

## License

This project was developed as part of an internship program and is provided for educational and professional purposes.

## Contact

For questions or further information about this project, please refer to the internship report documentation.

---

**Project Completion Date**: July 2026
**Total Lines of Code**: 1500+
**Simulation Cycles**: 1000
**Data Points Generated**: 3000+
**Visualizations Created**: 6 professional charts
**Report Pages**: 30+
