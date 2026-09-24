// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 FoodSafe-DX-OS Contributors

class TraceGraphViewer {
    constructor(canvasId, infoPanelId) {
        this.canvas = document.getElementById(canvasId);
        this.infoPanel = document.getElementById(infoPanelId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.links = [];
        this.selectedNode = null;
        this.hoveredNode = null;
        this.animFrame = null;
        this.pulsePhase = 0;

        this.initEvents();
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        if (!this.canvas) return;
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = 420;
        this.render();
    }

    setData(graphData) {
        if (!graphData || !graphData.nodes) return;
        this.nodes = JSON.parse(JSON.stringify(graphData.nodes));
        this.links = JSON.parse(JSON.stringify(graphData.links));

        // Tự động bố trí tọa độ nút (Layered Layout)
        this.layoutNodes();
        this.startAnimation();
        this.render();
    }

    layoutNodes() {
        const width = this.canvas.width;
        const height = this.canvas.height;
        const count = this.nodes.length;

        // Định vị các nút theo vai trò logic dịch tễ
        this.nodes.forEach((node, idx) => {
            node.radius = 28;
            if (node.type === 'SUPPLIER_ROOT') {
                node.x = width * 0.15;
                node.y = height * 0.5;
                node.color = '#ef4444';
                node.icon = '🏭';
            } else if (node.type === 'BATCH_CONTAMINATED') {
                node.x = width * 0.38;
                node.y = height * 0.5;
                node.color = '#f97316';
                node.icon = '📦';
            } else if (node.type === 'INCIDENT_HOTSPOT') {
                node.x = width * 0.65;
                node.y = height * 0.3;
                node.color = '#dc2626';
                node.icon = '🚨';
                node.radius = 34;
            } else if (node.type === 'FACILITY_OUTBREAK') {
                node.x = width * 0.88;
                node.y = height * 0.3;
                node.color = '#e11d48';
                node.icon = '🏥';
            } else if (node.type === 'FACILITY_IMMINENT_RISK') {
                node.x = width * 0.65;
                node.y = height * 0.75;
                node.color = '#eab308';
                node.icon = '🏫';
                node.radius = 32;
            } else {
                node.x = width * (0.2 + (idx * 0.15));
                node.y = height * (0.3 + (idx % 2) * 0.4);
                node.color = '#64748b';
                node.icon = '📌';
            }
        });
    }

    startAnimation() {
        if (this.animFrame) cancelAnimationFrame(this.animFrame);
        const animate = () => {
            this.pulsePhase = (this.pulsePhase + 0.05) % (Math.PI * 2);
            this.render();
            this.animFrame = requestAnimationFrame(animate);
        };
        this.animFrame = requestAnimationFrame(animate);
    }

    render() {
        if (!this.ctx || !this.canvas) return;
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // 1. Vẽ các đường liên kết (Links/Edges)
        this.links.forEach((link, i) => {
            const sourceNode = this.nodes.find(n => n.id === link.source);
            const targetNode = this.nodes.find(n => n.id === link.target);
            if (!sourceNode || !targetNode) return;

            ctx.save();
            ctx.beginPath();
            ctx.moveTo(sourceNode.x, sourceNode.y);
            ctx.lineTo(targetNode.x, targetNode.y);

            // Nét vẽ gradient cảnh báo
            const isAlertLink = targetNode.type === 'FACILITY_IMMINENT_RISK' || sourceNode.type === 'INCIDENT_HOTSPOT';
            ctx.strokeStyle = isAlertLink ? 'rgba(239, 68, 68, 0.7)' : 'rgba(100, 116, 139, 0.5)';
            ctx.lineWidth = isAlertLink ? 2.5 : 1.5;
            if (isAlertLink) {
                ctx.setLineDash([6, 4]);
            }
            ctx.stroke();
            ctx.restore();

            // Vẽ hạt xung nhịp dịch tễ di chuyển dọc theo đường lây nhiễm
            const t = (Math.sin(this.pulsePhase + i) + 1) / 2;
            const px = sourceNode.x + (targetNode.x - sourceNode.x) * t;
            const py = sourceNode.y + (targetNode.y - sourceNode.y) * t;
            ctx.beginPath();
            ctx.arc(px, py, 4, 0, Math.PI * 2);
            ctx.fillStyle = isAlertLink ? '#f87171' : '#38bdf8';
            ctx.fill();

            // Nhãn quan hệ giữa các nút
            const mx = (sourceNode.x + targetNode.x) / 2;
            const my = (sourceNode.y + targetNode.y) / 2 - 8;
            ctx.font = '10px sans-serif';
            ctx.fillStyle = '#94a3b8';
            ctx.textAlign = 'center';
            ctx.fillText(link.relationship, mx, my);
        });

        // 2. Vẽ các Nút (Nodes)
        this.nodes.forEach(node => {
            const isHotspot = node.type === 'INCIDENT_HOTSPOT' || node.type === 'FACILITY_IMMINENT_RISK';
            const pulse = isHotspot ? Math.sin(this.pulsePhase) * 6 : 0;

            // Vòng hào quang phát sáng cảnh báo
            if (isHotspot) {
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.radius + 8 + pulse, 0, Math.PI * 2);
                ctx.fillStyle = node.type === 'FACILITY_IMMINENT_RISK' ? 'rgba(234, 179, 8, 0.2)' : 'rgba(239, 68, 68, 0.25)';
                ctx.fill();
            }

            // Vòng tròn thân nút
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            ctx.fillStyle = node.color;
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = (node === this.selectedNode || node === this.hoveredNode) ? 3 : 1.5;
            ctx.stroke();

            // Vẽ Icon bên trong nút
            ctx.font = '18px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.icon || '📍', node.x, node.y);

            // Nhãn tiêu đề nút
            ctx.font = 'bold 11px sans-serif';
            ctx.fillStyle = '#f8fafc';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';

            // Rút ngắn nhãn hiển thị nếu quá dài
            let displayLabel = node.label;
            if (displayLabel.length > 25) {
                displayLabel = displayLabel.substring(0, 23) + '...';
            }
            ctx.fillText(displayLabel, node.x, node.y + node.radius + 6);
        });
    }

    initEvents() {
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            let hovered = null;
            for (const node of this.nodes) {
                const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
                if (dist <= node.radius + 5) {
                    hovered = node;
                    break;
                }
            }
            this.hoveredNode = hovered;
            this.canvas.style.cursor = hovered ? 'pointer' : 'default';
        });

        this.canvas.addEventListener('click', (e) => {
            if (this.hoveredNode) {
                this.selectedNode = this.hoveredNode;
                this.displayNodeInfo(this.selectedNode);
                this.render();
            }
        });
    }

    displayNodeInfo(node) {
        if (!this.infoPanel) return;
        let detailsHtml = '';
        if (node.details) {
            detailsHtml = Object.entries(node.details).map(([k, v]) => `
                <div class="flex justify-between py-1 border-b border-slate-700/50 text-xs">
                    <span class="text-slate-400 capitalize">${k.replace('_', ' ')}:</span>
                    <span class="font-medium text-slate-200 text-right">${Array.isArray(v) ? v.join(', ') : v}</span>
                </div>
            `).join('');
        }

        this.infoPanel.innerHTML = `
            <div class="p-4 rounded-xl border border-slate-700 bg-slate-900/90 shadow-xl">
                <div class="flex items-center space-x-2 mb-2">
                    <span class="text-xl">${node.icon || '📍'}</span>
                    <div>
                        <h4 class="text-sm font-bold text-white">${node.label}</h4>
                        <span class="text-[10px] px-2 py-0.5 rounded-full uppercase tracking-wider font-semibold ${
                            node.type === 'FACILITY_IMMINENT_RISK' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40' :
                            node.type === 'INCIDENT_HOTSPOT' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' :
                            'bg-slate-700 text-slate-300'
                        }">${node.type}</span>
                    </div>
                </div>
                <div class="mt-3 space-y-1">
                    ${detailsHtml}
                </div>
            </div>
        `;
    }
}

window.TraceGraphViewer = TraceGraphViewer;
