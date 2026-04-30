<script setup lang="ts">
import type { PickerViewInstance } from 'wot-design-uni/components/wd-picker-view/types'
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [Number, String],
  },
  data: {
    required: true,
    type: Array as () => OptionType[],
  },
  label: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
})

const emits = defineEmits(['update:modelValue'])

// 定义响应式变量
const selectedValues = ref<number[] | string[]>([])
const pickerColumns = ref<
  Array<Array<{ label: string, value: string | number }>>
>([])

// 监听 modelValue 的变化，更新 selectedValues
watch(
  () => props.modelValue,
  (val) => {
    selectedValues.value = val ? findTreePath(val) : []
  },
)

/**
 * 根据节点值查找路径
 * 示例数据： [{"value":"1","label":"公司","children":[{"value":"2","label":"研发部"}]}]
 * 查找部门ID为2的路径，返回结果：[1, 2]
 */
function findTreePath(value: number | string): number[] | string[] {
  const numberPath: number[] = []
  const stringPath: string[] = []
  const list = props.data

  const find = (value: number | string, list: OptionType[]): boolean => {
    for (const item of list) {
      if (item.value === value) {
        typeof value === 'number'
          ? numberPath.push(value)
          : stringPath.push(value)
        return true
      }
      if (item.children?.length) {
        typeof item.value === 'number'
          ? numberPath.push(item.value)
          : stringPath.push(item.value)
        if (find(value, item.children))
          return true
        typeof item.value === 'number' ? numberPath.pop() : stringPath.pop()
      }
    }
    return false
  }

  find(value, list)
  return typeof value === 'number' ? numberPath : stringPath
}

/**
 * 将树形数据转换为 Picker 所需的 columns 格式
 *
 * @param treeData 树形数据
 * @returns Picker 所需的 columns 格式
 */
function transformTreeToColumns(treeData: OptionType[]): Array<Array<{ label: string, value: string | number }>> {
  const columns: Array<Array<{ label: string, value: string | number }>> = []

  for (let depth = 0; depth <= selectedValues.value.length; depth++) {
    const currentColumn = treeData.map(node => ({
      label: node.label,
      value: node.value,
    }))
    if (!currentColumn.length)
      break

    const selectedId = selectedValues.value[depth]
    if (!currentColumn.some(item => item.value === selectedId)) {
      selectedValues.value[depth] = currentColumn[0]?.value
    }

    columns.push(currentColumn)
    const selectedNode = treeData.find(
      node => node.value === selectedValues.value[depth],
    )
    treeData = selectedNode?.children || []
  }

  return columns
}

// 监听 data 的变化，更新 pickerColumns
watch(
  () => props.data,
  (val) => {
    console.log('监听 data 的变化', val)
    pickerColumns.value = transformTreeToColumns(val)
  },
  {
    immediate: true,
  },
)

/**
 * 处理列的变化，动态更新后续列的数据
 */
function handleColumnChange(
  pickerView: PickerViewInstance,
  value: Record<string, any> | Record<string, any>[],
  columnIndex: number,
  resolve: () => void,
) {
  const selectedValue
    = selectedValues.value[selectedValues.value.length - 1] || undefined
  emits('update:modelValue', selectedValue)

  const item = Array.isArray(value) ? value[columnIndex] : value.value
  updatePickerColumns(pickerView, item.value, columnIndex)
  resolve()
}

/**
 * 动态更新所有后续列的数据
 */
function updatePickerColumns(
  pickerView: PickerViewInstance,
  parentId: string | number,
  columnIndex: number,
) {
  const nextColumnIndex = columnIndex + 1
  const children = findChildren(parentId, props.data)

  if (children.length > 0 && nextColumnIndex < 3) {
    pickerView.setColumnData(nextColumnIndex, children)
    updatePickerColumns(pickerView, children[0].value, nextColumnIndex)
  }
}

/**
 * 根据节点value查找其子节点数据
 */
function findChildren(
  parentId: string | number,
  list: Record<string, any>[],
): Record<string, any>[] {
  for (const item of list) {
    if (item.value === parentId && item.children) {
      return item.children
    }
    if (item.children) {
      const children = findChildren(parentId, item.children)
      if (children.length)
        return children
    }
  }
  return []
}

// 格式化显示选中项（显示最后一个子节点的 label）
function displayFormat(items: any) {
  return items.length > 0 ? items[items.length - 1].label : ''
}
</script>

<template>
  <wd-picker
    v-model="selectedValues"
    :columns="pickerColumns"
    :display-format="displayFormat"
    :column-change="handleColumnChange"
    :label="label"
    :placeholder="pickerColumns.length ? '请选择' : '加载中...'"
    :required="required"
  />
</template>
