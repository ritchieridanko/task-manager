import { client } from "./client";
import type { Board, CreateBoardPayload } from "../types";

export const boardApi = {
  create: async (payload: CreateBoardPayload): Promise<Board> => {
    const res = await client.post<Board>("/boards", payload);
    return res.data;
  },

  getAll: async (): Promise<Board[]> => {
    const res = await client.get<Board[]>("/boards");
    return res.data;
  },

  delete: async (id: string): Promise<void> => {
    await client.delete(`/boards/${id}`);
  },
};
