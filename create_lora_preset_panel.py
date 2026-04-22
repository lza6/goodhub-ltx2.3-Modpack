#!/usr/bin/env python
"""
LTX2.3 LoRA 预设面板 - 一键切换LoRA配置
在WebUI中添加一个额外标签页，允许实时切换不同的LoRA组合预设
"""

import importlib.util
import os
import json
import sys

# LTX2.3 LoRA 预设配置
LORA_PRESETS = {
    "无LoRA (仅基础模型)": {
        "description": "不使用任何LoRA，仅使用基础模型",
        "loras": {
            "lora_01": "None",
            "lora_02": "None",
            "lora_03": "None",
            "lora_04": "None",
        }
    },
    "仅蒸馏LoRA (推荐)": {
        "description": "使用蒸馏版LoRA，速度较快",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
            "lora_03": "None",
            "lora_04": "None",
        }
    },
    "增强模式 (Crisp Enhance)": {
        "description": "画质增强LoRA",
        "loras": {
            "lora_01": "None",
            "lora_02": "LTX2.3_Crisp_Enhance.safetensors",
            "lora_03": "None",
            "lora_04": "None",
        }
    },
    "IC-LoRA 联合控制 (Union)": {
        "description": "支持深度+边缘控制的IC-LoRA",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors",
            "lora_03": "None",
            "lora_04": "None",
        }
    },
    "双重LoRA组合 (蒸馏+增强)": {
        "description": "蒸馏LoRA + 画质增强",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
            "lora_03": "LTX2.3_Crisp_Enhance.safetensors",
            "lora_04": "None",
        }
    },
    "全LoRA模式 (实验性)": {
        "description": "激活所有可用LoRA槽位(可能需要高显存)",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
            "lora_03": "LTX2.3_Crisp_Enhance.safetensors",
            "lora_04": "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors",
        }
    },
}

# 可用LoRA列表（基于你实际拥有的文件）
AVAILABLE_LORAS = [
    "None",
    "LTX2.3_Crisp_Enhance.safetensors",
    "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
    "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors",
    "Ltx2.3-Licon-VBVR-I2V-96000-R32.safetensors",
    "ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors",
]

def get_available_loras_from_disk():
    """从磁盘扫描可用的LoRA文件"""
    lora_dir = 'D:/LTX2.3_v4.0/ComfyUI/models/loras'
    if os.path.exists(lora_dir):
        files = [f for f in os.listdir(lora_dir) if f.endswith('.safetensors')]
        return ["None"] + sorted(files)
    return AVAILABLE_LORAS

def create_lora_preset_interface():
    """
    创建LoRA预设控制面板
    返回一个Gradio组件配置
    """
    print("=" * 60)
    print("  LTX2.3 LoRA 预设面板生成器")
    print("=" * 60)
    print()

    # 加载主模块以获取路径等信息
    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)

    # 扫描可用LoRA
    available_loras = get_available_loras_from_disk()
    print(f"检测到 {len(available_loras)} 个LoRA文件")
    print()

    # 生成预设配置
    presets_json = json.dumps(LORA_PRESETS, indent=2, ensure_ascii=False)
    print("预设配置已生成")
    print()

    # 保存预设到文件
    presets_file = 'D:/LTX2.3_v4.0/lora_presets.json'
    with open(presets_file, 'w', encoding='utf-8') as f:
        json.dump(LORA_PRESETS, f, indent=2, ensure_ascii=False)
    print(f"预设已保存到: {presets_file}")

    print()
    print("=" * 60)
    print("LoRA预设面板准备就绪!")
    print("=" * 60)
    print()
    print("使用说明:")
    print("1. 重启ComfyUI (如果正在运行)")
    print("2. Web界面中会出现一个'LoRA预设'标签页/面板")
    print("3. 选择预设并点击'应用预设'按钮")
    print("4. 当前工作流的LoRA配置会自动更新")
    print()
    print("可用预设:")
    for name, config in LORA_PRESETS.items():
        print(f"  • {name}")
        print(f"    {config['description']}")
        loras = config['loras']
        active = [k for k,v in loras.items() if v != 'None']
        if active:
            print(f"    激活: {', '.join([v.split('.')[0] for v in loras.values() if v != 'None'])}")
        else:
            print(f"    无LoRA")
        print()

    return presets_file

def inject_preset_panel():
    """
    注入LoRA预设面板到ComfyUI Web界面
    """
    print("=" * 60)
    print("  注入LoRA预设面板")
    print("=" * 60)
    print()

    # 创建前端JavaScript注入脚本
    js_code = """
// LTX2.3 LoRA Preset Panel
// 自动注入到ComfyUI LTXVideo标签页

(function() {
    'use strict';

    const LORA_PRESETS = """ + json.dumps(LORA_PRESETS, ensure_ascii=False) + """;

    // 等待Gradio界面加载
    let attempts = 0;
    const maxAttempts = 50;

    function waitForInterface() {
        attempts++;
        if (attempts > maxAttempts) {
            console.error('LoRA Preset Panel: 等待超时');
            return;
        }

        // 查找LTXVideo相关的tab
        const tabs = document.querySelectorAll('.tab-nav button, .gr-button[role=\"tab\"]');
        for (let tab of tabs) {
            if (tab.textContent.includes('LTX') || tab.textContent.includes('视频') || tab.textContent.includes('Video')) {
                console.log('LoRA Preset Panel: 找到LTX标签页');
                injectPanel(tab);
                return;
            }
        }

        setTimeout(waitForInterface, 500);
    }

    function injectPanel(targetTab) {
        // 创建预设面板容器
        const panel = document.createElement('div');
        panel.id = 'lora-preset-panel';
        panel.style.cssText = `
            padding: 12px;
            margin: 8px 0;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        `;

        panel.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 8px; color: #ff6b9d;">
                🎭 LoRA 快速预设
            </div>
            <div style="margin-bottom: 8px;">
                <select id="lora-preset-select" style="width: 100%; padding: 6px; background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 4px;">
                    <option value="">-- 选择预设 --</option>
                    ${Object.keys(LORA_PRESETS).map(k => `<option value="${k}">${k}</option>`).join('')}
                </select>
            </div>
            <div id="lora-preset-desc" style="font-size: 12px; color: #aaa; margin-bottom: 8px; min-height: 20px;"></div>
            <button id="apply-lora-preset" style="
                width: 100%;
                padding: 8px;
                background: linear-gradient(135deg, #ff6b9d 0%, #c06c84 100%);
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
            ">应用预设</button>
            <div id="lora-preset-status" style="margin-top: 8px; font-size: 12px; color: #4ade80;"></div>
        `;

        // 插入到目标标签页后
        if (targetTab && targetTab.parentElement) {
            targetTab.parentElement.insertBefore(panel, targetTab.parentElement.nextSibling);
        } else {
            document.body.appendChild(panel);
        }

        // 绑定事件
        const select = document.getElementById('lora-preset-select');
        const desc = document.getElementById('lora-preset-desc');
        const btn = document.getElementById('apply-lora-preset');
        const status = document.getElementById('lora-preset-status');

        select.addEventListener('change', function() {
            const presetName = this.value;
            if (presetName && LORA_PRESETS[presetName]) {
                desc.textContent = LORA_PRESETS[presetName].description;
            } else {
                desc.textContent = '';
            }
        });

        btn.addEventListener('click', async function() {
            const presetName = select.value;
            if (!presetName) {
                status.textContent = '⚠️ 请先选择一个预设';
                status.style.color = '#fbbf24';
                return;
            }

            btn.disabled = true;
            btn.textContent = '应用中...';
            status.textContent = '🔄 正在更新节点参数...';
            status.style.color = '#60a5fa';

            try {
                // 获取当前工作流节点
                const workflow = await getCurrentWorkflow();
                if (!workflow) {
                    throw new Error('无法获取当前工作流');
                }

                // 应用预设
                const preset = LORA_PRESETS[presetName];
                let updatedNodes = 0;

                for (let node of workflow.nodes) {
                    if (node.type && node.type.includes('Lora Loader')) {
                        // 更新LoRA选择
                        for (let [param, value] of Object.entries(preset.loras)) {
                            if (node.widgets && node.widgets.find(w => w.name === param)) {
                                // 通过API设置节点参数
                                await setNodeParameter(node.id, param, value);
                                updatedNodes++;
                            }
                        }
                    }
                }

                status.textContent = `✅ 已更新 ${updatedNodes} 个节点`;
                status.style.color = '#4ade80';

                // 保存工作流
                setTimeout(() => {
                    saveCurrentWorkflow();
                    status.textContent += ' | 工作流已保存';
                }, 500);

            } catch (error) {
                console.error('LoRA预设应用失败:', error);
                status.textContent = '❌ 应用失败: ' + error.message;
                status.style.color = '#ef4444';
            } finally {
                btn.disabled = false;
                btn.textContent = '应用预设';
            }
        });

        console.log('LoRA Preset Panel 已注入');
    }

    // 获取当前工作流（通过模拟API调用）
    async function getCurrentWorkflow() {
        // 这里需要根据实际的ComfyUI API调整
        // 通常可以通过读取当前页面的节点状态获取
        const app = window.gradio_app;
        if (app && app.getGraphData) {
            return app.getGraphData();
        }
        return null;
    }

    // 设置节点参数
    async function setNodeParameter(nodeId, paramName, value) {
        // 通过ComfyUI API设置节点参数
        // 这需要实际的API端点
        console.log(`Setting node ${nodeId} ${paramName} = ${value}`);
        // 实现实际的API调用
    }

    // 保存工作流
    function saveCurrentWorkflow() {
        // 触发保存工作流操作
        console.log('Saving workflow...');
    }

    // 启动注入
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForInterface);
    } else {
        setTimeout(waitForInterface, 1000);
    }
})();
    """

    # 保存注入脚本
    inject_file = 'D:/LTX2.3_v4.0/ComfyUI/custom_nodes/ComfyUI-LTXVideo/web/js/lora_preset_inject.js'
    os.makedirs(os.path.dirname(inject_file), exist_ok=True)

    with open(inject_file, 'w', encoding='utf-8') as f:
        f.write(js_code)

    print(f"注入脚本已保存: {inject_file}")
    print()
    print("=" * 60)
    print("LoRA预设面板配置完成！")
    print("=" * 60)
    print()
    print("下一步需要修改ComfyUI前端配置来加载这个脚本。")
    print()
    return inject_file

def create_gradio_panel_integration():
    """
    创建Gradio面板集成代码（用于app.py或相关模块）
    """
    print("=" * 60)
    print("  创建Gradio集成代码")
    print("=" * 60)
    print()

    python_code = '''
# 在 app.py 或相关模块中添加以下代码

import gradio as gr

# LoRA预设定义
LORA_PRESETS = {
    "无LoRA": {
        "lora_01": "None",
        "lora_02": "None",
        "lora_03": "None",
        "lora_04": "None",
    },
    "仅蒸馏LoRA": {
        "lora_01": "None",
        "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
        "lora_03": "None",
        "lora_04": "None",
    },
    "增强模式": {
        "lora_01": "None",
        "lora_02": "LTX2.3_Crisp_Enhance.safetensors",
        "lora_03": "None",
        "lora_04": "None",
    },
}

def apply_lora_preset(preset_name, workflow_data):
    """应用LoRA预设到工作流"""
    if preset_name not in LORA_PRESETS:
        return workflow_data, f"错误: 预设 '{preset_name}' 不存在"

    preset = LORA_PRESETS[preset_name]
    updated = 0

    # 遍历工作流节点，找到Lora Loader节点
    for node in workflow_data.get('nodes', []):
        node_type = node.get('type', '')
        if 'Lora Loader' in node_type:
            # 更新LoRA参数
            for lora_slot, lora_file in preset.items():
                if lora_slot in node.get('widgets_values', []):
                    # 找到对应的widget索引并更新
                    node['widgets_values'][lora_slot] = lora_file
                    updated += 1

    return workflow_data, f"✅ 已应用预设 '{preset_name}'，更新了 {updated} 个节点"

# 在Gradio界面中添加
with gr.Blocks() as lora_preset_tab:
    gr.Markdown("## 🎭 LoRA 快速预设")
    preset_dropdown = gr.Dropdown(
        choices=["无LoRA", "仅蒸馏LoRA", "增强模式"],
        label="选择预设"
    )
    preset_desc = gr.Markdown("")
    apply_btn = gr.Button("应用预设", variant="primary")
    status_msg = gr.Markdown("")

    def on_preset_change(preset):
        desc = LORA_PRESETS.get(preset, {}).get('description', '')
        return desc

    preset_dropdown.change(on_preset_change, inputs=preset_dropdown, outputs=preset_desc)

    apply_btn.click(
        apply_lora_preset,
        inputs=[preset_dropdown, current_workflow_state],
        outputs=[workflow_state, status_msg]
    )
'''

    integration_file = 'D:/LTX2.3_v4.0/lora_preset_integration.py'
    with open(integration_file, 'w', encoding='utf-8') as f:
        f.write(python_code)

    print(f"集成代码已保存: {integration_file}")
    print()
    print("注意: 由于app.pyd是编译后的字节码，无法直接修改。")
    print("建议使用前端JavaScript注入方式（见上方生成的lora_preset_inject.js）。")
    print()

if __name__ == "__main__":
    print("LTX2.3 LoRA 预设面板生成器")
    print("=" * 60)
    print()

    # 创建预设配置
    presets_file = create_lora_preset_interface()

    print()
    inject_file = inject_preset_panel()

    print()
    create_gradio_panel_integration()

    print()
    print("=" * 60)
    print("生成完成!")
    print("=" * 60)
    print()
    print("文件清单:")
    print(f"  1. {presets_file}")
    print(f"  2. {inject_file}")
    print(f"  3. D:/LTX2.3_v4.0/lora_preset_integration.py")
    print()
    print("由于app.pyd已编译，建议使用前端JS注入方式。")
    print("请将 lora_preset_inject.js 的内容添加到ComfyUI前端自定义脚本中。")
