import { client } from "./client";
import type {
  CreateTaskPayload,
  GetAllTasksParams,
  Task,
  UpdateTaskPayload,
} from "../types";

export const taskApi = {
  create: async (
    boardId: string,
    payload: CreateTaskPayload,
  ): Promise<Task> => {
    const res = await client.post<Task>(`/boards/${boardId}/tasks`, payload);
    return res.data;
  },

  getAll: async (
    boardId: string,
    params: GetAllTasksParams,
  ): Promise<Task[]> => {
    const res = await client.get<Task[]>(`/boards/${boardId}/tasks`, {
      params,
    });
    return res.data;
  },

  update: async (id: string, payload: UpdateTaskPayload): Promise<Task> => {
    const res = await client.patch<Task>(`/tasks/${id}`, payload);
    return res.data;
  },

  delete: async (id: string): Promise<void> => {
    await client.delete(`/tasks/${id}`);
  },
};
