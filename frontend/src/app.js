// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 FoodSafe-DX-OS Contributors

const STATE = {
    facilities: [],
    suppliers: [],
    batches: [],
    lockers: [],
    incidents: [],
    stats: {},
    currentFacilityId: null,
    graphViewer: null,
};

// ==========================================
// API HELPER
// ==========================================
const API = {
    async get(endpoint) {
        const res = await fetch(`/api/v1${endpoint}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return await res.json();
    },

    async post(endpoint, payload) {
        const res = await fetch(`/api/v1${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        return { status: res.status, ok: res.ok, data };
    }
};

// ==========================================
// APP INITIALIZATION
// ==========================================
window.addEventListener('DOMContentLoaded', async () => {
    initTabs();
    await checkSystemHealth();
    await loadInitialData();
    initGraph();
    loadSampleLockers();
    loadStandardsCatalog();
    loadPathogensCatalog();
});

function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;
            tabButtons.forEach(b => {
                b.classList.remove('border-emerald-400', 'text-emerald-400', 'bg-emerald-500/10');
                b.classList.add('border-transparent', 'text-slate-400', 'hover:text-slate-200');
            });
            btn.classList.add('border-emerald-400', 'text-emerald-400', 'bg-emerald-500/10');
            btn.classList.remove('border-transparent', 'text-slate-400');

            tabContents.forEach(content => {
                content.classList.toggle('hidden', content.id !== target);
            });

            if (target === 'tab-trace' && STATE.graphViewer) {
                setTimeout(() => STATE.graphViewer.resize(), 100);
            }
        });
    });
}

function initGraph() {
    STATE.graphViewer = new TraceGraphViewer('traceCanvas', 'graphNodeDetails');
}

// ==========================================
// SYSTEM HEALTH & INITIAL DATA
// ==========================================
async function checkSystemHealth() {
    const statusDot = document.getElementById('backend-status-dot');
    const statusText = document.getElementById('backend-status-text');

    try {
        const res = await fetch('/api/health');
        const data = await res.json();
        if (data.status === 'healthy') {
            statusDot.className = 'w-2.5 h-2.5 rounded-full bg-emerald-400';
            statusText.innerText = 'Hệ thống Online (Docker & DB Sẵn sàng)';
        }
    } catch (e) {
        statusDot.className = 'w-2.5 h-2.5 rounded-full bg-rose-500';
        statusText.innerText = 'Mất kết nối Backend';
    }
}

async function loadInitialData() {
    try {
        const [facilities, suppliers, batches, incidents, statsRes] = await Promise.all([
            API.get('/facilities'),
            API.get('/suppliers'),
            API.get('/batches'),
            API.get('/incidents'),
            fetch('/db/stats').then(r => r.json())
        ]);

        STATE.facilities = facilities;
        STATE.suppliers = suppliers;
        STATE.batches = batches;
        STATE.incidents = incidents;
        STATE.stats = statsRes;

        renderFacilitySelector();
        populateStep1Selects();
        populateStep2Selects();
        renderBIStats();
    } catch (err) {
        console.error('Lỗi nạp dữ liệu ban đầu:', err);
    }
}

function renderFacilitySelector() {
    const select = document.getElementById('facilitySelector');
    if (!select) return;

    select.innerHTML = STATE.facilities.map(f => `
        <option value="${f.id}">🏫 ${f.name} (${f.daily_meal_capacity} suất/ngày)</option>
    `).join('');

    if (STATE.facilities.length > 0) {
        STATE.currentFacilityId = STATE.facilities[0].id;
        updateCurrentFacilityUI();
    }

    select.addEventListener('change', (e) => {
        STATE.currentFacilityId = parseInt(e.target.value);
        updateCurrentFacilityUI();
        loadSampleLockers();
    });
}

function updateCurrentFacilityUI() {
    const fac = STATE.facilities.find(f => f.id === STATE.currentFacilityId);
    if (!fac) return;
    const badge = document.getElementById('currentFacilityBadge');
    if (badge) badge.innerText = `${fac.name} • Quản lý: ${fac.manager_name} (${fac.phone || 'N/A'})`;
}

// ==========================================
// TAB 1: KIỂM THỰC 3 BƯỚC & POKA-YOKE
// ==========================================
function populateStep1Selects() {
    const batchSelect = document.getElementById('step1-batch');
    if (!batchSelect) return;
    batchSelect.innerHTML = STATE.batches.map(b => `
        <option value="${b.id}">${b.batch_code} - ${b.name} (${b.category} - Hạn: ${new Date(b.expiry_date).toLocaleDateString('vi-VN')})</option>
    `).join('');
}

function populateStep2Selects() {
    const batchSelect = document.getElementById('step2-batches');
    if (!batchSelect) return;
    batchSelect.innerHTML = STATE.batches.map(b => `
        <option value="${b.id}" ${b.status === 'REJECTED' ? 'class="text-rose-400 font-bold"' : ''}>
            ${b.batch_code} - ${b.name} [Trạng thái: ${b.status}]
        </option>
    `).join('');
}

// Kiểm thực Bước 1
async function handleStep1Submit(e) {
    if (e) e.preventDefault();
    const batchId = parseInt(document.getElementById('step1-batch').value);
    const temp = parseFloat(document.getElementById('step1-temp').value);
    const packagingIntact = document.getElementById('step1-packaging').checked;
    const sensoryStatus = document.getElementById('step1-sensory').value;
    const notes = document.getElementById('step1-notes').value;

    const payload = {
        batch_id: batchId,
        facility_id: STATE.currentFacilityId,
        inspector_name: "Cán bộ Y tế Bếp ăn",
        delivery_temp: temp,
        packaging_intact: packagingIntact,
        sensory_status: sensoryStatus,
        notes: notes || "Kiểm tra thực tế tại cổng giao nhận"
    };

    const res = await API.post('/inspections/step1', payload);
    const alertBox = document.getElementById('step1-result-alert');

    if (res.status === 422) {
        // POKA-YOKE KÍCH HOẠT CHẶN ĐỨNG
        const v = res.data.violation || res.data.detail || res.data;
        showPokaYokeModal(v);
        alertBox.className = "mt-4 p-4 rounded-xl border border-rose-500/50 bg-rose-950/40 text-rose-300 text-xs";
        alertBox.innerHTML = `
            <div class="flex items-center space-x-2 font-bold text-sm text-rose-400 mb-1">
                <i class="fa-solid fa-hand text-lg"></i>
                <span>POKA-YOKE ĐÃ TỰ ĐỘNG CHẶN NHẬP KHO!</span>
            </div>
            <p><strong>Lỗi:</strong> ${v.message || res.data.message || 'Vi phạm an toàn chuỗi lạnh'}</p>
            <p><strong>Căn cứ:</strong> ${v.standard_ref || 'QCVN Bộ Y tế'}</p>
            <p><strong>Hành động:</strong> ${v.action_required || 'Từ chối lô hàng'}</p>
        `;
        alertBox.classList.remove('hidden');
    } else if (res.ok) {
        alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/50 bg-emerald-950/40 text-emerald-300 text-xs";
        alertBox.innerHTML = `
            <div class="flex items-center space-x-2 font-bold text-sm text-emerald-400 mb-1">
                <i class="fa-solid fa-circle-check text-lg"></i>
                <span>ĐẠT CHUẨN! ĐÃ DUYỆT NHẬP KHO THỰC PHẨM</span>
            </div>
            <p>Phiếu kiểm thực số #${res.data.id} đã lưu trữ thành công. Lô hàng đủ điều kiện chuyển sang Bước 2 (Sơ chế).</p>
        `;
        alertBox.classList.remove('hidden');
    }
    await loadInitialData();
}

// Preset Buttons Test Bước 1
function presetStep1Violation() {
    document.getElementById('step1-temp').value = '13.5';
    document.getElementById('step1-packaging').checked = false;
    document.getElementById('step1-sensory').value = 'OFF_SMELL';
    document.getElementById('step1-notes').value = 'Cố tình test vi phạm nhiệt độ chuỗi lạnh 13.5°C để thử nghiệm rào chắn Poka-yoke';
    handleStep1Submit();
}

function presetStep1Pass() {
    document.getElementById('step1-temp').value = '2.2';
    document.getElementById('step1-packaging').checked = true;
    document.getElementById('step1-sensory').value = 'FRESH';
    document.getElementById('step1-notes').value = 'Thực phẩm tươi mới, nhiệt độ bảo quản lạnh 2.2°C đạt chuẩn QCVN';
    handleStep1Submit();
}

// Kiểm thực Bước 2
async function handleStep2Submit(e) {
    if (e) e.preventDefault();
    const mealName = document.getElementById('step2-meal-name').value;
    const batchSelect = document.getElementById('step2-batches');
    const selectedBatchIds = Array.from(batchSelect.selectedOptions).map(opt => parseInt(opt.value));
    const cookingMethod = document.getElementById('step2-method').value;
    const coreTemp = parseFloat(document.getElementById('step2-core-temp').value);
    const sensoryCheck = document.getElementById('step2-sensory').value;

    const payload = {
        facility_id: STATE.currentFacilityId,
        meal_name: mealName,
        batch_ids: selectedBatchIds,
        cooking_method: cookingMethod,
        core_temp: coreTemp,
        sensory_check: sensoryCheck,
        cook_name: "Bếp trưởng Phụ trách"
    };

    const res = await API.post('/inspections/step2', payload);
    const alertBox = document.getElementById('step2-result-alert');

    if (res.status === 422) {
        const v = res.data.violation || res.data.detail || res.data;
        showPokaYokeModal(v);
        alertBox.className = "mt-4 p-4 rounded-xl border border-rose-500/50 bg-rose-950/40 text-rose-300 text-xs";
        alertBox.innerHTML = `
            <div class="flex items-center space-x-2 font-bold text-sm text-rose-400 mb-1">
                <i class="fa-solid fa-ban text-lg"></i>
                <span>POKA-YOKE CHẶN XUẤT PHẦN ĂN: VI PHẠM AN TOÀN CHẾ BIẾN!</span>
            </div>
            <p><strong>Lỗi:</strong> ${v.message || res.data.message || 'Vi phạm nhiệt độ nấu chín'}</p>
            <p><strong>Căn cứ:</strong> ${v.standard_ref || 'QCVN 8-2:2011/BYT'}</p>
            <p><strong>Hành động:</strong> ${v.action_required || 'Hủy bỏ'}</p>
        `;
        alertBox.classList.remove('hidden');
    } else if (res.ok) {
        alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/50 bg-emerald-950/40 text-emerald-300 text-xs";
        alertBox.innerHTML = `
            <div class="flex items-center space-x-2 font-bold text-sm text-emerald-400 mb-1">
                <i class="fa-solid fa-circle-check text-lg"></i>
                <span>ĐẠT CHUẨN NẤU CHÍN HOÀN TOÀN! (Nhiệt độ tâm ${res.data.core_temp}°C >= 75.0°C)</span>
            </div>
            <p>Món ăn '${res.data.meal_name}' đã được phê duyệt. Vui lòng tiến hành Lưu mẫu thức ăn 24H tại Bước 3.</p>
        `;
        alertBox.classList.remove('hidden');
    }
}

function presetStep2Undercooked() {
    document.getElementById('step2-meal-name').value = 'Gà kho gừng chưa chín thấu (Test)';
    document.getElementById('step2-core-temp').value = '61.5';
    document.getElementById('step2-sensory').value = 'UNDERCOOKED_RAW_INSIDE';
    handleStep2Submit();
}

function presetStep2Pass() {
    document.getElementById('step2-meal-name').value = 'Gà hấp lá chanh đạt chuẩn chín sâu';
    document.getElementById('step2-core-temp').value = '86.0';
    document.getElementById('step2-sensory').value = 'COOKED_THOROUGHLY';
    handleStep2Submit();
}

// Kiểm thực Bước 3 (Tủ lưu mẫu 24h)
async function loadSampleLockers() {
    const container = document.getElementById('lockersGrid');
    if (!container) return;

    try {
        const lockers = await API.get(`/sample-lockers?facility_id=${STATE.currentFacilityId || ''}`);
        STATE.lockers = lockers;

        if (lockers.length === 0) {
            container.innerHTML = `<p class="col-span-full text-center text-slate-500 text-xs py-8">Chưa có mẫu thức ăn nào đang lưu tại cơ sở này.</p>`;
            return;
        }

        container.innerHTML = lockers.map(loc => {
            const isLocked = loc.is_locked;
            const hoursLeft = loc.hours_remaining;
            return `
                <div class="p-4 rounded-xl border ${isLocked ? 'border-amber-500/30 bg-amber-950/20' : 'border-slate-700 bg-slate-800/60'} shadow-lg relative">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-mono font-bold text-slate-300">#${loc.locker_number}</span>
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            loc.status === 'LOCKED_24H' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                            loc.status === 'ACCIDENT_INSPECTED' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                            'bg-emerald-500/20 text-emerald-400'
                        }">
                            ${loc.status}
                        </span>
                    </div>
                    <h4 class="text-sm font-bold text-white mb-1 truncate">${loc.meal_name}</h4>
                    <p class="text-xs text-slate-400 mb-2">Mã mẫu: <span class="font-mono text-slate-300">${loc.sample_code}</span></p>

                    <div class="flex items-center justify-between text-xs py-1.5 px-2.5 rounded-lg bg-slate-900/80 border border-slate-800 mb-3">
                        <span class="text-slate-400"><i class="fa-solid fa-temperature-arrow-down mr-1"></i> Nhiệt độ tủ:</span>
                        <span class="font-bold text-emerald-400">${loc.storage_temp}°C</span>
                    </div>

                    <div class="flex items-center justify-between text-xs py-1.5 px-2.5 rounded-lg bg-slate-900/80 border border-slate-800 mb-4">
                        <span class="text-slate-400"><i class="fa-solid fa-clock mr-1"></i> Đếm ngược:</span>
                        <span class="font-bold font-mono ${hoursLeft > 0 ? 'text-amber-400' : 'text-emerald-400'}">
                            ${hoursLeft > 0 ? `${hoursLeft} giờ còn lại` : 'Đủ 24h (Hợp lệ)'}
                        </span>
                    </div>

                    ${isLocked ? `
                        <button onclick="openUnlockModal(${loc.id}, '${loc.locker_number}', ${hoursLeft})" class="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold flex items-center justify-center space-x-1.5 transition">
                            <i class="fa-solid fa-lock text-amber-400"></i>
                            <span>Thao Tác Mở Khóa Tủ</span>
                        </button>
                    ` : `
                        <div class="w-full py-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold text-center">
                            <i class="fa-solid fa-lock-open mr-1"></i> Đã Mở Niêm Phong
                        </div>
                    `}
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('Lỗi tải tủ lưu mẫu:', e);
    }
}

// Modal Mở Khóa Tủ Mẫu (Poka-yoke & HITL)
let activeUnlockLockerId = null;

function openUnlockModal(lockerId, lockerNumber, hoursLeft) {
    activeUnlockLockerId = lockerId;
    document.getElementById('unlock-modal-title').innerText = `Mở Khóa Tủ Mẫu: ${lockerNumber}`;
    document.getElementById('unlock-modal-hours').innerText = hoursLeft > 0 ? `${hoursLeft} giờ nữa mới đủ điều kiện quy chuẩn 24H!` : 'Đã đủ 24H theo quy định.';
    document.getElementById('unlockModal').classList.remove('hidden');
}

function closeUnlockModal() {
    document.getElementById('unlockModal').classList.add('hidden');
    activeUnlockLockerId = null;
}

async function executeLockerUnlock() {
    if (!activeUnlockLockerId) return;
    const isOverride = document.getElementById('unlock-override-toggle').checked;
    const reason = document.getElementById('unlock-reason').value;
    const passcode = document.getElementById('unlock-passcode').value;

    const payload = {
        operator_name: "Cán bộ Y tế Bếp ăn",
        is_emergency_override: isOverride,
        override_reason: reason || null,
        override_passcode: passcode || null
    };

    const res = await API.post(`/sample-lockers/${activeUnlockLockerId}/unlock`, payload);

    if (res.status === 422) {
        const v = res.data.violation || res.data.detail || res.data;
        showPokaYokeModal(v);
    } else if (res.ok) {
        showToast("Mở niêm phong tủ mẫu thành công: " + (res.data.message || 'Đã mở chốt'), "success");
        closeUnlockModal();
        await loadSampleLockers();
    }
}

// ==========================================
// TAB 2: RAPID GRAPH RECALL DƯỚI 3 GIÂY
// ==========================================
async function triggerRapidTraceDemo() {
    const traceBtn = document.getElementById('btnTriggerTrace');
    const timerBadge = document.getElementById('traceExecutionTimer');
    const resultsPanel = document.getElementById('traceResultsPanel');

    traceBtn.disabled = true;
    traceBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> Đang kích hoạt thuật toán BFS...`;

    try {
        // Gọi API truy vết sự cố ID 4 (hoặc sự cố đầu tiên)
        const incidentId = STATE.incidents.length > 0 ? STATE.incidents[0].id : 4;
        const res = await API.post(`/incidents/${incidentId}/trace`, {});

        if (res.ok) {
            const data = res.data;
            // Hiển thị thời gian thực thi (ms)
            timerBadge.innerText = `Thời gian thực thi: ${data.execution_time_ms} ms (Dưới 3 giây)`;
            timerBadge.className = "px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";

            // Cập nhật thông tin mầm bệnh
            document.getElementById('pathogenName').innerText = data.pathogen_analysis.likely_pathogen;
            document.getElementById('pathogenIncubation').innerText = data.pathogen_analysis.incubation_period;
            document.getElementById('pathogenStandard').innerText = data.pathogen_analysis.standard_reference;
            document.getElementById('pathogenResponse').innerText = data.pathogen_analysis.recommended_medical_response;

            // Cập nhật nguyên nhân gốc rễ
            document.getElementById('rootBatchCode').innerText = data.root_cause_analysis.batch_code;
            document.getElementById('rootSupplierName').innerText = data.root_cause_analysis.supplier_name;
            document.getElementById('rootSupplierTax').innerText = data.root_cause_analysis.supplier_tax_code;

            // Cập nhật cảnh báo cơ sở nguy cơ cao
            const alertContainer = document.getElementById('imminentRiskContainer');
            if (data.imminent_risk_facilities && data.imminent_risk_facilities.length > 0) {
                alertContainer.innerHTML = data.imminent_risk_facilities.map(fac => `
                    <div class="p-4 rounded-xl border border-amber-500/50 bg-amber-950/40 text-amber-200 text-xs mb-2 danger-glow">
                        <div class="flex items-center justify-between mb-1">
                            <span class="font-bold text-sm text-amber-400"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> CẢNH BÁO NGUY CƠ LÂY NHIỄM: ${fac.facility_name}</span>
                            <span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">Khẩn Cấp</span>
                        </div>
                        <p class="text-slate-300 mb-1"><strong>Địa chỉ:</strong> ${fac.facility_address} | <strong>Điện thoại:</strong> ${fac.manager_phone}</p>
                        <p class="text-rose-400 font-bold mb-1"><strong>Chỉ thị:</strong> ${fac.emergency_action}</p>
                        <p class="text-slate-300"><strong>Tủ mẫu cần niêm phong:</strong> ${fac.locker_to_seal.join(', ')}</p>
                    </div>
                `).join('');
            } else {
                alertContainer.innerHTML = `<p class="text-xs text-slate-400">Không phát hiện cơ sở nào khác dùng chung lô nguyên liệu này.</p>`;
            }

            // Cập nhật Lệnh thu hồi khẩn cấp
            document.getElementById('emergencyDirectiveText').innerText = data.emergency_directive;

            // Render Đồ thị mạng lưới
            if (STATE.graphViewer && data.graph) {
                STATE.graphViewer.setData(data.graph);
            }

            const emptyState = document.getElementById('traceEmptyState');
            if (emptyState) emptyState.classList.add('hidden');
            resultsPanel.classList.remove('hidden');
            showToast(`Truy vết BFS hoàn tất trong ${data.execution_time_ms} ms! Phát hiện mầm bệnh ${data.pathogen_analysis.likely_pathogen}.`, "success");
        } else {
            showToast('Lỗi truy vết: ' + (res.data?.detail || res.data?.message || JSON.stringify(res.data)), "error");
        }
    } catch (e) {
        console.error('Lỗi truy vết:', e);
        showToast('Lỗi hệ thống khi truy vết: ' + e.message, "error");
    } finally {
        traceBtn.disabled = false;
        traceBtn.innerHTML = `<i class="fa-solid fa-bolt text-amber-400 mr-2"></i> Kích Hoạt Truy Vết Thần Tốc (Live Demo)`;
    }
}

// ==========================================
// TAB 3: TRỢ LÝ QUY CHUẨN VI SINH RAG (OFFLINE)
// ==========================================
async function submitRAGQuery(queryText) {
    const input = document.getElementById('ragQueryInput');
    const query = queryText || input.value.trim();
    if (!query) return;

    if (queryText) input.value = queryText;

    const answerBox = document.getElementById('ragAnswerBox');
    const timerBadge = document.getElementById('ragTimerBadge');
    answerBox.innerHTML = `<div class="p-6 text-center text-slate-400 text-xs"><i class="fa-solid fa-spinner fa-spin mr-2 text-emerald-400"></i> Đang đối soát tri thức QCVN 8-2 và văn bản pháp luật...</div>`;

    try {
        const res = await API.post('/rag/query', { query, top_k: 2 });
        if (res.ok) {
            const data = res.data;
            timerBadge.innerText = `${data.execution_time_ms} ms (100% Offline Local)`;
            
            // Format answer with simple markdown to HTML
            let formattedHtml = data.answer
                .replace(/^## (.*$)/gim, '<h2 class="text-base font-bold text-white mt-3 mb-2">$1</h2>')
                .replace(/^### (.*$)/gim, '<h3 class="text-sm font-bold text-emerald-400 mt-2 mb-1">$1</h3>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong class="text-slate-100">$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em class="text-slate-300">$1</em>')
                .replace(/\n/gim, '<br>');

            answerBox.innerHTML = `
                <div class="p-5 rounded-xl border border-slate-700 bg-slate-900/90 text-xs leading-relaxed">
                    ${formattedHtml}
                    <div class="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
                        <span><i class="fa-solid fa-shield-halved text-emerald-400 mr-1"></i> Chế độ: <strong>${data.engine_mode}</strong></span>
                        <span>Độ tin cậy: <strong>${(data.confidence_score * 100).toFixed(0)}%</strong></span>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        answerBox.innerHTML = `<div class="p-4 rounded-xl border border-rose-500/50 bg-rose-950/30 text-rose-300 text-xs">Lỗi tra cứu: ${e.message}</div>`;
    }
}

async function loadStandardsCatalog() {
    const list = document.getElementById('standardsList');
    if (!list) return;
    try {
        const res = await API.get('/rag/standards');
        list.innerHTML = res.standards.map(s => `
            <div class="p-3 rounded-lg border border-slate-800 bg-slate-900/60 hover:border-slate-700 transition">
                <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-emerald-400">${s.standard_code}</span>
                    <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 uppercase">${s.category}</span>
                </div>
                <h5 class="text-xs font-medium text-slate-200">${s.title}</h5>
            </div>
        `).join('');
    } catch (e) {
        console.error('Lỗi tải danh mục chuẩn:', e);
    }
}

async function loadPathogensCatalog() {
    const container = document.getElementById('pathogensTableBody');
    if (!container) return;
    try {
        const pathogens = await API.get('/rag/pathogens');
        container.innerHTML = pathogens.map(p => `
            <tr class="border-b border-slate-800 text-xs hover:bg-slate-800/40">
                <td class="py-2.5 px-3 font-bold text-white">${p.pathogen}</td>
                <td class="py-2.5 px-3 font-mono text-rose-400">${p.limit_allowed}</td>
                <td class="py-2.5 px-3 text-slate-300">${p.safe_core_temp}</td>
                <td class="py-2.5 px-3 text-slate-400">${p.incubation}</td>
                <td class="py-2.5 px-3 text-emerald-400 font-mono">${p.legal_basis}</td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Lỗi tải bảng vi sinh:', e);
    }
}

// ==========================================
// TAB 4: BI & EXECUTIVE DASHBOARD
// ==========================================
function renderBIStats() {
    const s = STATE.stats;
    if (!s) return;

    if (document.getElementById('bi-facilities-count')) document.getElementById('bi-facilities-count').innerText = s.facilities || 4;
    if (document.getElementById('bi-suppliers-count')) document.getElementById('bi-suppliers-count').innerText = s.suppliers || 5;
    if (document.getElementById('bi-batches-count')) document.getElementById('bi-batches-count').innerText = s.batches || 5;
    if (document.getElementById('bi-step1-count')) document.getElementById('bi-step1-count').innerText = s.inspections_step1 || 4;
    if (document.getElementById('bi-step2-count')) document.getElementById('bi-step2-count').innerText = s.inspections_step2 || 1;
    if (document.getElementById('bi-lockers-count')) document.getElementById('bi-lockers-count').innerText = s.sample_lockers || 3;
    if (document.getElementById('bi-incidents-count')) document.getElementById('bi-incidents-count').innerText = s.incidents || 1;
}

// ==========================================
// POKA-YOKE GLOBAL MODAL
// ==========================================
function showPokaYokeModal(detail) {
    if (!detail) return;
    const v = detail.violation || detail;
    document.getElementById('poka-error-code').innerText = v.error_code || 'POKA_YOKE_TRIGGERED';
    document.getElementById('poka-message').innerText = v.message || detail.message || 'Hệ thống đã tự động khóa chốt thao tác để ngăn ngừa sai phạm!';
    document.getElementById('poka-standard').innerText = v.standard_ref || 'QCVN Bộ Y tế';
    document.getElementById('poka-action').innerText = v.action_required || 'Liên hệ cán bộ phụ trách an toàn thực phẩm.';
    document.getElementById('poka-blocked').innerText = v.blocked_operation || 'Thao tác bị hủy bỏ';
    document.getElementById('pokaYokeModal').classList.remove('hidden');
}

function closePokaYokeModal() {
    document.getElementById('pokaYokeModal').classList.add('hidden');
}

function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    const isSuccess = type === 'success';
    const isError = type === 'error';

    toast.className = `pointer-events-auto flex items-center space-x-3 px-4 py-3 rounded-xl shadow-2xl border text-xs font-medium transition-all transform duration-300 translate-y-2 opacity-0 ${
        isSuccess ? 'bg-slate-900 border-emerald-500/50 text-emerald-200' :
        isError ? 'bg-slate-900 border-rose-500/50 text-rose-200' :
        'bg-slate-900 border-slate-700 text-slate-200'
    }`;

    const icon = isSuccess ? 'fa-circle-check text-emerald-400' :
                 isError ? 'fa-circle-exclamation text-rose-400' :
                 'fa-circle-info text-sky-400';

    toast.innerHTML = `
        <i class="fa-solid ${icon} text-sm flex-shrink-0"></i>
        <span class="flex-1">${message}</span>
        <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-white transition ml-2">
            <i class="fa-solid fa-xmark text-xs"></i>
        </button>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });

    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('-translate-y-2', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Exports
window.showToast = showToast;
window.handleStep1Submit = handleStep1Submit;
window.presetStep1Violation = presetStep1Violation;
window.presetStep1Pass = presetStep1Pass;
window.handleStep2Submit = handleStep2Submit;
window.presetStep2Undercooked = presetStep2Undercooked;
window.presetStep2Pass = presetStep2Pass;
window.openUnlockModal = openUnlockModal;
window.closeUnlockModal = closeUnlockModal;
window.executeLockerUnlock = executeLockerUnlock;
window.triggerRapidTraceDemo = triggerRapidTraceDemo;
window.submitRAGQuery = submitRAGQuery;
window.closePokaYokeModal = closePokaYokeModal;
