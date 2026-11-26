        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "学校观测雨列签发",
  "module": "有效雨列签发",
  "caption": "有效雨列签发",
  "detail": "签发选定架位总雨量和排除条数。原始窗口依旧可追溯。",
  "path": "/rain_series",
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
      "name": "flag",
      "label": "复核签条"
    },
    {
      "name": "total",
      "label": "有效累积 mm"
    },
    {
      "name": "n_windows",
      "label": "签发时窗数"
    },
    {
      "name": "omitted",
      "label": "排除时窗数"
    }
  ],
  "layout": "flip",
  "view": "stack",
  "actions": [
    {
      "name": "publish_rain",
      "label": "签发有效雨列",
      "path": "/rain_series/publish-rain",
      "fields": [
        {
          "name": "code",
          "label": "雨列号",
          "kind": "text",
          "initial": "RAIN-24"
        },
        {
          "name": "flag",
          "label": "脉冲复核号",
          "kind": "text",
          "initial": "PULSE-24"
        }
      ],
      "help": "发布表附带独立复核签条。同秤有未结复核时旧签条暂缓签发。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "rain_series";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
