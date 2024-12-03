import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Isulion.ResourceMonitor",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ResourceMonitor") {
            // Store original methods
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Override node creation
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Create monitor container
                const container = document.createElement("div");
                container.className = "resource-monitor-widget";
                container.style.padding = "10px";
                container.style.width = "300px";
                container.style.backgroundColor = "#1a1a1a";
                container.style.borderRadius = "5px";
                container.style.margin = "10px";
                
                // Add it to the node
                this.widgets_up?.appendChild(container);
                this.monitorContainer = container;
                
                // Initialize empty metrics
                this.updateMetrics({
                    cpu: 0,
                    ram: 0,
                    gpu: 0,
                    vram: 0
                });
                
                return result;
            };

            // Add method to update metrics
            nodeType.prototype.updateMetrics = function(metrics) {
                if (!this.monitorContainer) return;

                // Update the display
                this.monitorContainer.innerHTML = `
                    <style>
                        .resource-bar {
                            margin: 8px 0;
                            background: #2a2a2a;
                            border-radius: 4px;
                            overflow: hidden;
                        }
                        .resource-label {
                            display: flex;
                            justify-content: space-between;
                            margin-bottom: 2px;
                            color: #ddd;
                            font-size: 12px;
                        }
                        .progress {
                            height: 12px;
                            background: linear-gradient(90deg, var(--color-start) 0%, var(--color-end) 100%);
                            width: var(--progress);
                            transition: width 0.3s ease-in-out;
                            position: relative;
                        }
                        .progress::after {
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            background: linear-gradient(
                                45deg,
                                rgba(255,255,255,0.1) 25%,
                                transparent 25%,
                                transparent 50%,
                                rgba(255,255,255,0.1) 50%,
                                rgba(255,255,255,0.1) 75%,
                                transparent 75%,
                                transparent
                            );
                            background-size: 20px 20px;
                            animation: move 1s linear infinite;
                        }
                        @keyframes move {
                            0% { background-position: 0 0; }
                            100% { background-position: 20px 0; }
                        }
                    </style>
                    <div style="font-weight: bold; margin-bottom: 8px; color: #fff; text-align: center;">
                        System Monitor
                    </div>
                    ${this.createResourceBar('CPU', metrics.cpu)}
                    ${this.createResourceBar('RAM', metrics.ram)}
                    ${this.createResourceBar('GPU', metrics.gpu)}
                    ${this.createResourceBar('VRAM', metrics.vram)}
                `;
            };

            // Helper to create resource bars
            nodeType.prototype.createResourceBar = function(label, value) {
                const getColorGradient = (value) => {
                    if (value < 70) return { start: '#00ff00', end: '#99ff00' };
                    if (value < 90) return { start: '#ffff00', end: '#ffaa00' };
                    return { start: '#ff0000', end: '#ff0000' };
                };

                const colors = getColorGradient(value);
                
                return `
                    <div class="resource-bar">
                        <div class="resource-label">
                            <span>${label}</span>
                            <span>${value.toFixed(1)}%</span>
                        </div>
                        <div class="progress" style="
                            --progress: ${value}%;
                            --color-start: ${colors.start};
                            --color-end: ${colors.end};
                        "></div>
                    </div>
                `;
            };

            // Override the onExecuted to update metrics
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                const result = onExecuted ? onExecuted.apply(this, arguments) : undefined;

                if (message && message.status_report) {
                    // Extract metrics from status_report using regex
                    const metrics = {
                        cpu: parseFloat(message.cpu_usage) || 0,
                        ram: parseFloat(message.ram_usage) || 0,
                        gpu: parseFloat(message.gpu_util) || 0,
                        vram: parseFloat(message.vram_usage) || 0
                    };
                    
                    this.updateMetrics(metrics);
                }

                return result;
            };
        }
    }
});
