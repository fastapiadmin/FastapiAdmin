<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <div class="logo-section">
        <el-icon class="logo-icon" :size="28"><ChatDotRound /></el-icon>
        <span v-if="!isCollapsed" class="project-name">FA智能助手</span>
      </div>
    </div>

    <div class="sidebar-content">
      <template v-if="!isCollapsed">
        <div class="new-session-section">
          <el-button type="primary" class="new-session-btn" @click="handleNewSession">
            <el-icon class="btn-icon"><Plus /></el-icon>
            <span>开启新对话</span>
          </el-button>
        </div>

        <div class="history-section">
          <div class="search-section">
            <el-input
              v-model="searchQuery"
              placeholder="搜索会话历史"
              :prefix-icon="Search"
              clearable
              @input="handleSearch"
            />
          </div>
          <div class="history-groups">
            <div v-for="group in groupedSessions" :key="group.title" class="history-group">
              <div class="group-title" @click="toggleGroup(group.title)">
                <span>{{ group.title }}</span>
                <el-icon
                  class="collapse-icon"
                  :class="{ collapsed: collapsedGroups.has(group.title) }"
                >
                  <ArrowDown />
                </el-icon>
              </div>
              <div v-show="!collapsedGroups.has(group.title)" class="session-list">
                <div
                  v-for="session in group.sessions"
                  :key="session.id"
                  class="session-item"
                  :class="{ active: currentSessionId === session.id }"
                  @click="handleSelectSession(session)"
                >
                  <el-icon class="session-icon"><ChatLineRound /></el-icon>
                  <span class="session-title">{{ session.title }}</span>
                  <el-dropdown
                    trigger="click"
                    @command="(cmd) => handleSessionCommand(cmd, session)"
                  >
                    <el-icon class="more-icon" @click.stop><MoreFilled /></el-icon>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="rename">重命名</el-dropdown-item>
                        <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </div>
            <div v-if="filteredSessions.length === 0" class="empty-state">
              <el-empty description="暂无会话历史" :image-size="60" />
            </div>
          </div>
        </div>
      </template>
    </div>

    <div class="sidebar-footer">
      <div v-if="!isCollapsed" class="user-info">
        <el-avatar :size="32" :src="userInfo.avatar">
          <el-icon><User /></el-icon>
        </el-avatar>
        <div class="user-details">
          <div class="user-name">{{ userInfo.name }}</div>
          <div class="user-status">在线</div>
        </div>
        <el-dropdown trigger="click" @command="handleUserCommand">
          <el-icon class="user-menu-icon"><Setting /></el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      <div v-else class="collapsed-user">
        <el-dropdown trigger="click" @command="handleUserCommand">
          <el-avatar :size="32" :src="userInfo.avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  ChatLineRound,
  User,
  Setting,
  MoreFilled,
  Plus,
  Search,
  ArrowDown,
} from "@element-plus/icons-vue";
import { useUserStoreHook } from "@/store";
import AiAPI, { ChatSession, SessionGroup, UserInfo } from "@/api/module_ai/chat_session";

interface Props {
  currentSessionId?: number | null;
  isCollapsed?: boolean;
}

interface Emits {
  (e: "select-session", session: ChatSession): void;
  (e: "new-session"): void;
}

const { currentSessionId, isCollapsed = false } = defineProps<Props>();
const emit = defineEmits<Emits>();

const router = useRouter();
const userStore = useUserStoreHook();

const sessions = ref<ChatSession[]>([]);
const searchQuery = ref("");
const collapsedGroups = ref<Set<string>>(new Set());

const userInfo = computed<UserInfo>(() => ({
  id: userStore.basicInfo.id || 0,
  name: userStore.basicInfo.name || "用户",
  username: userStore.basicInfo.username || "",
  avatar: userStore.basicInfo.avatar || "",
  email: userStore.basicInfo.email || "",
}));

const filteredSessions = computed<ChatSession[]>(() => {
  if (!searchQuery.value.trim()) {
    return sessions.value;
  }
  const query = searchQuery.value.toLowerCase();
  return sessions.value.filter((session) => session.title.toLowerCase().includes(query));
});

const groupedSessions = computed<SessionGroup[]>(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayStart = today.getTime();
  const yesterdayStart = todayStart - 24 * 60 * 60 * 1000;
  const weekAgo = todayStart - 7 * 24 * 60 * 60 * 1000;

  const todaySessions: ChatSession[] = [];
  const yesterdaySessions: ChatSession[] = [];
  const weekSessions: ChatSession[] = [];
  const earlierSessions: ChatSession[] = [];

  filteredSessions.value.forEach((session) => {
    const updatedTime = new Date(session.updated_time).getTime();

    if (updatedTime >= todayStart) {
      todaySessions.push(session);
    } else if (updatedTime >= yesterdayStart) {
      yesterdaySessions.push(session);
    } else if (updatedTime >= weekAgo) {
      weekSessions.push(session);
    } else {
      earlierSessions.push(session);
    }
  });

  const groups: SessionGroup[] = [];

  if (todaySessions.length > 0) {
    groups.push({ title: "今天", sessions: todaySessions });
  }

  if (yesterdaySessions.length > 0) {
    groups.push({ title: "昨天", sessions: yesterdaySessions });
  }

  if (weekSessions.length > 0) {
    groups.push({ title: "本周", sessions: weekSessions });
  }

  if (earlierSessions.length > 0) {
    groups.push({ title: "更早", sessions: earlierSessions });
  }

  return groups;
});

const handleSearch = () => {};

const toggleGroup = (groupTitle: string) => {
  const newCollapsed = new Set(collapsedGroups.value);
  if (newCollapsed.has(groupTitle)) {
    newCollapsed.delete(groupTitle);
  } else {
    newCollapsed.add(groupTitle);
  }
  collapsedGroups.value = newCollapsed;
};

const handleSelectSession = (session: ChatSession) => {
  emit("select-session", session);
};

const handleNewSession = () => {
  emit("new-session");
};

const handleSessionCommand = async (command: string, session: ChatSession) => {
  if (command === "rename") {
    try {
      const { value } = await ElMessageBox.prompt("请输入新的会话名称", "重命名", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /.+/,
        inputErrorMessage: "会话名称不能为空",
      });
      await AiAPI.updateSession(session.id, { title: value });
      session.title = value;
      ElMessage.success("重命名成功");
    } catch (error) {
      if (error !== "cancel") {
        ElMessage.error("重命名失败");
      } else {
        ElMessage.info("已取消重命名");
      }
    }
  } else if (command === "delete") {
    try {
      await ElMessageBox.confirm("确定要删除此会话吗？", "确认删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      });
      await AiAPI.deleteSession([session.id]);
      const index = sessions.value.findIndex((s) => s.id === session.id);
      if (index > -1) {
        sessions.value.splice(index, 1);
      }
      ElMessage.success("删除成功");
    } catch (error) {
      if (error !== "cancel") {
        ElMessage.error("删除失败");
      } else {
        ElMessage.info("已取消删除");
      }
    }
  }
};

const handleUserCommand = (command: string) => {
  if (command === "profile") {
    router.push("/profile");
  } else if (command === "settings") {
    ElMessage.info("设置功能开发中");
  } else if (command === "logout") {
    userStore.logout();
    router.push("/login");
  }
};

const loadSessions = async () => {
  try {
    const res = await AiAPI.listSession({ page_no: 1, page_size: 100 });
    if (res.data?.code === 0 || res.data?.success === true) {
      sessions.value = (res.data.data?.items || [])
        .filter((item: any) => item.id !== undefined)
        .map((item: any) => ({
          id: item.id,
          title: item.title,
          created_time: item.created_time,
          updated_time: item.updated_time,
          message_count: 0,
        }));
    }
  } catch (error) {
    console.error("加载会话列表失败:", error);
  }
};

onMounted(() => {
  loadSessions();
});

defineExpose({
  loadSessions,
});
</script>

<style lang="scss" scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid var(--el-border-color-light);
  transition: width 0.3s ease;

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;

    .logo-section {
      display: flex;
      gap: 12px;
      align-items: center;

      .logo-icon {
        color: var(--el-color-primary);
      }

      .project-name {
        font-size: 16px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
    }
  }

  .sidebar-content {
    flex: 1;
    padding: 16px;
    overflow-y: auto;

    .new-session-section {
      margin-bottom: 16px;

      .new-session-btn {
        display: flex;
        gap: 8px;
        align-items: center;
        justify-content: center;
        width: 100%;
        border-radius: 20px;
        transition: all 0.2s ease;

        .btn-icon {
          font-size: 16px;
        }

        &:hover {
          box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
          transform: translateY(-1px);
        }

        &:active {
          transform: translateY(0);
        }
      }
    }

    .history-section {
      .search-section {
        margin-bottom: 16px;

        :deep(.el-input__wrapper) {
          border-radius: 20px;
          box-shadow: 0 0 0 1px var(--el-border-color) inset;
          transition: all 0.2s ease;

          &:hover {
            box-shadow: 0 0 0 1px var(--el-color-primary) inset;
          }

          &.is-focus {
            box-shadow: 0 0 0 1px var(--el-color-primary) inset;
          }
        }

        :deep(.el-input__inner) {
          font-size: 13px;
        }
      }

      .history-groups {
        .history-group {
          margin-bottom: 24px;

          &:last-child {
            margin-bottom: 0;
          }

          .group-title {
            display: flex;
            gap: 6px;
            align-items: center;
            justify-content: space-between;
            padding: 0 4px;
            margin-bottom: 10px;
            font-size: 12px;
            font-weight: 500;
            color: var(--el-text-color-secondary);
            cursor: pointer;
            user-select: none;
            transition: color 0.2s;

            &::before {
              width: 3px;
              height: 12px;
              content: "";
              background: var(--el-color-primary);
              border-radius: 2px;
            }

            &:hover {
              color: var(--el-text-color-primary);
            }

            .collapse-icon {
              font-size: 14px;
              transition: transform 0.2s ease;

              &.collapsed {
                transform: rotate(-90deg);
              }
            }
          }

          .session-list {
            .session-item {
              position: relative;
              display: flex;
              gap: 10px;
              align-items: center;
              padding: 4px;
              margin-bottom: 6px;
              cursor: pointer;
              border: 1px solid transparent;
              border-radius: 14px;
              transition: all 0.2s ease;

              &:hover {
                background: var(--el-fill-color-light);
                border-color: var(--el-border-color-light);
                transform: translateX(2px);
              }

              &.active {
                color: var(--el-color-primary);
                background: var(--el-color-primary-light-9);
                border-color: var(--el-color-primary-light-7);
                box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
              }

              .session-icon {
                flex-shrink: 0;
                font-size: 18px;
                color: var(--el-text-color-secondary);
                transition: color 0.2s;
              }

              &.active .session-icon {
                color: var(--el-color-primary);
              }

              .session-title {
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 14px;
                font-weight: 400;
                white-space: nowrap;
                transition: font-weight 0.2s;
              }

              &.active .session-title {
                font-weight: 500;
              }

              .more-icon {
                flex-shrink: 0;
                padding: 4px;
                font-size: 16px;
                border-radius: 4px;
                opacity: 0;
                transition: all 0.2s;

                &:hover {
                  color: var(--el-color-primary);
                  background: var(--el-fill-color);
                }
              }

              &:hover .more-icon {
                opacity: 1;
              }
            }
          }
        }

        .empty-state {
          display: flex;
          flex-direction: column;
          gap: 8px;
          align-items: center;
          justify-content: center;
          padding: 40px 20px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }

  .sidebar-footer {
    padding: 12px;
    border-top: 1px solid var(--el-border-color-light);

    .user-info {
      display: flex;
      gap: 12px;
      align-items: center;

      .user-details {
        flex: 1;
        overflow: hidden;

        .user-name {
          overflow: hidden;
          text-overflow: ellipsis;
          font-size: 14px;
          font-weight: 500;
          color: var(--el-text-color-primary);
          white-space: nowrap;
        }

        .user-status {
          font-size: 12px;
          color: var(--el-color-success);
        }
      }

      .user-menu-icon {
        font-size: 18px;
        color: var(--el-text-color-secondary);
        cursor: pointer;

        &:hover {
          color: var(--el-color-primary);
        }
      }
    }

    .collapsed-user {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
