import type { TaskStatus } from "./task";

export interface CreateBoardPayload {
  name: string;
}

export interface CreateTaskPayload {
  title: string;
  description?: string;
  status?: TaskStatus;
}

export interface GetAllTasksParams {
  status?: TaskStatus;
}

export interface UpdateTaskPayload {
  title?: string;
  description?: string;
  status?: TaskStatus;
}
