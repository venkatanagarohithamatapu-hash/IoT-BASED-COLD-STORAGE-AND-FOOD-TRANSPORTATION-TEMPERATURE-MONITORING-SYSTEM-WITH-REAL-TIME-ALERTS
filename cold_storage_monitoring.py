"""
IoT-Based Cold Storage and Food Transportation Temperature Monitoring System
with Real-Time Alerts

This module simulates a comprehensive temperature monitoring system for cold storage
facilities and food transportation with alert generation and performance tracking.
"""

import random
import datetime
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import statistics
from enum import Enum


class AlertLevel(Enum):
    """Alert severity levels."""
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class TemperatureReading:
    """Represents a temperature reading from the monitoring system."""
    timestamp: str
    location: str
    temperature: float  # Celsius
    humidity: float     # Percentage (0-100)
    alert_level: str    # NORMAL, WARNING, CRITICAL
    alert_message: str
    equipment_status: str  # OPERATIONAL, MAINTENANCE, OFFLINE


class TemperatureSensor:
    """Simulates a temperature sensor with realistic readings."""
    
    def __init__(self, location: str, baseline_temp: float = -18.0):
        """
        Initialize the temperature sensor.
        
        Args:
            location: Location identifier (e.g., "Zone A", "Transport Unit 1")
            baseline_temp: Baseline temperature in Celsius (default: -18°C for freezer)
        """
        self.location = location
        self.baseline_temp = baseline_temp
        self.last_reading = None
    
    def read_temperature(self) -> float:
        """
        Read temperature with realistic fluctuations and occasional anomalies.
        
        Returns:
            Temperature in Celsius
        """
        # Simulate occasional temperature fluctuations
        anomaly_chance = random.random()
        
        if anomaly_chance < 0.05:  # 5% chance of anomaly
            # Simulate equipment malfunction or door opening
            fluctuation = random.uniform(-5, 8)
        elif anomaly_chance < 0.15:  # 10% chance of minor fluctuation
            fluctuation = random.uniform(-1, 2)
        else:  # 85% normal operation
            fluctuation = random.uniform(-0.5, 0.5)
        
        if self.last_reading is None:
            reading = self.baseline_temp + fluctuation
        else:
            reading = self.last_reading + fluctuation
            # Gradually return to baseline
            reading = reading * 0.9 + self.baseline_temp * 0.1
        
        self.last_reading = reading
        return round(reading, 2)


class HumiditySensor:
    """Simulates a humidity sensor."""
    
    def __init__(self):
        self.last_reading = None
    
    def read_humidity(self) -> float:
        """
        Read humidity with realistic variations.
        
        Returns:
            Humidity percentage (0-100)
        """
        if self.last_reading is None:
            reading = random.uniform(60, 90)
        else:
            reading = self.last_reading + random.uniform(-2, 2)
            reading = max(0, min(100, reading))
        
        self.last_reading = reading
        return round(reading, 2)


class AlertGenerator:
    """Generates alerts based on temperature readings."""
    
    def __init__(self, 
                 temp_warning_high: float = -15.0,
                 temp_critical_high: float = -10.0,
                 temp_critical_low: float = -25.0):
        """
        Initialize alert generator with thresholds.
        
        Args:
            temp_warning_high: Temperature for warning level
            temp_critical_high: Temperature for critical level (too warm)
            temp_critical_low: Temperature for critical level (too cold)
        """
        self.temp_warning_high = temp_warning_high
        self.temp_critical_high = temp_critical_high
        self.temp_critical_low = temp_critical_low
        self.alert_history = []
    
    def check_temperature(self, temperature: float) -> Tuple[AlertLevel, str]:
        """
        Check temperature and generate appropriate alert.
        
        Args:
            temperature: Current temperature reading
            
        Returns:
            Tuple of (AlertLevel, alert_message)
        """
        if temperature >= self.temp_critical_high:
            return AlertLevel.CRITICAL, f"CRITICAL: Temperature {temperature}°C exceeds maximum safe limit"
        elif temperature <= self.temp_critical_low:
            return AlertLevel.CRITICAL, f"CRITICAL: Temperature {temperature}°C is dangerously low"
        elif temperature >= self.temp_warning_high:
            return AlertLevel.WARNING, f"WARNING: Temperature {temperature}°C approaching unsafe levels"
        else:
            return AlertLevel.NORMAL, f"Temperature {temperature}°C is within safe operating range"
    
    def record_alert(self, alert_level: AlertLevel, message: str, location: str):
        """Record alert in history."""
        self.alert_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'location': location,
            'level': alert_level.value,
            'message': message
        })


class EquipmentMonitor:
    """Monitors equipment status and maintenance needs."""
    
    def __init__(self):
        self.equipment_status = {}
        self.maintenance_log = []
    
    def check_equipment_status(self) -> str:
        """
        Check equipment status.
        
        Returns:
            Equipment status string
        """
        # Simulate occasional maintenance needs (2% chance)
        if random.random() < 0.02:
            return "MAINTENANCE"
        elif random.random() < 0.01:
            return "OFFLINE"
        else:
            return "OPERATIONAL"


class ColdStorageMonitoringSystem:
    """Main system controller for cold storage temperature monitoring."""
    
    def __init__(self, 
                 num_zones: int = 3,
                 temp_warning_high: float = -15.0,
                 temp_critical_high: float = -10.0,
                 temp_critical_low: float = -25.0):
        """
        Initialize the cold storage monitoring system.
        
        Args:
            num_zones: Number of monitoring zones
            temp_warning_high: Warning threshold temperature
            temp_critical_high: Critical high threshold
            temp_critical_low: Critical low threshold
        """
        self.num_zones = num_zones
        self.zones = [f"Zone {chr(65+i)}" for i in range(num_zones)]
        
        # Initialize sensors for each zone
        self.temperature_sensors = {
            zone: TemperatureSensor(zone, baseline_temp=-18.0) 
            for zone in self.zones
        }
        self.humidity_sensors = {
            zone: HumiditySensor() 
            for zone in self.zones
        }
        
        # Initialize alert system
        self.alert_generator = AlertGenerator(
            temp_warning_high=temp_warning_high,
            temp_critical_high=temp_critical_high,
            temp_critical_low=temp_critical_low
        )
        
        # Initialize equipment monitor
        self.equipment_monitor = EquipmentMonitor()
        
        # Data logging
        self.readings: List[TemperatureReading] = []
        self.alert_count = 0
        self.critical_alert_count = 0
        self.warning_alert_count = 0
    
    def read_sensors(self, zone: str) -> Tuple[float, float]:
        """
        Read sensors for a specific zone.
        
        Returns:
            Tuple of (temperature, humidity)
        """
        temperature = self.temperature_sensors[zone].read_temperature()
        humidity = self.humidity_sensors[zone].read_humidity()
        return temperature, humidity
    
    def simulate_cycle(self) -> List[TemperatureReading]:
        """
        Simulate one complete monitoring cycle for all zones.
        
        Returns:
            List of TemperatureReading objects
        """
        cycle_readings = []
        
        for zone in self.zones:
            # Read sensors
            temperature, humidity = self.read_sensors(zone)
            
            # Check temperature and generate alerts
            alert_level, alert_message = self.alert_generator.check_temperature(temperature)
            
            # Check equipment status
            equipment_status = self.equipment_monitor.check_equipment_status()
            
            # Record alert if needed
            if alert_level != AlertLevel.NORMAL:
                self.alert_count += 1
                if alert_level == AlertLevel.CRITICAL:
                    self.critical_alert_count += 1
                else:
                    self.warning_alert_count += 1
                self.alert_generator.record_alert(alert_level, alert_message, zone)
            
            # Create reading record
            reading = TemperatureReading(
                timestamp=datetime.datetime.now().isoformat(),
                location=zone,
                temperature=temperature,
                humidity=humidity,
                alert_level=alert_level.value,
                alert_message=alert_message,
                equipment_status=equipment_status
            )
            
            cycle_readings.append(reading)
            self.readings.append(reading)
        
        return cycle_readings
    
    def run_simulation(self, num_cycles: int = 1000) -> List[TemperatureReading]:
        """
        Run the simulation for a specified number of cycles.
        
        Args:
            num_cycles: Number of monitoring cycles to simulate
            
        Returns:
            List of all temperature readings
        """
        for _ in range(num_cycles):
            self.simulate_cycle()
        
        return self.readings
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from collected readings.
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.readings:
            return {}
        
        # Group readings by zone
        zone_data = {}
        for zone in self.zones:
            zone_readings = [r for r in self.readings if r.location == zone]
            temps = [r.temperature for r in zone_readings]
            humidities = [r.humidity for r in zone_readings]
            
            zone_data[zone] = {
                'avg_temp': round(statistics.mean(temps), 2) if temps else 0,
                'min_temp': round(min(temps), 2) if temps else 0,
                'max_temp': round(max(temps), 2) if temps else 0,
                'std_temp': round(statistics.stdev(temps), 2) if len(temps) > 1 else 0,
                'avg_humidity': round(statistics.mean(humidities), 2) if humidities else 0,
                'readings_count': len(zone_readings)
            }
        
        # Overall statistics
        all_temps = [r.temperature for r in self.readings]
        all_humidities = [r.humidity for r in self.readings]
        alert_readings = [r for r in self.readings if r.alert_level != "NORMAL"]
        
        return {
            'total_readings': len(self.readings),
            'total_cycles': len(self.readings) // self.num_zones,
            'avg_temperature': round(statistics.mean(all_temps), 2),
            'min_temperature': round(min(all_temps), 2),
            'max_temperature': round(max(all_temps), 2),
            'std_temperature': round(statistics.stdev(all_temps), 2) if len(all_temps) > 1 else 0,
            'avg_humidity': round(statistics.mean(all_humidities), 2),
            'min_humidity': round(min(all_humidities), 2),
            'max_humidity': round(max(all_humidities), 2),
            'total_alerts': self.alert_count,
            'critical_alerts': self.critical_alert_count,
            'warning_alerts': self.warning_alert_count,
            'alert_percentage': round((len(alert_readings) / len(self.readings)) * 100, 2),
            'zone_statistics': zone_data
        }
    
    def export_to_csv(self, filename: str):
        """
        Export readings to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'location', 'temperature', 'humidity', 
                         'alert_level', 'alert_message', 'equipment_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for reading in self.readings:
                writer.writerow(asdict(reading))
    
    def export_to_json(self, filename: str):
        """
        Export readings to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        data = {
            'metadata': {
                'total_readings': len(self.readings),
                'total_cycles': len(self.readings) // self.num_zones,
                'num_zones': self.num_zones,
                'zones': self.zones
            },
            'statistics': self.get_statistics(),
            'alert_history': self.alert_generator.alert_history,
            'readings': [asdict(r) for r in self.readings]
        }
        
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
    
    def export_alerts_to_csv(self, filename: str):
        """Export alert history to CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'location', 'level', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for alert in self.alert_generator.alert_history:
                writer.writerow(alert)


class SystemPerformanceAnalyzer:
    """Analyzes system performance and reliability metrics."""
    
    @staticmethod
    def calculate_system_reliability(total_readings: int, alert_count: int) -> float:
        """
        Calculate system reliability score.
        
        Args:
            total_readings: Total number of readings
            alert_count: Number of alerts triggered
            
        Returns:
            Reliability score (0-100)
        """
        if total_readings == 0:
            return 100.0
        reliability = max(0, 100 - (alert_count / total_readings) * 100)
        return round(reliability, 2)
    
    @staticmethod
    def calculate_temperature_stability(temperatures: List[float]) -> float:
        """
        Calculate temperature stability score.
        
        Args:
            temperatures: List of temperature readings
            
        Returns:
            Stability score (0-100)
        """
        if len(temperatures) < 2:
            return 100.0
        
        std_dev = statistics.stdev(temperatures)
        # Normalize standard deviation to 0-100 scale
        stability = max(0, 100 - std_dev * 5)
        return round(stability, 2)
    
    @staticmethod
    def calculate_alert_response_efficiency(critical_count: int, warning_count: int) -> float:
        """
        Calculate alert response efficiency.
        
        Args:
            critical_count: Number of critical alerts
            warning_count: Number of warning alerts
            
        Returns:
            Efficiency score (0-100)
        """
        total_alerts = critical_count + warning_count
        if total_alerts == 0:
            return 100.0
        
        # Efficiency based on early warning (warnings caught before critical)
        efficiency = max(0, 100 - (critical_count / (total_alerts + 1)) * 50)
        return round(efficiency, 2)


def main():
    """Main function to run the simulation."""
    print("=" * 80)
    print("IoT-BASED COLD STORAGE AND FOOD TRANSPORTATION TEMPERATURE MONITORING SYSTEM")
    print("=" * 80)
    print()
    
    # Initialize system with 3 monitoring zones
    system = ColdStorageMonitoringSystem(
        num_zones=3,
        temp_warning_high=-15.0,
        temp_critical_high=-10.0,
        temp_critical_low=-25.0
    )
    
    print("Starting simulation with 1000 monitoring cycles...")
    print("(Each cycle monitors 3 zones: Zone A, Zone B, Zone C)")
    print()
    
    # Run simulation
    readings = system.run_simulation(num_cycles=1000)
    
    # Get statistics
    stats = system.get_statistics()
    
    # Export data
    system.export_to_csv('/home/ubuntu/cold_storage_report/temperature_readings.csv')
    system.export_to_json('/home/ubuntu/cold_storage_report/temperature_readings.json')
    system.export_alerts_to_csv('/home/ubuntu/cold_storage_report/alert_history.csv')
    
    # Display results
    print("SIMULATION RESULTS")
    print("-" * 80)
    print(f"Total Monitoring Cycles: {stats['total_cycles']}")
    print(f"Total Readings (3 zones × cycles): {stats['total_readings']}")
    print()
    
    print("ALERT STATISTICS")
    print("-" * 80)
    print(f"Total Alerts: {stats['total_alerts']}")
    print(f"Critical Alerts: {stats['critical_alerts']}")
    print(f"Warning Alerts: {stats['warning_alerts']}")
    print(f"Alert Percentage: {stats['alert_percentage']}%")
    print()
    
    print("TEMPERATURE STATISTICS (Overall)")
    print("-" * 80)
    print(f"Average Temperature: {stats['avg_temperature']}°C")
    print(f"Minimum Temperature: {stats['min_temperature']}°C")
    print(f"Maximum Temperature: {stats['max_temperature']}°C")
    print(f"Standard Deviation: {stats['std_temperature']}°C")
    print()
    
    print("HUMIDITY STATISTICS")
    print("-" * 80)
    print(f"Average Humidity: {stats['avg_humidity']}%")
    print(f"Minimum Humidity: {stats['min_humidity']}%")
    print(f"Maximum Humidity: {stats['max_humidity']}%")
    print()
    
    print("ZONE-SPECIFIC STATISTICS")
    print("-" * 80)
    for zone, zone_stats in stats['zone_statistics'].items():
        print(f"\n{zone}:")
        print(f"  Average Temperature: {zone_stats['avg_temp']}°C")
        print(f"  Temperature Range: {zone_stats['min_temp']}°C to {zone_stats['max_temp']}°C")
        print(f"  Temperature Std Dev: {zone_stats['std_temp']}°C")
        print(f"  Average Humidity: {zone_stats['avg_humidity']}%")
        print(f"  Readings: {zone_stats['readings_count']}")
    
    print()
    
    # Performance analysis
    analyzer = SystemPerformanceAnalyzer()
    all_temps = [r.temperature for r in readings]
    
    reliability = analyzer.calculate_system_reliability(stats['total_readings'], stats['total_alerts'])
    stability = analyzer.calculate_temperature_stability(all_temps)
    efficiency = analyzer.calculate_alert_response_efficiency(
        stats['critical_alerts'], 
        stats['warning_alerts']
    )
    
    print("SYSTEM PERFORMANCE METRICS")
    print("-" * 80)
    print(f"System Reliability Score: {reliability}/100")
    print(f"Temperature Stability Score: {stability}/100")
    print(f"Alert Response Efficiency: {efficiency}/100")
    print()
    
    print("Data exported to:")
    print("  - /home/ubuntu/cold_storage_report/temperature_readings.csv")
    print("  - /home/ubuntu/cold_storage_report/temperature_readings.json")
    print("  - /home/ubuntu/cold_storage_report/alert_history.csv")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
