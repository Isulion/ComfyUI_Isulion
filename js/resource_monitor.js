import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Isulion.ResourceMonitor",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ResourceMonitor") {
            // Store metrics
            nodeType.prototype.metrics = {
                cpu: 0,
                ram: 0,
                gpu: 0,
                vram: 0
            };

            // Handle UI updates
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                const result = onExecuted?.apply(this, arguments);
                if (message?.ui) {
                    // Extract first value from each metric list
                    const newMetrics = {};
                    for (const [key, values] of Object.entries(message.ui)) {
                        if (Array.isArray(values) && values.length > 0) {
                            newMetrics[key] = values[0];
                        }
                    }
                    this.metrics = { ...this.metrics, ...newMetrics };
                    this.setDirtyCanvas(true);
                }
                return result;
            };

            const onDrawBackground = nodeType.prototype.onDrawBackground;
            nodeType.prototype.onDrawBackground = function (ctx) {
                if (onDrawBackground) {
                    onDrawBackground.apply(this, arguments);
                }

                // Set up drawing context
                const margin = 10;
                const barHeight = 10;
                const barSpacing = 20;
                const width = this.size[0] - margin * 2;
                let y = 40;

                // Draw each resource bar
                const resources = [
                    { label: "CPU", value: this.metrics.cpu },
                    { label: "RAM", value: this.metrics.ram },
                    { label: "GPU", value: this.metrics.gpu },
                    { label: "VRAM", value: this.metrics.vram }
                ];

                resources.forEach(resource => {
                    this.drawResourceBar(ctx, resource.label, resource.value, margin, y, width, barHeight);
                    y += barSpacing;
                });

                // Set minimum node height
                this.size[1] = Math.max(120, y + barSpacing);
            };

            // Helper function to draw a single resource bar
            nodeType.prototype.drawResourceBar = function (ctx, label, value, x, y, width, height) {
                const barWidth = width - 50;

                // Draw label
                ctx.fillStyle = "#CCC";
                ctx.font = "10px Arial";
                ctx.textAlign = "left";
                ctx.fillText(label, x, y + height - 2);

                // Draw background
                ctx.fillStyle = "#333";
                ctx.fillRect(x + 35, y, barWidth, height);

                // Draw progress
                const progress = Math.min((value / 100) * barWidth, barWidth);
                const gradient = ctx.createLinearGradient(x + 35, y, x + 35 + barWidth, y);

                if (value < 70) {
                    gradient.addColorStop(0, "#00FF00");
                    gradient.addColorStop(1, "#00AA00");
                } else if (value < 90) {
                    gradient.addColorStop(0, "#FFFF00");
                    gradient.addColorStop(1, "#FFA500");
                } else {
                    gradient.addColorStop(0, "#FF0000");
                    gradient.addColorStop(1, "#8B0000");
                }

                ctx.fillStyle = gradient;
                ctx.fillRect(x + 35, y, progress, height);

                // Draw percentage
                ctx.fillStyle = "#CCC";
                ctx.textAlign = "right";
                ctx.fillText(value.toFixed(1) + "%", x + width, y + height - 2);
            };
        }
    }
});
