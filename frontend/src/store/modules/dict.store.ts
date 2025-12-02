import { store } from "@/store";
import DictAPI, { DictDataTable } from "@/api/module_system/dict";

export const useDictStore = defineStore("dict", {
  state: () => ({
    dictData: {} as Record<string, DictDataTable[]>,
    isLoaded: false,
  }),
  getters: {
    getDictData(): Record<string, DictDataTable[]> {
      return this.dictData;
    },

    // 获取指定类型的字典数据，确保返回数组
    getDictArray() {
      return (type: string): Array<{ dict_value: string; dict_label: string }> => {
        return (this.dictData[type] || [])
          .filter((item) => item.dict_value !== undefined && item.dict_label !== undefined)
          .map((item) => ({
            dict_value: item.dict_value!,
            dict_label: item.dict_label!,
          }));
      };
    },
  },
  actions: {
    // 批量获取字典数据
    async getDict(types: string[]): Promise<Record<string, DictDataTable[]>> {
      try {
        for (const type of types) {
          if (!this.dictData[type]) {
            const response = await DictAPI.getInitDict(type);
            // 确保数据格式正确
            this.dictData[type] = ((response.data.data as DictDataTable[]) || []).filter(
              (item) => item.dict_value !== undefined && item.dict_label !== undefined
            );
            this.isLoaded = true;
          }
        }
        // 返回请求的字典数据
        return types.reduce(
          (result, type) => {
            result[type] = this.getDictArray(type);
            return result;
          },
          {} as Record<string, DictDataTable[]>
        );
      } catch (error) {
        console.error("获取字典数据失败", error);
        return {};
      }
    },

    getDictLabel(type: string, value: string) {
      const result = this.dictData[type].find((item) => item.dict_value === value);
      if (!result) {
        return value;
      }
      const dict_data = {
        id: result.id,
        dict_value: result.dict_value,
        dict_label: result.dict_label,
        dict_type: result.dict_type,
        css_class: result.css_class,
        list_class: result.list_class,
        is_default: result.is_default,
        dict_sort: result.dict_sort,
        dict_type_id: result.dict_type_id,
        uuid: result.uuid,
        status: result.status,
        description: result.description,
        created_time: result.created_time,
        updated_time: result.updated_time,
      };
      return dict_data;
    },
    clearDictData() {
      this.dictData = {};
    },
  },
  persist: true,
});

export function useDictStoreHook() {
  return useDictStore(store);
}
