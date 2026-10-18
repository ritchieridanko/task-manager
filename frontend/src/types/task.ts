export type TaskStatus = "TODO" | "IN_PROGRESS" | "DONE";

export interface Task {
  id: string;
  board_id: string;
  title: string;
  description?: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}
