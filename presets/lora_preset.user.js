// ==UserScript==
// @name         LTX2.3 LoRA 快速预设面板
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  在LTX2.3 WebUI中添加LoRA预设一键切换面板
// @author       You
// @match        http://127.0.0.1:7966/*
// @match        http://localhost:7966/*
// @match        http://0.0.0.0:7966/*
// @match        http://*:7966/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const LORA_PRESETS = {
        "无LoRA": {
            "description": "清空所有LoRA，仅使用基础模型",
            "loras": {"lora_01":"None","lora_02":"None","lora_03":"None","lora_04":"None"}
        },
        "仅蒸馏LoRA": {
            "description": "使用蒸馏版LoRA，最快速度",
            "loras": {"lora_01":"None","lora_02":"ltx-2.3-22b-distilled-lora-384-1.1.safetensors","lora_03":"None","lora_04":"None"}
        },
        "仅Crisp增强": {
            "description": "画质增强LoRA",
            "loras": {"lora_01":"None","lora_02":"LTX2.3_Crisp_Enhance.safetensors","lora_03":"None","lora_04":"None"}
        },
        "IC-LoRA Union": {
            "description": "支持深度+边缘控制",
            "loras": {"lora_01":"None","lora_02":"ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors","lora_03":"None","lora_04":"None"}
        },
        "蒸馏+增强": {
            "description": "蒸馏LoRA + Crisp增强双LoRA",
            "loras": {"lora_01":"None","lora_02":"ltx-2.3-22b-distilled-lora-384-1.1.safetensors","lora_03":"LTX2.3_Crisp_Enhance.safetensors","lora_04":"None"}
        },
        "全激活": {
            "description": "所有LoRA槽位（需要32GB+显存）",
            "loras": {"lora_01":"None","lora_02":"ltx-2.3-22b-distilled-lora-384-1.1.safetensors","lora_03":"LTX2.3_Crisp_Enhance.safetensors","lora_04":"ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"}
        }
    };

    // 等待页面加载
    window.addEventListener('load', function() {
        setTimeout(injectPanel, 2000);
    });

    function injectPanel() {
        if (document.getElementById('lora-preset-root')) return;

        const root = document.createElement('div');
        root.id = 'lora-preset-root';
        root.style.cssText = `
            position:fixed;bottom:20px;right:20px;width:300px;max-height:85vh;overflow:auto;
            background:rgba(18,18,22,0.95);border:2px solid #ff6b9d;border-radius:10px;
            padding:14px;z-index:999999;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
            box-shadow:0 8px 32px rgba(0,0,0,0.5);backdrop-filter:blur(10px);
        `;

        root.innerHTML = `
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <div style="font-size:15px;font-weight:bold;color:#ff6b9d;">🎭 LoRA 预设</div>
                <button id="lora-close" style="background:none;border:none;color:#888;cursor:pointer;font-size:18px;">×</button>
            </div>
            <div style="margin-bottom:10px;">
                <select id="lora-preset" style="width:100%;padding:8px;background:#222;color:#fff;border:1px solid #444;border-radius:4px;">
                    <option value="">-- 选择预设 --</option>
                    ${Object.keys(LORA_PRESETS).map(k=>`<option value="${k}">${k}</option>`).join('')}
                </select>
            </div>
            <div id="lora-desc" style="font-size:12px;color:#aaa;margin-bottom:10px;min-height:18px;"></div>
            <button id="lora-apply" style="width:100%;padding:10px;background:linear-gradient(135deg,#ff6b9d,#c06c84);color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:bold;">应用预设</button>
            <div id="lora-status" style="margin-top:10px;font-size:12px;color:#4ade80;"></div>
        `;

        document.body.appendChild(root);

        document.getElementById('lora-close').onclick = () => root.remove();
        document.getElementById('lora-preset').onchange = function() {
            const p = LORA_PRESETS[this.value];
            document.getElementById('lora-desc').textContent = p ? p.description : '';
        };

        document.getElementById('lora-apply').onclick = async function() {
            const name = document.getElementById('lora-preset').value;
            if (!name) { setStatus('⚠️ 请选择预设','#fbbf24'); return; }

            this.disabled = true; this.textContent = '应用中...';
            setStatus('🔄 更新节点...','#60a5fa');

            const preset = LORA_PRESETS[name];
            const graph = getGraph();
            if (!graph) { setStatus('❌ 无法获取工作流','#ef4444'); this.disabled=false; this.textContent='应用预设'; return; }

            let count = 0;
            for (const node of graph.nodes || []) {
                if ((node.type||'').toLowerCase().includes('lora') && (node.type||'').toLowerCase().includes('loader')) {
                    for (const [slot, file] of Object.entries(preset.loras)) {
                        if (findAndSetWidget(node, slot, file)) count++;
                    }
                }
            }

            setStatus(`✅ 已更新 ${count} 个节点·请保存工作流`, '#4ade80');
            this.disabled = false; this.textContent = '应用预设';
        };

        function setStatus(msg, color) {
            document.getElementById('lora-status').textContent = msg;
            document.getElementById('lora-status').style.color = color;
        }

        function getGraph() {
            return window.graph || (window.gradio_app?.graph) || (app?.graph);
        }

        function findAndSetWidget(node, slotName, value) {
            for (const w of node.widgets || []) {
                if ((w.name || '') === slotName || (w.name || '').includes(slotName)) {
                    // 直接修改widget值并触发更新
                    if (w.setValue) w.setValue(value); else w.value = value;
                    triggerNodeUpdate(node);
                    return true;
                }
            }
            return false;
        }

        function triggerNodeUpdate(node) {
            // 触发节点重新计算
            const event = new Event('change', {bubbles:true});
            if (node.widgets?.[0]?.element) node.widgets[0].element.dispatchEvent(event);
        }

        console.log('✅ LoRA预设面板已加载');
    }
})();
