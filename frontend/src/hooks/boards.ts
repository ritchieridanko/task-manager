import axios from "axios";
import { useCallback, useEffect, useState } from "react";
import toast from "react-hot-toast";

import { boardApi } from "../api";
import { COLORS } from "../constants";
import type { Board, CreateBoardPayload } from "../types";

export const useFetchAllBoards = () => {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchAllBoards = useCallback(async () => {
    setLoading(true);

    try {
      const data: Board[] = await boardApi.getAll();
      setBoards(data);
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
        id: "fab-err-toast",
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
  }, []);

  useEffect(() => {
    fetchAllBoards();
  }, [fetchAllBoards]);

  const append = (board: Board) => {
    setBoards((prev) => [board, ...prev]);
  };

  const remove = (id: string) => {
    setBoards((prev) => prev.filter((b) => b.id !== id));
  };

  return { boards, loading, refetch: fetchAllBoards, append, remove };
};

export const useCreateBoard = () => {
  const [form, setForm] = useState<CreateBoardPayload>({
    name: "",
  });
  const [loading, setLoading] = useState<boolean>(false);

  const createBoard = useCallback(async (payload: CreateBoardPayload) => {
    setLoading(true);

    try {
      const data: Board = await boardApi.create(payload);
      return data;
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
        id: "cb-err-toast",
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
  }, []);

  const clearForm = () => {
    setForm({ name: "" });
  };

  return { form, setForm, clearForm, loading, createBoard };
};

export const useDeleteBoard = () => {
  const [loading, setLoading] = useState<boolean>(false);

  const deleteBoard = useCallback(async (id: string) => {
    setLoading(true);

    try {
      await boardApi.delete(id);
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
        id: "db-err-toast",
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
  }, []);

  return { loading, deleteBoard };
};
