import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import { createMemoryHistory, createRouter } from "vue-router";
import { beforeAll, describe, expect, it, vi } from "vitest";

let FaTable: any;

beforeAll(async () => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }),
  });
  FaTable = (await import("@/components/tables/fa-table/index.vue")).default;
}, 30_000);

const i18n = createI18n({
  legacy: false,
  locale: "zh",
  messages: {
    zh: {
      common: {
        loadFailed: "加载失败",
        retry: "重试",
        noData: "暂无数据",
        selectAll: "全选",
      },
    },
  },
});

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: "/", component: { template: "<div />" } }],
});

const EmptyStateStub = {
  props: ["title", "description"],
  template:
    '<div class="empty-state"><span>{{ title }}</span><span>{{ description }}</span><slot /></div>',
};

const ButtonStub = {
  emits: ["click"],
  template: '<button type="button" @click="$emit(\'click\')"><slot /></button>',
};

function mountTable(error: { code: string; message: string } | null) {
  return mount(FaTable, {
    props: {
      data: [],
      loading: false,
      error,
    },
    global: {
      plugins: [i18n, createPinia(), router],
      directives: { loading: {} },
      stubs: {
        FaEmptyState: EmptyStateStub,
        ElButton: ButtonStub,
        ElSkeleton: true,
        ElSkeletonItem: true,
        ElTable: { template: '<div><slot name="empty" /></div>' },
        ElTableColumn: true,
        ElCheckbox: true,
        FaPagination: true,
        VueDraggable: { template: "<div><slot /></div>" },
      },
    },
  });
}

describe("FaTable 错误态", () => {
  it("展示错误原因并触发 retry", async () => {
    const wrapper = mountTable({ code: "NETWORK", message: "网络连接失败" });

    expect(wrapper.text()).toContain("加载失败");
    expect(wrapper.text()).toContain("网络连接失败");

    await wrapper.get("button").trigger("click");
    expect(wrapper.emitted("retry")).toHaveLength(1);
  });

  it("无错误时展示空状态而不是错误态", () => {
    const wrapper = mountTable(null);
    expect(wrapper.text()).toContain("暂无数据");
    expect(wrapper.text()).not.toContain("加载失败");
  });
});
