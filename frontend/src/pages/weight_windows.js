        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "按窗保留原始三路读数",
  "module": "三轴脉冲原始窗",
  "caption": "三轴脉冲原始窗",
  "detail": "每窗记录称重、风振、底座脉冲和折算雨量。复核员可标记保留的人工观测窗。",
  "path": "/weight_windows",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "gauge",
      "label": "秤架"
    },
    {
      "name": "probes",
      "label": "载荷／风振／底座"
    },
    {
      "name": "rain_mm",
      "label": "原始雨量 mm"
    },
    {
      "name": "protected",
      "label": "手工保留"
    },
    {
      "name": "state",
      "label": "数据状态"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "note_window",
      "label": "抄录三路脉冲",
      "path": "/weight_windows/note-window",
      "fields": [
        {
          "name": "code",
          "label": "观测窗编号",
          "kind": "text",
          "initial": "W-PULSE"
        },
        {
          "name": "gauge",
          "label": "秤架",
          "kind": "text",
          "initial": "G-SCI"
        },
        {
          "name": "probes",
          "label": "载荷／风振／底座",
          "kind": "json",
          "initial": [
            14,
            18,
            16
          ]
        },
        {
          "name": "rain_mm",
          "label": "原始雨量 mm",
          "kind": "float",
          "initial": 9.2
        }
      ],
      "help": "以逐窗照片记实测，不覆盖旧窗。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "protect_window",
      "label": "标记人工保留窗",
      "path": "/weight_windows/protect-window",
      "fields": [
        {
          "name": "window_code",
          "label": "原始窗号",
          "kind": "text",
          "initial": "W-PULSE"
        },
        {
          "name": "protected",
          "label": "是否保持",
          "kind": "bool",
          "initial": true
        }
      ],
      "help": "人工观测保留期间不得剔除。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "weight_windows";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
