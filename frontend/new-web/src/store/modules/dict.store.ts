/**
 * 字典状态管理模块
 *
 * 提供数据字典的状态管理和缓存机制
 *
 * ## 主要功能
 *
 * - 字典数据缓存和管理
 * - 批量获取字典数据
 * - 字典标签查找
 * - 字典数据清空
 *
 * ## 使用场景
 *
 * - 表单下拉选择框数据填充
 * - 表格列数据格式化显示
 * - 状态字段标签转换
 * - 动态表单配置
 *
 * ## 核心特性
 *
 * - 自动去重缓存
 * - 按需加载字典
 * - 统一的数据格式
 * - 支持批量获取
 *
 * ## 持久化
 *
 * - 使用 localStorage 存储
 * - 缓存已加载的字典数据
 * - 减少重复请求
 *
 * @module store/modules/dict.store
 * @author FastapiAdmin Team
 */
import { store } from "@/store";
import DictAPI, { DictDataTable } from "@/api/module_system/dict";
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useDictStore = defineStore(
  "dictStore",
  () => {
    // 字典数据
    const dictData = ref<Record<string, DictDataTable[]>>({});
    // 是否已加载
    const isLoaded = ref(false);

    /**
     * 获取所有字典数据
     */
    const getDictData = computed(() => dictData.value);

    /**
     * 获取指定类型的字典数据，确保返回数组
     */
    const getDictArray = (type: string): Array<{ dict_value: string; dict_label: string }> => {
      return (dictData.value[type] || [])
        .filter((item) => item.dict_value !== undefined && item.dict_label !== undefined)
        .map((item) => ({
          dict_value: item.dict_value!,
          dict_label: item.dict_label!,
        }));
    };

    /**
     * 批量获取字典数据
     * @param types 字典类型数组
     * @returns 指定类型的字典数据
     */
    async function getDict(types: string[]): Promise<Record<string, DictDataTable[]>> {
      try {
        for (const type of types) {
          if (!dictData.value[type]) {
            const response = await DictAPI.getInitDict(type);
            // 确保数据格式正确
            dictData.value[type] = ((response.data.data as DictDataTable[]) || []).filter(
              (item) => item.dict_value !== undefined && item.dict_label !== undefined
            );
            isLoaded.value = true;
          }
        }
        // 返回请求的字典数据
        return types.reduce(
          (result, type) => {
            result[type] = getDictArray(type);
            return result;
          },
          {} as Record<string, DictDataTable[]>
        );
      } catch (error) {
        console.error("获取字典数据失败", error);
        return {};
      }
    }

    /**
     * 根据类型和值获取字典标签
     * @param type 字典类型
     * @param value 字典值
     * @returns 字典标签对象或原值
     */
    function getDictLabel(type: string, value: string) {
      const result = dictData.value[type]?.find((item) => item.dict_value === value);
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
    }

    /**
     * 清空字典数据
     */
    function clearDictData() {
      dictData.value = {};
    }

    return {
      dictData,
      isLoaded,
      getDictData,
      getDictArray,
      getDict,
      getDictLabel,
      clearDictData,
    };
  },
  {
    persist: true,
  }
);

export function useDictStoreHook() {
  return useDictStore(store);
}
