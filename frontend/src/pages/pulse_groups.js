        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "同秤嫌疑窗整组复核",
  "module": "鸟落脉冲复核",
  "caption": "同秤嫌疑窗整组复核",
  "detail": "圈选同秤嫌疑窗，冻结组外同秤基线统一判分。复核未结案时同秤旧签条暂缓签发。",
  "path": "/pulse_groups",
  "columns": [
    {
      "name": "code",
      "label": "复核组编号"
    },
    {
      "name": "gauge",
      "label": "秤架"
    },
    {
      "name": "windows",
      "label": "嫌疑窗"
    },
    {
      "name": "scores",
      "label": "各窗残差"
    },
    {
      "name": "limit_value",
      "label": "分位阈值"
    },
    {
      "name": "status",
      "label": "复核状态"
    },
    {
      "name": "flag",
      "label": "整组签条"
    },
    {
      "name": "rain",
      "label": "雨列"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "open_review",
      "label": "圈选同秤嫌疑窗",
      "path": "/pulse_groups/open-review",
      "fields": [
        {
          "name": "code",
          "label": "复核组编号",
          "kind": "text",
          "initial": "GROUP-24"
        },
        {
          "name": "windows",
          "label": "嫌疑窗号",
          "kind": "json",
          "initial": [
            "W-PULSE"
          ]
        }
      ],
      "help": "冻结组外同秤基线给各圈选窗判分。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "cancel_review",
      "label": "撤销复核",
      "path": "/pulse_groups/cancel-review",
      "fields": [
        {
          "name": "code",
          "label": "复核组编号",
          "kind": "text",
          "initial": "GROUP-24"
        }
      ],
      "help": "撤销未结复核，同秤旧签条恢复签发。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "issue_review",
      "label": "整组签发有效雨列",
      "path": "/pulse_groups/issue-review",
      "fields": [
        {
          "name": "code",
          "label": "复核组编号",
          "kind": "text",
          "initial": "GROUP-24"
        },
        {
          "name": "rain",
          "label": "雨列号",
          "kind": "text",
          "initial": "RAIN-24"
        }
      ],
      "help": "整组排除与雨列签发一同生效；重复签发不新增雨列。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "pulse_groups";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
