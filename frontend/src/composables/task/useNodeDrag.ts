import { Ref, ref } from "vue";

interface DragItem {
  id: string;
  data: {
    label: string;
    type: string;
    args?: string;
    kwargs?: string;
    nodeId?: number;
    category?: string;
  };
  type: string;
  position: { x: number; y: number };
  class?: string;
}

interface NodeItem {
  id?: number;
  type: string;
  name: string;
  icon?: string;
  color?: string;
  class?: string;
  args?: string;
  kwargs?: string;
}

interface Coordinate {
  x: number;
  y: number;
}

interface ScreenToFlowCoordinate {
  (coordinate: Coordinate): Coordinate;
}

interface OnNodesInitialized {
  (callback: () => void): { off: () => void };
}

interface UpdateNode {
  (nodeId: string, updater: (node: any) => any): void;
}

interface AddNodes {
  (nodes: any): void;
}

export function useNodeDrag() {
  const dragItem: Ref<DragItem | null> = ref(null);

  function onDragStart(event: DragEvent, item: NodeItem) {
    dragItem.value = {
      id: `node-${Date.now()}`,
      data: {
        label: item.name,
        type: item.type,
        args: item.args || "",
        kwargs: item.kwargs || "{}",
        nodeId: item.id,
        category: (item as any).category,
      },
      type: item.type,
      position: { x: 0, y: 0 },
      class: item.class || "light",
    };
  }

  function onDragEnd() {
    dragItem.value = null;
  }

  function onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  function onDrop(
    event: DragEvent,
    screenToFlowCoordinate: ScreenToFlowCoordinate,
    onNodesInitialized: OnNodesInitialized,
    updateNode: UpdateNode,
    addNodes: AddNodes
  ) {
    if (!dragItem.value) return;

    const position = screenToFlowCoordinate({
      x: event.clientX,
      y: event.clientY,
    });

    const newNode = {
      ...dragItem.value,
      position,
    };

    const { off } = onNodesInitialized(() => {
      updateNode(dragItem.value?.id || "", (node: any) => ({
        position: {
          x: node.position.x - node.dimensions.width / 2,
          y: node.position.y - node.dimensions.height / 2,
        },
      }));

      off();
    });

    dragItem.value = null;
    addNodes(newNode);
  }

  return {
    dragItem,
    onDragStart,
    onDragEnd,
    onDragOver,
    onDrop,
  };
}
