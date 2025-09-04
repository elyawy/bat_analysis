import re
import datetime
from pathlib import Path
import csv

def extract_simulation_time(log_file_path):
    try:
        # Read the log file
        with open(log_file_path, 'r') as file:
            log_content = file.read()
        
        # Extract timestamp patterns for start and end of simulations
        start_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\[INFO\]\[main\.py\]\[main\]: '
        end_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\[INFO\]\[abc_inference\.py\]\[main\]: '
        
        # Find all matches
        start_times = re.findall(start_pattern, log_content)
        end_times = re.findall(end_pattern, log_content)
        
        if not start_times or not end_times:
            return None
        
        # Convert first start time and first end time to datetime objects
        start_time = datetime.datetime.strptime(start_times[0], '%Y-%m-%d %H:%M:%S,%f')
        end_time = datetime.datetime.strptime(end_times[0], '%Y-%m-%d %H:%M:%S,%f')
        
        # Calculate the time difference
        time_diff = end_time - start_time
        
        return {
            'start_time': start_times[0],
            'end_time': end_times[0],
            'duration_seconds': time_diff.total_seconds(),
            'duration_minutes': time_diff.total_seconds() / 60,
            'duration_hours': time_diff.total_seconds() / 3600
        }
    except Exception as e:
        print(f"Error processing {log_file_path}: {str(e)}")
        return None

def process_directory(directory_path, output_csv):
    # Get all log files in the directory
    log_files = list(directory_path.glob('**/*.log'))
    
    # Prepare CSV output
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File_Name', 'Start_Time', 'End_Time', 'Duration_Seconds', 'Duration_Minutes', 'Duration_Hours'])
        
        for log_file in log_files:
            file_name = log_file.parent.stem  # Remove .log suffix
            
            result = extract_simulation_time(log_file)
            
            if result:
                csv_writer.writerow([
                    file_name,
                    result['start_time'],
                    result['end_time'],
                    f"{result['duration_seconds']:.2f}",
                    f"{result['duration_minutes']:.2f}",
                    f"{result['duration_hours']:.2f}"
                ])
                print(f"Processed {log_file}")
            else:
                print(f"Could not extract simulation times from {log_file}")

def main():
    directory_path = Path('other_msas').resolve()  # Current directory, change this to your log files directory
    output_csv = 'times_others.csv'
    
    try:
        process_directory(directory_path, output_csv)
        print(f"Results written to {output_csv}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()