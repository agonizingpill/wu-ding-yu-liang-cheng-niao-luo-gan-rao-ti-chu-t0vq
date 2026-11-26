        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "独立成分残差与脉冲复核",
  "module": "鸟落脉冲复核",
  "caption": "鸟落脉冲复核",
  "detail": "观察当前秤架三路脉冲的异常分量，并核对人工保留。",
  "path": "/artifact_flags",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "window_code",
      "label": "嫌疑窗"
    },
    {
      "name": "score",
      "label": "独立成分残差"
    },
    {
      "name": "limit_value",
      "label": "分位阈值"
    },
    {
      "name": "action",
      "label": "复核动作"
    },
    {
      "name": "token",
      "label": "分析号"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "decompose",
      "label": "拆解校核过的观测信号",
      "path": "/artifact_flags/decompose",
      "fields": [
        {
          "name": "window_code",
          "label": "嫌疑窗号",
          "kind": "text",
          "initial": "W-PULSE"
        }
      ],
      "help": "以同秤记录建立 FastICA 分量。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "classify_pulse",
      "label": "签认脉冲处置",
      "path": "/artifact_flags/classify-pulse",
      "fields": [
        {
          "name": "code",
          "label": "脉冲复核编号",
          "kind": "text",
          "initial": "PULSE-24"
        },
        {
          "name": "token",
          "label": "分析任务",
          "kind": "token",
          "initial": ""
        },
        {
          "name": "action",
          "label": "建议动作",
          "kind": "text",
          "initial": "排除"
        }
      ],
      "help": "决策只改变是否纳入雨列。原始读数始终留存。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "artifact_flags";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
