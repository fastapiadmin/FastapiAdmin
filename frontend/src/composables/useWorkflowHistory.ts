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

interface WorkflowState {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
}

export function useWorkflowHistory(maxHistory = 50) {
  const history: Ref<WorkflowState[]> = ref([]);
  const historyIndex: Ref<number> = ref(-1);

  function saveToHistory(nodes: WorkflowNode[], edges: WorkflowEdge[]) {
    const state: WorkflowState = {
      nodes: JSON.parse(JSON.stringify(nodes)),
      edges: JSON.parse(JSON.stringify(edges)),
    };

    if (historyIndex.value < history.value.length - 1) {
      history.value = history.value.slice(0, historyIndex.value + 1);
    }

    history.value.push(state);

    if (history.value.length > maxHistory) {
      history.value.shift();
    } else {
      historyIndex.value++;
    }
  }

  function undo(): WorkflowState | null {
    if (historyIndex.value > 0) {
      historyIndex.value--;
      const state = history.value[historyIndex.value];
      return {
        nodes: JSON.parse(JSON.stringify(state.nodes)),
        edges: JSON.parse(JSON.stringify(state.edges)),
      };
    }
    return null;
  }

  function redo(): WorkflowState | null {
    if (historyIndex.value < history.value.length - 1) {
      historyIndex.value++;
      const state = history.value[historyIndex.value];
      return {
        nodes: JSON.parse(JSON.stringify(state.nodes)),
        edges: JSON.parse(JSON.stringify(state.edges)),
      };
    }
    return null;
  }

  function clear() {
    history.value = [];
    historyIndex.value = -1;
  }

  function canUndo(): boolean {
    return historyIndex.value > 0;
  }

  function canRedo(): boolean {
    return historyIndex.value < history.value.length - 1;
  }

  function getCurrentState(): WorkflowState | null {
    if (historyIndex.value >= 0 && historyIndex.value < history.value.length) {
      return history.value[historyIndex.value];
    }
    return null;
  }

  return {
    history,
    historyIndex,
    saveToHistory,
    undo,
    redo,
    clear,
    canUndo,
    canRedo,
    getCurrentState,
  };
}
