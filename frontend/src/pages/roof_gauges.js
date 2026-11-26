        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "秤架归零记",
  "module": "屋顶气象架位",
  "caption": "屋顶气象架位",
  "detail": "不同架位独立归零和存档。保留日期与屋顶观测点。",
  "path": "/roof_gauges",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "building",
      "label": "楼栋"
    },
    {
      "name": "tared",
      "label": "称重已归零"
    },
    {
      "name": "window",
      "label": "观测时段"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "tare_scale",
      "label": "校核称重归零",
      "path": "/roof_gauges/tare-scale",
      "fields": [
        {
          "name": "gauge",
          "label": "秤架",
          "kind": "text",
          "initial": "G-ART"
        },
        {
          "name": "check",
          "label": "归零凭记",
          "kind": "text",
          "initial": "TARE-111"
        }
      ],
      "help": "编号与楼栋验收记录对应。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "roof_gauges";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
