import axios from "axios";
import { useCallback, useState } from "react";
import toast from "react-hot-toast";

import { taskApi } from "../api";
import { COLORS } from "../constants";
import type { GetAllTasksParams, Task } from "../types";

export const useFetchAllTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchAllTasks = useCallback(
    async (boardId: string, params: GetAllTasksParams) => {
      setLoading(true);

      try {
        const data: Task[] = await taskApi.getAll(boardId, params);
        setTasks(data);
      } catch (err: unknown) {
        let message: string = "Something went wrong";

        if (axios.isAxiosError(err)) {
          message = err.response?.data?.message || err.message;
        } else if (err instanceof Error) {
          message = err.message;
        } else {
          console.log(err);
        }

        toast.error(message, {
          id: "fat-err-toast",
          duration: 5000,
          style: {
            background: COLORS.ERROR,
            color: COLORS.LIGHT,
          },
          iconTheme: {
            primary: COLORS.LIGHT,
            secondary: COLORS.ERROR,
          },
        });
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const append = (task: Task) => {
    setTasks((prev) => [task, ...prev]);
  };

  const remove = (id: string) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const replace = (task: Task) => {
    setTasks((prev) => prev.map((t) => (t.id === task.id ? task : t)));
  };

  return { tasks, loading, fetchAllTasks, append, remove, replace };
};
