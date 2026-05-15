/**
 * 全局组件 / API 类型声明（手动维护，不会被 unplugin 覆盖）
 * 仅用于 <script> 中通过 typeof / h() 等方式引用的组件和 API
 * 模板中使用的组件由 unplugin-vue-components 自动注册，无需在此声明
 */
export {};

declare global {
  // ─── Fa 组件 ───
  const FaButtonTable: (typeof import("./../components/forms/fa-button-table/index.vue"))["default"];
  const FaForm: (typeof import("./../components/forms/fa-form/index.vue"))["default"];
  const FaSearchBar: (typeof import("./../components/forms/fa-search-bar/index.vue"))["default"];
  const FaSearchBarWithAudit: (typeof import("./../components/forms/fa-search-bar/FaSearchBarWithAudit.vue"))["default"];

  // ─── 自定义组件 ───
  const JsonPretty: (typeof import("./../components/others/fa-json-pretty/index.vue"))["default"];
  const CopyButton: (typeof import("./../components/others/fa-copy-button/index.vue"))["default"];
  const MenuRouteIcon: (typeof import("./../components/others/fa-menu-routeIcon/index.vue"))["default"];

  // ─── Element Plus 组件（在 <script> 中通过 h() 使用） ───
  const ElTag: (typeof import("element-plus/es"))["ElTag"];
  const ElTooltip: (typeof import("element-plus/es"))["ElTooltip"];
  const ElDropdown: (typeof import("element-plus/es"))["ElDropdown"];
  const ElDropdownMenu: (typeof import("element-plus/es"))["ElDropdownMenu"];
  const ElDropdownItem: (typeof import("element-plus/es"))["ElDropdownItem"];

  // ─── Element Plus API ───
  const ElMessageBox: (typeof import("element-plus/es"))["ElMessageBox"];
}
