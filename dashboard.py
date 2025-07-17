import subprocess
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

console = Console()
layout = Layout()

layout.split(
    Layout(name="header"),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="footer"),
)

layout["main"].split_row(Layout(name="left"), Layout(name="right"))
layout["left"].split_column(Layout(name="event_generator"), Layout(name="event_collector"))
layout["right"].split_column(Layout(name="data_processor"), Layout(name="data_storage"))

class ServiceLog:
    def __init__(self, title):
        self.title = title
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)
        if len(self.lines) > 10:
            self.lines.pop(0)

    def __rich__(self):
        return Panel("\n".join(self.lines), title=self.title)

# Create log containers
event_generator_log = ServiceLog("Event Generator")
event_collector_log = ServiceLog("Event Collector")
data_processor_log = ServiceLog("Data Processor")
data_storage_log = ServiceLog("Data Storage")

# Update layout with logs
layout["event_generator"].update(event_generator_log)
layout["event_collector"].update(event_collector_log)
layout["data_processor"].update(data_processor_log)
layout["data_storage"].update(data_storage_log)

procs = []
def start_services():
    # Start zookeeper and kafka
    procs.append(subprocess.Popen(["docker-compose", "up"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    time.sleep(15) # Wait for kafka to be ready

    # Start services
    procs.append(subprocess.Popen(["uvicorn", "event-collector.main:app", "--host", "0.0.0.0", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    procs.append(subprocess.Popen(["python", "-u", "data-processor/main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    procs.append(subprocess.Popen(["python", "-u", "data-storage/main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    procs.append(subprocess.Popen(["python", "-u", "event-generator/main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))

def stop_services():
    for p in procs:
        p.terminate()
    subprocess.run(["docker-compose", "down"])


with Live(layout, screen=True, redirect_stderr=False) as live:
    try:
        start_services()
        while True:
            for p in procs:
                if p.poll() is None:
                    line = p.stdout.readline().strip()
                    if line:
                        if "event-collector" in p.args[2]:
                            event_collector_log.add_line(line)
                        elif "data-processor" in p.args[2]:
                            data_processor_log.add_line(line)
                        elif "data-storage" in p.args[2]:
                            data_storage_log.add_line(line)
                        elif "event-generator" in p.args[2]:
                            event_generator_log.add_line(line)
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_services()
        console.print("Dashboard stopped.")
