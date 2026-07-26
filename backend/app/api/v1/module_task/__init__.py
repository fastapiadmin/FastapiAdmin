from fastapi import APIRouter

from .cronjob.job.controller import JobRouter
from .cronjob.node.controller import NodeRouter
from .workflow.flows.controller import WorkflowRouter
from .workflow.node_type.controller import WorkflowNodeTypeRouter

task_router = APIRouter(prefix="/task")

task_router.include_router(JobRouter)
task_router.include_router(NodeRouter)
task_router.include_router(WorkflowRouter)
task_router.include_router(WorkflowNodeTypeRouter)
