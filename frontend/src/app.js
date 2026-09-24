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

function switchMainTab(targetTabId) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(b => {
        if (b.dataset.tab === targetTabId) {
            b.classList.add('border-emerald-400', 'text-emerald-400', 'bg-emerald-500/10');
            b.classList.remove('border-transparent', 'text-slate-400');
        } else {
            b.classList.remove('border-emerald-400', 'text-emerald-400', 'bg-emerald-500/10');
            b.classList.add('border-transparent', 'text-slate-400', 'hover:text-slate-200');
        }
    });

    tabContents.forEach(content => {
        content.classList.toggle('hidden', content.id !== targetTabId);
    });

    if (targetTabId === 'tab-trace' && STATE.graphViewer) {
        setTimeout(() => STATE.graphViewer.resize(), 100);
    }
}

function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            switchMainTab(btn.dataset.tab);
        });
    });
}

function navigateToContext(contextKey) {
    switch (contextKey) {
        case 'facilities':
        case 'suppliers':
        case 'batches':
            switchMainTab('tab-inspection');
            switchInspectionStep(1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        case 'step1':
            switchMainTab('tab-inspection');
            switchInspectionStep(1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        case 'step2':
            switchMainTab('tab-inspection');
            switchInspectionStep(2);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        case 'lockers':
            switchMainTab('tab-inspection');
            switchInspectionStep(3);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        case 'incidents':
            switchMainTab('tab-trace');
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        default:
            break;
    }
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

    if (!STATE.currentFacilityId && STATE.facilities.length > 0) {
        STATE.currentFacilityId = STATE.facilities[0].id;
    }

    select.innerHTML = STATE.facilities.map(f => `
        <option value="${f.id}" ${f.id === STATE.currentFacilityId ? 'selected' : ''}>🏫 ${f.name} (${f.daily_meal_capacity} suất/ngày)</option>
    `).join('');

    updateCurrentFacilityUI();

    select.onchange = (e) => {
        STATE.currentFacilityId = parseInt(e.target.value);
        updateCurrentFacilityUI();
        loadSampleLockers();
    };
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
    if (!STATE.batches || STATE.batches.length === 0) {
        batchSelect.innerHTML = `<option value="">(Chưa có lô hàng)</option>`;
        return;
    }
    batchSelect.innerHTML = STATE.batches.map(b => {
        const isApproved = b.status === 'APPROVED';
        const isRejected = b.status === 'REJECTED';
        const statusText = isApproved ? 'ĐẠT' : (isRejected ? 'BỊ TỪ CHỐI' : b.status);
        return `
            <option value="${b.id}">
                ${b.batch_code} - ${b.name} [${statusText}] (${b.category} - HSD: ${b.expiry_date ? new Date(b.expiry_date).toLocaleDateString('vi-VN') : 'N/A'})
            </option>
        `;
    }).join('');
}

function populateStep2Selects() {
    const batchSelect = document.getElementById('step2-batches');
    const listContainer = document.getElementById('step2-batches-list');

    // Keep hidden native select synchronized for any fallback / headless scripts
    if (batchSelect) {
        batchSelect.innerHTML = STATE.batches.map(b => `
            <option value="${b.id}" ${b.status === 'REJECTED' ? 'class="text-rose-400 font-bold"' : ''}>
                ${b.batch_code} - ${b.name} [Trạng thái: ${b.status}]
            </option>
        `).join('');
    }

    if (!listContainer) return;

    if (!STATE.batches || STATE.batches.length === 0) {
        listContainer.innerHTML = `<div class="p-4 text-center text-xs text-slate-500">Chưa có lô nguyên liệu nào trong kho.</div>`;
        onStep2BatchCheckboxChange();
        return;
    }

    listContainer.innerHTML = STATE.batches.map(b => {
        const isApproved = b.status === 'APPROVED';
        const isRejected = b.status === 'REJECTED';
        const badgeClass = isApproved 
            ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
            : (isRejected ? 'bg-rose-500/20 text-rose-400 border-rose-500/30' : 'bg-amber-500/20 text-amber-400 border-amber-500/30');
        const badgeText = isApproved ? 'ĐẠT CHUẨN' : (isRejected ? 'BỊ TỪ CHỐI' : b.status);
        const badgeIcon = isApproved ? 'fa-circle-check' : (isRejected ? 'fa-circle-xmark' : 'fa-clock');

        return `
            <label class="flex items-center justify-between p-2.5 hover:bg-slate-900 cursor-pointer transition select-none group" for="step2-cb-${b.id}">
                <div class="flex items-center space-x-3 min-w-0">
                    <input type="checkbox" id="step2-cb-${b.id}" value="${b.id}" data-status="${b.status}"
                        class="step2-batch-checkbox w-4 h-4 rounded bg-slate-900 border-slate-700 text-amber-500 focus:ring-0 cursor-pointer"
                        onchange="onStep2BatchCheckboxChange()">
                    <div class="min-w-0">
                        <div class="flex items-center space-x-2">
                            <span class="font-mono font-bold text-xs text-amber-400 group-hover:text-amber-300">${b.batch_code}</span>
                            <span class="text-xs font-semibold text-slate-200 truncate">${b.name}</span>
                        </div>
                        <div class="text-[10px] text-slate-400">
                            ${b.category || 'Thực phẩm'} &bull; HSD: ${b.expiry_date ? new Date(b.expiry_date).toLocaleDateString('vi-VN') : 'N/A'}
                        </div>
                    </div>
                </div>
                <div class="flex-shrink-0 ml-2">
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold border ${badgeClass}">
                        <i class="fa-solid ${badgeIcon} mr-1"></i>
                        <span>${badgeText}</span>
                    </span>
                </div>
            </label>
        `;
    }).join('');

    // Auto-select first APPROVED batch by default if none checked
    const approvedCbs = listContainer.querySelectorAll('.step2-batch-checkbox[data-status="APPROVED"]');
    if (approvedCbs.length > 0) {
        approvedCbs[0].checked = true;
    }
    onStep2BatchCheckboxChange();
}

function onStep2BatchCheckboxChange() {
    const checkboxes = document.querySelectorAll('.step2-batch-checkbox');
    const batchSelect = document.getElementById('step2-batches');
    const selectedCountEl = document.getElementById('step2-selected-count');
    const warningEl = document.getElementById('step2-rejected-warning');

    let count = 0;
    let hasRejected = false;
    const selectedIds = new Set();

    checkboxes.forEach(cb => {
        if (cb.checked) {
            count++;
            selectedIds.add(cb.value);
            if (cb.getAttribute('data-status') === 'REJECTED') {
                hasRejected = true;
            }
        }
    });

    if (selectedCountEl) selectedCountEl.textContent = count;

    if (warningEl) {
        if (hasRejected) {
            warningEl.classList.remove('hidden');
        } else {
            warningEl.classList.add('hidden');
        }
    }

    // Keep native select options synchronized
    if (batchSelect) {
        Array.from(batchSelect.options).forEach(opt => {
            opt.selected = selectedIds.has(opt.value);
        });
    }
}

function selectApprovedBatchesStep2() {
    const checkboxes = document.querySelectorAll('.step2-batch-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = (cb.getAttribute('data-status') === 'APPROVED');
    });
    onStep2BatchCheckboxChange();
}

function clearSelectedBatchesStep2() {
    const checkboxes = document.querySelectorAll('.step2-batch-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = false;
    });
    onStep2BatchCheckboxChange();
}

// Kiểm thực Bước 1
async function handleStep1Submit(e) {
    if (e) e.preventDefault();
    const batchInput = document.getElementById('step1-batch');
    const batchId = batchInput ? parseInt(batchInput.value) : NaN;
    if (isNaN(batchId)) {
        showToast("Vui lòng chọn lô hàng nhập kho trước khi phê duyệt.", "warning");
        return;
    }

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

    const submitBtn = document.getElementById('btnStep1Submit');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i><span>Đang kiểm tra rào chắn...</span>`;
    }

    try {
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
            showToast("Phê duyệt nhập kho thành công! Đã cấp phép chuyển sang Bước 2.", "success");
            alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/50 bg-emerald-950/40 text-emerald-300 text-xs";
            alertBox.innerHTML = `
                <div class="flex items-center space-x-2 font-bold text-sm text-emerald-400 mb-1">
                    <i class="fa-solid fa-circle-check text-lg"></i>
                    <span>ĐẠT CHUẨN! ĐÃ DUYỆT NHẬP KHO THỰC PHẨM</span>
                </div>
                <p class="mb-3 text-slate-300">Phiếu kiểm thực số #${res.data.id} đã lưu trữ thành công. Lô hàng đủ điều kiện chuyển sang Bước 2 (Chế biến).</p>
                <button type="button" onclick="switchInspectionStep(2)" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition inline-flex items-center space-x-1.5 shadow-md">
                    <span>Chuyển Sang Bước 2: Chế Biến</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                </button>
            `;
            alertBox.classList.remove('hidden');
        }
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            submitBtn.innerHTML = `<i class="fa-solid fa-file-circle-check text-sm mr-2"></i><span>Phê Duyệt Nhập Kho Lô Hàng</span>`;
        }
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
    const mealName = document.getElementById('step2-meal-name').value.trim();
    if (!mealName) {
        showToast("Vui lòng nhập tên món ăn bán trú.", "warning");
        return;
    }

    let selectedBatchIds = [];
    const checkedBoxes = document.querySelectorAll('.step2-batch-checkbox:checked');
    if (checkedBoxes.length > 0) {
        selectedBatchIds = Array.from(checkedBoxes).map(cb => parseInt(cb.value));
    } else {
        const batchSelect = document.getElementById('step2-batches');
        if (batchSelect && batchSelect.selectedOptions) {
            selectedBatchIds = Array.from(batchSelect.selectedOptions).map(opt => parseInt(opt.value));
        }
    }

    if (selectedBatchIds.length === 0) {
        showToast("Vui lòng chọn ít nhất 1 lô nguyên liệu cấu thành món ăn!", "warning");
        return;
    }

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

    const submitBtn = document.getElementById('btnStep2Submit');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i><span>Đang thẩm định rào chắn Poka-Yoke...</span>`;
    }

    try {
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
                <p><strong>Lỗi:</strong> ${v.message || res.data.message || 'Vi phạm an toàn chế biến'}</p>
                <p><strong>Căn cứ:</strong> ${v.standard_ref || 'QCVN 8-2:2011/BYT'}</p>
                <p><strong>Hành động:</strong> ${v.action_required || 'Hủy bỏ và nấu lại'}</p>
            `;
            alertBox.classList.remove('hidden');
        } else if (res.ok) {
            showToast(`Món ăn '${res.data.meal_name}' đạt chuẩn nấu chín! Sẵn sàng lưu mẫu.`, "success");
            alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/50 bg-emerald-950/40 text-emerald-300 text-xs";
            alertBox.innerHTML = `
                <div class="flex items-center space-x-2 font-bold text-sm text-emerald-400 mb-1">
                    <i class="fa-solid fa-circle-check text-lg"></i>
                    <span>ĐẠT CHUẨN NẤU CHÍN HOÀN TOÀN! (Nhiệt độ tâm ${res.data.core_temp}°C &ge; 75.0°C)</span>
                </div>
                <p class="mb-3 text-slate-300">Món ăn '${res.data.meal_name}' đã được phê duyệt. Vui lòng tiến hành Lưu mẫu thức ăn 24H tại Bước 3.</p>
                <button type="button" onclick="switchInspectionStep(3)" class="px-3.5 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs transition inline-flex items-center space-x-1.5 shadow-md">
                    <span>Chuyển Sang Bước 3: Tủ Lưu Mẫu</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                </button>
            `;
            alertBox.classList.remove('hidden');
        }
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            submitBtn.innerHTML = `<i class="fa-solid fa-fire-burner text-sm mr-2"></i><span>Kiểm Định Nhiệt Độ Nấu Chín</span>`;
        }
    }
}

function presetStep2Undercooked() {
    selectApprovedBatchesStep2();
    document.getElementById('step2-meal-name').value = 'Gà kho gừng chưa chín thấu (Test Nhiệt Độ)';
    document.getElementById('step2-core-temp').value = '61.5';
    document.getElementById('step2-sensory').value = 'UNDERCOOKED_RAW_INSIDE';
    handleStep2Submit();
}

function presetStep2Contaminated() {
    clearSelectedBatchesStep2();
    const rejectedCb = document.querySelector('.step2-batch-checkbox[data-status="REJECTED"]');
    if (rejectedCb) {
        rejectedCb.checked = true;
    } else {
        const firstCb = document.querySelector('.step2-batch-checkbox');
        if (firstCb) firstCb.checked = true;
    }
    onStep2BatchCheckboxChange();
    document.getElementById('step2-meal-name').value = 'Món dùng nguyên liệu vi phạm (Test Poka-Yoke)';
    document.getElementById('step2-core-temp').value = '82.0';
    document.getElementById('step2-sensory').value = 'COOKED_THOROUGHLY';
    handleStep2Submit();
}

function presetStep2Pass() {
    selectApprovedBatchesStep2();
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
let lastActiveUnlockTrigger = null;

function openUnlockModal(lockerId, lockerNumber, hoursLeft) {
    lastActiveUnlockTrigger = document.activeElement;
    activeUnlockLockerId = lockerId;
    const titleEl = document.getElementById('unlock-modal-title');
    if (titleEl) {
        titleEl.innerHTML = `<i class="fa-solid fa-key text-amber-400"></i><span>Mở Khóa Tủ Mẫu: ${lockerNumber}</span>`;
    }
    const hoursEl = document.getElementById('unlock-modal-hours');
    if (hoursEl) {
        hoursEl.innerText = hoursLeft > 0 ? `${hoursLeft} giờ nữa mới đủ điều kiện quy chuẩn 24H!` : 'Đã đủ 24H theo quy định.';
    }

    // Reset fields
    const toggle = document.getElementById('unlock-override-toggle');
    if (toggle) toggle.checked = false;
    const reasonInput = document.getElementById('unlock-reason');
    if (reasonInput) reasonInput.value = '';
    const passInput = document.getElementById('unlock-passcode');
    if (passInput) passInput.value = '';

    const modal = document.getElementById('unlockModal');
    if (modal) {
        modal.classList.remove('hidden');
        setTimeout(() => {
            if (toggle) toggle.focus();
        }, 50);
    }
}

function closeUnlockModal() {
    const modal = document.getElementById('unlockModal');
    if (!modal) return;
    modal.classList.add('hidden');
    activeUnlockLockerId = null;
    if (lastActiveUnlockTrigger && typeof lastActiveUnlockTrigger.focus === 'function') {
        lastActiveUnlockTrigger.focus();
        lastActiveUnlockTrigger = null;
    }
}

function handleUnlockBackdropClick(e) {
    if (e.target === document.getElementById('unlockModal')) {
        closeUnlockModal();
    }
}

async function executeLockerUnlock() {
    if (!activeUnlockLockerId) return;
    const isOverride = document.getElementById('unlock-override-toggle').checked;
    const reason = document.getElementById('unlock-reason').value.trim();
    const passcode = document.getElementById('unlock-passcode').value.trim();

    const payload = {
        operator_name: "Cán bộ Y tế Bếp ăn",
        is_emergency_override: isOverride,
        override_reason: reason || null,
        override_passcode: passcode || null
    };

    const confirmBtn = document.getElementById('btnConfirmUnlock');
    if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.classList.add('opacity-75', 'cursor-not-allowed');
        confirmBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1.5"></i><span>Đang xác thực...</span>`;
    }

    try {
        const res = await API.post(`/sample-lockers/${activeUnlockLockerId}/unlock`, payload);

        if (res.status === 422) {
            const v = res.data.violation || res.data.detail || res.data;
            showPokaYokeModal(v);
        } else if (res.ok) {
            showToast("Mở niêm phong tủ mẫu thành công: " + (res.data.message || 'Đã mở chốt'), "success");
            closeUnlockModal();
            await loadSampleLockers();
        }
    } finally {
        if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            confirmBtn.innerHTML = `<i class="fa-solid fa-lock-open text-xs"></i><span>Xác Nhận Mở Chốt Tủ</span>`;
        }
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
function clearRAGQuery() {
    const input = document.getElementById('ragQueryInput');
    const clearBtn = document.getElementById('btnRagClear');
    if (input) {
        input.value = '';
        input.focus();
    }
    if (clearBtn) {
        clearBtn.classList.add('hidden');
    }
}

function toggleRagClearBtn() {
    const input = document.getElementById('ragQueryInput');
    const clearBtn = document.getElementById('btnRagClear');
    if (!input || !clearBtn) return;
    if (input.value.trim().length > 0) {
        clearBtn.classList.remove('hidden');
    } else {
        clearBtn.classList.add('hidden');
    }
}

async function submitRAGQuery(queryText) {
    const input = document.getElementById('ragQueryInput');
    const query = (queryText !== undefined && queryText !== null ? queryText : (input ? input.value : '')).trim();
    if (!query) return;

    if (input) {
        input.value = query;
        toggleRagClearBtn();
    }

    const answerBox = document.getElementById('ragAnswerBox');
    const timerBadge = document.getElementById('ragTimerBadge');
    const submitBtn = document.getElementById('btnRagSubmit');

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1.5"></i><span>Đang tra cứu...</span>`;
    }

    answerBox.innerHTML = `
        <div class="p-8 text-center text-slate-400 text-xs border border-dashed border-sky-500/30 rounded-2xl bg-slate-900/60 animate-pulse">
            <i class="fa-solid fa-spinner fa-spin mr-2 text-sky-400 text-base"></i>
            <span>Đang đối soát ngữ nghĩa tri thức QCVN 8-2, QĐ 1246 và văn bản pháp luật ATTP...</span>
        </div>
    `;

    try {
        const res = await API.post('/rag/query', { query, top_k: 3 });
        if (res.ok) {
            const data = res.data;
            if (timerBadge) {
                timerBadge.innerText = `${data.execution_time_ms} ms (100% Offline Local)`;
                timerBadge.className = "px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
            }
            
            // Format answer with simple markdown to HTML
            let formattedHtml = data.answer
                .replace(/^## (.*$)/gim, '<h2 class="text-base font-bold text-white mt-3 mb-2 flex items-center space-x-1.5"><i class="fa-solid fa-file-lines text-sky-400 text-xs mr-1"></i><span>$1</span></h2>')
                .replace(/^### (.*$)/gim, '<h3 class="text-sm font-bold text-emerald-400 mt-2.5 mb-1.5">$1</h3>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong class="text-slate-100 font-bold">$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em class="text-slate-300 italic">$1</em>')
                .replace(/\n/gim, '<br>');

            // Citations pill badges
            let citationsHtml = '';
            if (data.citations && data.citations.length > 0) {
                citationsHtml = `
                    <div class="mt-4 pt-3.5 border-t border-slate-800 flex flex-wrap items-center gap-1.5">
                        <span class="text-[11px] font-bold text-slate-400 mr-1.5 inline-flex items-center">
                            <i class="fa-solid fa-book-bookmark text-sky-400 mr-1"></i>Viện dẫn căn cứ:
                        </span>
                        ${data.citations.map(c => `
                            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-500/15 text-sky-300 border border-sky-500/30 inline-flex items-center shadow-sm">
                                <i class="fa-solid fa-stamp text-[9px] mr-1 text-sky-400"></i>${c}
                            </span>
                        `).join('')}
                    </div>
                `;
            }

            // Relevant Chunks (Source Accordion Drawer)
            let chunksHtml = '';
            if (data.relevant_chunks && data.relevant_chunks.length > 0) {
                chunksHtml = `
                    <details class="mt-3.5 group border border-slate-800 rounded-xl bg-slate-950/60 overflow-hidden">
                        <summary class="flex items-center justify-between p-3 cursor-pointer hover:bg-slate-900/80 transition text-xs font-semibold text-slate-300 select-none">
                            <span class="flex items-center space-x-2">
                                <i class="fa-solid fa-file-contract text-emerald-400"></i>
                                <span>Trích đoạn văn bản gốc đối chiếu (${data.relevant_chunks.length} điều khoản)</span>
                            </span>
                            <i class="fa-solid fa-chevron-down text-slate-500 text-[10px] transition group-open:rotate-180"></i>
                        </summary>
                        <div class="p-3 pt-2 space-y-3 border-t border-slate-800/80 divide-y divide-slate-800/60">
                            ${data.relevant_chunks.map((ch, idx) => `
                                <div class="${idx > 0 ? 'pt-3' : ''} text-xs">
                                    <div class="flex items-center justify-between text-[11px] mb-1">
                                        <span class="font-bold text-emerald-400">${ch.title}</span>
                                        <span class="font-mono text-[10px] text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                                            Match: ${(ch.relevance_score * 100).toFixed(0)}%
                                        </span>
                                    </div>
                                    <div class="font-mono text-[10px] text-sky-300 mb-1.5">${ch.standard_code}</div>
                                    <p class="text-slate-300 text-[11px] leading-relaxed bg-slate-900/80 p-2.5 rounded-lg border border-slate-800/80 whitespace-pre-line font-mono">
                                        ${ch.content}
                                    </p>
                                </div>
                            `).join('')}
                        </div>
                    </details>
                `;
            }

            answerBox.innerHTML = `
                <div class="p-5 rounded-2xl border border-slate-700 bg-slate-900/90 text-xs leading-relaxed shadow-xl">
                    <div class="prose prose-invert max-w-none text-slate-200">
                        ${formattedHtml}
                    </div>
                    ${citationsHtml}
                    ${chunksHtml}
                    <div class="mt-4 pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-400">
                        <span class="flex items-center space-x-1.5">
                            <i class="fa-solid fa-shield-halved text-emerald-400"></i>
                            <span>Chế độ: <strong>${data.engine_mode}</strong> (BM25 Hybrid)</span>
                        </span>
                        <span class="flex items-center space-x-3">
                            <span>Độ tin cậy: <strong class="text-emerald-400 font-mono">${(data.confidence_score * 100).toFixed(0)}%</strong></span>
                            <span>Thời gian: <strong class="text-sky-400 font-mono">${data.execution_time_ms} ms</strong></span>
                        </span>
                    </div>
                </div>
            `;
        } else {
            answerBox.innerHTML = `<div class="p-4 rounded-xl border border-rose-500/50 bg-rose-950/30 text-rose-300 text-xs">Lỗi tra cứu: ${res.data?.detail || res.data?.message || 'Không thể tra cứu tri thức'}</div>`;
        }
    } catch (e) {
        answerBox.innerHTML = `<div class="p-4 rounded-xl border border-rose-500/50 bg-rose-950/30 text-rose-300 text-xs">Lỗi tra cứu: ${e.message}</div>`;
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            submitBtn.innerHTML = `<i class="fa-solid fa-bolt mr-1.5"></i><span>Tra Cứu</span>`;
        }
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
let lastPokaActiveTrigger = null;

function showPokaYokeModal(detail) {
    if (!detail) return;
    lastPokaActiveTrigger = document.activeElement;
    const v = detail.violation || detail;
    const errCodeEl = document.getElementById('poka-error-code');
    if (errCodeEl) errCodeEl.innerText = v.error_code || 'POKA_YOKE_TRIGGERED';
    const msgEl = document.getElementById('poka-message');
    if (msgEl) msgEl.innerText = v.message || detail.message || 'Hệ thống đã tự động khóa chốt thao tác để ngăn ngừa sai phạm!';
    const stdEl = document.getElementById('poka-standard');
    if (stdEl) stdEl.innerText = v.standard_ref || 'QCVN Bộ Y tế';
    const actEl = document.getElementById('poka-action');
    if (actEl) actEl.innerText = v.action_required || 'Liên hệ cán bộ phụ trách an toàn thực phẩm.';
    const blkEl = document.getElementById('poka-blocked');
    if (blkEl) blkEl.innerText = v.blocked_operation || 'Thao tác bị hủy bỏ';

    const modal = document.getElementById('pokaYokeModal');
    if (modal) {
        modal.classList.remove('hidden');
        const dismissBtn = document.getElementById('poka-dismiss-btn');
        if (dismissBtn) {
            setTimeout(() => dismissBtn.focus(), 50);
        }
    }
}

function closePokaYokeModal() {
    const modal = document.getElementById('pokaYokeModal');
    if (!modal) return;
    modal.classList.add('hidden');
    if (lastPokaActiveTrigger && typeof lastPokaActiveTrigger.focus === 'function') {
        lastPokaActiveTrigger.focus();
        lastPokaActiveTrigger = null;
    }
}

function handlePokaBackdropClick(e) {
    if (e.target === document.getElementById('pokaYokeModal')) {
        closePokaYokeModal();
    }
}

// Global Keyboard Shortcut: ESC key closes open modals
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' || e.key === 'Esc') {
        const pokaModal = document.getElementById('pokaYokeModal');
        if (pokaModal && !pokaModal.classList.contains('hidden')) {
            closePokaYokeModal();
            return;
        }

        const unlockModal = document.getElementById('unlockModal');
        if (unlockModal && !unlockModal.classList.contains('hidden')) {
            closeUnlockModal();
            return;
        }
    }
});

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

// ==========================================
// STEPPER WORKFLOW CONTROLS
// ==========================================
let currentInspectionStep = 1;
let isAllStepsView = false;

function switchInspectionStep(stepNumber) {
    currentInspectionStep = stepNumber;
    isAllStepsView = false;
    updateInspectionStepUI();
}

function toggleAllStepsView() {
    isAllStepsView = !isAllStepsView;
    updateInspectionStepUI();
}

function updateInspectionStepUI() {
    const panels = [
        document.getElementById('step1-panel'),
        document.getElementById('step2-panel'),
        document.getElementById('step3-panel')
    ];
    const navBtns = [
        document.getElementById('step-nav-1'),
        document.getElementById('step-nav-2'),
        document.getElementById('step-nav-3')
    ];
    const container = document.getElementById('inspectionPanelsContainer');
    const toggleBtn = document.getElementById('toggleViewBtn');

    if (isAllStepsView) {
        if (container) {
            container.className = "grid grid-cols-1 lg:grid-cols-3 gap-6";
        }
        panels.forEach(p => {
            if (p) p.classList.remove('hidden');
        });
        navBtns.forEach(btn => {
            if (btn) btn.className = "step-nav-btn flex items-center space-x-2 sm:space-x-3 p-2.5 sm:p-3 rounded-xl border transition text-left bg-slate-950/60 border-slate-800 text-slate-400";
        });
        if (toggleBtn) toggleBtn.innerHTML = `<i class="fa-solid fa-compress mr-1.5 text-emerald-400"></i> Xem 1 bước tập trung`;
    } else {
        if (container) {
            container.className = "space-y-6";
        }
        panels.forEach((p, idx) => {
            if (!p) return;
            if (idx === currentInspectionStep - 1) {
                p.classList.remove('hidden');
            } else {
                p.classList.add('hidden');
            }
        });
        navBtns.forEach((btn, idx) => {
            if (!btn) return;
            const numBadge = btn.querySelector('.step-num-badge');
            if (idx === currentInspectionStep - 1) {
                btn.className = "step-nav-btn flex items-center space-x-2 sm:space-x-3 p-2.5 sm:p-3 rounded-xl border transition text-left bg-emerald-500/10 border-emerald-500/40 text-white shadow-lg";
                if (numBadge) numBadge.className = "step-num-badge w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center font-bold text-xs sm:text-sm bg-emerald-500 text-white flex-shrink-0";
            } else {
                btn.className = "step-nav-btn flex items-center space-x-2 sm:space-x-3 p-2.5 sm:p-3 rounded-xl border transition text-left bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200";
                if (numBadge) numBadge.className = "step-num-badge w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center font-bold text-xs sm:text-sm bg-slate-800 text-slate-400 flex-shrink-0";
            }
        });
        if (toggleBtn) toggleBtn.innerHTML = `<i class="fa-solid fa-table-columns mr-1.5 text-slate-400"></i> Xem cả 3 bước`;
    }
}

// Exports
window.showToast = showToast;
window.switchMainTab = switchMainTab;
window.navigateToContext = navigateToContext;
window.switchInspectionStep = switchInspectionStep;
window.toggleAllStepsView = toggleAllStepsView;
window.handleStep1Submit = handleStep1Submit;
window.presetStep1Violation = presetStep1Violation;
window.presetStep1Pass = presetStep1Pass;
window.handleStep2Submit = handleStep2Submit;
window.presetStep2Undercooked = presetStep2Undercooked;
window.presetStep2Pass = presetStep2Pass;
window.presetStep2Contaminated = presetStep2Contaminated;
window.selectApprovedBatchesStep2 = selectApprovedBatchesStep2;
window.clearSelectedBatchesStep2 = clearSelectedBatchesStep2;
window.onStep2BatchCheckboxChange = onStep2BatchCheckboxChange;
window.openUnlockModal = openUnlockModal;
window.closeUnlockModal = closeUnlockModal;
window.handleUnlockBackdropClick = handleUnlockBackdropClick;
window.executeLockerUnlock = executeLockerUnlock;
window.triggerRapidTraceDemo = triggerRapidTraceDemo;
window.submitRAGQuery = submitRAGQuery;
window.clearRAGQuery = clearRAGQuery;
window.toggleRagClearBtn = toggleRagClearBtn;
window.showPokaYokeModal = showPokaYokeModal;
window.closePokaYokeModal = closePokaYokeModal;
window.handlePokaBackdropClick = handlePokaBackdropClick;
