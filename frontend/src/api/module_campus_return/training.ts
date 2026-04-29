import request from "@/utils/request";

const API_BASE = "/campus_return/training";

export interface TrainingCourseItem {
  id?: number;
  batch_id: number;
  course_name: string;
  description?: string;
  content?: string;
  video_url?: string;
  duration: number;
  order: number;
  is_required: boolean;
  is_active: boolean;
  created_time?: string;
}

export interface TrainingCourseForm {
  batch_id: number;
  course_name: string;
  description?: string;
  content?: string;
  video_url?: string;
  duration?: number;
  order?: number;
  is_required?: boolean;
  is_active?: boolean;
}

export const TrainingAPI = {
  listCourses: (batchId?: number) =>
    request.get<TrainingCourseItem[]>(`${API_BASE}/courses`, { params: { batch_id: batchId } }),

  createCourse: (data: TrainingCourseForm) =>
    request.post<{ id: number }>(`${API_BASE}/courses`, data),
};
