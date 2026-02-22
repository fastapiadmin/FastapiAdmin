import { Ref, ref } from "vue";

interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: any;
  [key: string]: any;
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: string;
  animated?: boolean;
  style?: any;
  data?: any;
  [key: string]: any;
}

interface EdgeData {
  label: string;
  type: string;
  animated: boolean;
  color: string;
  strokeWidth: number;
  condition?: string;
  description?: string;
}

interface GetNodes {
  (): WorkflowNode[];
}

interface SetNodes {
  (nodes: WorkflowNode[]): void;
}

interface GetEdges {
  (): WorkflowEdge[];
}

interface SetEdges {
  (edges: WorkflowEdge[]): void;
}

interface AddNodes {
  (nodes: WorkflowNode | WorkflowNode[]): void;
}

export function useNodeOperations() {
  const clipboard: Ref<WorkflowNode | null> = ref(null);

  function copyNode(node: WorkflowNode | null): boolean {
    if (node?.id) {
      clipboard.value = JSON.parse(JSON.stringify(node));
      return true;
    }
    return false;
  }

  function pasteNode(addNodes: AddNodes): WorkflowNode | null {
    if (clipboard.value) {
      const newNode: WorkflowNode = {
        ...clipboard.value,
        id: `node-${Date.now()}`,
        position: {
          x: clipboard.value.position.x + 50,
          y: clipboard.value.position.y + 50,
        },
      };
      addNodes(newNode);
      return newNode;
    }
    return null;
  }

  function deleteNode(
    nodeId: string,
    getNodes: GetNodes,
    setNodes: SetNodes,
    getEdges: GetEdges,
    setEdges: SetEdges
  ): boolean {
    if (!nodeId) return false;

    setNodes(getNodes().filter((n) => n.id !== nodeId));
    setEdges(getEdges().filter((e) => e.source !== nodeId && e.target !== nodeId));
    return true;
  }

  function updateNodeData(
    nodeId: string,
    data: any,
    getNodes: GetNodes,
    setNodes: SetNodes
  ): boolean {
    if (!nodeId) return false;

    const allNodes = getNodes();
    const targetNode = allNodes.find((n) => n.id === nodeId);
    if (!targetNode) return false;

    setNodes([
      ...allNodes.filter((n) => n.id !== nodeId),
      {
        ...targetNode,
        data: { ...targetNode.data, ...data },
      },
    ]);
    return true;
  }

  function deleteEdge(edgeId: string, getEdges: GetEdges, setEdges: SetEdges): boolean {
    if (!edgeId) return false;

    setEdges(getEdges().filter((e) => e.id !== edgeId));
    return true;
  }

  function updateEdgeData(
    edgeId: string,
    data: EdgeData,
    getEdges: GetEdges,
    setEdges: SetEdges
  ): boolean {
    if (!edgeId) return false;

    const allEdges = getEdges();
    const targetEdge = allEdges.find((e) => e.id === edgeId);
    if (!targetEdge) return false;

    setEdges([
      ...allEdges.filter((e) => e.id !== edgeId),
      {
        ...targetEdge,
        label: data.label,
        type: data.type,
        animated: data.animated,
        style: {
          stroke: data.color,
          strokeWidth: data.strokeWidth,
        },
        data: {
          condition: data.condition,
          description: data.description,
        },
      },
    ]);
    return true;
  }

  return {
    clipboard,
    copyNode,
    pasteNode,
    deleteNode,
    updateNodeData,
    deleteEdge,
    updateEdgeData,
  };
}
