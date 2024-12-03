import torch
import psutil
import time
import subprocess
import logging

class ResourceMonitorNode:
    def __init__(self):
        self.last_update = 0
        self.update_interval = 1.0
        self.logger = logging.getLogger("ComfyUI")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "monitor_resources"
    CATEGORY = "Isulion/Utils"
    OUTPUT_NODE = True

    def get_system_metrics(self):
        try:
            # CPU Usage - use interval=0.1 for more accurate reading
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.logger.info(f"CPU Usage: {cpu_percent}%")
            
            # RAM Usage
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            self.logger.info(f"RAM Usage: {ram_percent}%")

            # GPU Metrics
            gpu_util = 0.0
            vram_percent = 0.0
            
            if torch.cuda.is_available():
                try:
                    # Get GPU info using nvidia-smi
                    result = subprocess.check_output(
                        ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,nounits,noheader'],
                        encoding='utf-8'
                    )
                    gpu_util, vram_used, vram_total = map(float, result.strip().split(','))
                    vram_percent = (vram_used / vram_total) * 100.0 if vram_total > 0 else 0.0
                    
                    self.logger.info(f"GPU Usage: {gpu_util}%")
                    self.logger.info(f"VRAM Usage: {vram_percent}%")
                except Exception as e:
                    self.logger.warning(f"Error getting GPU metrics: {str(e)}")

            metrics = {
                "cpu": [float(cpu_percent)],
                "ram": [float(ram_percent)],
                "gpu": [float(gpu_util)],
                "vram": [float(vram_percent)]
            }
            
            self.logger.info(f"Collected metrics: {metrics}")
            return metrics

        except Exception as e:
            self.logger.error(f"Error collecting metrics: {str(e)}")
            return {
                "cpu": [0.0],
                "ram": [0.0],
                "gpu": [0.0],
                "vram": [0.0]
            }

    def monitor_resources(self, trigger):
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            metrics = self.get_system_metrics()
            return {"ui": metrics}
        return {"ui": {}}

NODE_CLASS_MAPPINGS = {
    "ResourceMonitor": ResourceMonitorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResourceMonitor": "Resource Monitor"
}
