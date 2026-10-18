import React, { useEffect, useState } from "react";
import { Toaster } from "react-hot-toast";

import { Button, ListItem, TaskCard, TextField } from "./components";
import {
  useCreateBoard,
  useCreateTask,
  useDeleteBoard,
  useDeleteTask,
  useFetchAllBoards,
  useFetchAllTasks,
  useUpdateTask,
} from "./hooks";
import type { Board, Task, TaskStatus } from "./types";

const App: React.FC = () => {
  const [selectedBoard, setSelectedBoard] = useState<Board | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("");

  const {
    boards,
    loading: loadingBoards,
    append: appendBoard,
    remove: removeBoard,
  } = useFetchAllBoards();
  const {
    form: createBoardForm,
    setForm: setCreateBoardForm,
    clearForm: clearCreateBoardForm,
    createBoard,
  } = useCreateBoard();
  const { deleteBoard } = useDeleteBoard();

  const {
    tasks,
    loading: loadingTasks,
    fetchAllTasks,
    append: appendTask,
    remove: removeTask,
    replace: replaceTask,
  } = useFetchAllTasks();
  const {
    form: createTaskForm,
    setForm: setCreateTaskForm,
    clearForm: clearCreateTaskForm,
    createTask,
  } = useCreateTask();
  const { clearForm: clearUpdateTaskForm, updateTask } = useUpdateTask();
  const { deleteTask } = useDeleteTask();

  useEffect(() => {
    if (selectedBoard) {
      fetchAllTasks(selectedBoard.id, {
        status: statusFilter !== "" ? (statusFilter as TaskStatus) : undefined,
      });
    }
  }, [selectedBoard, statusFilter]);

  const handleCreateBoard = async () => {
    const data: Board | undefined = await createBoard(createBoardForm);
    if (data) {
      appendBoard(data);
    }

    clearCreateBoardForm();
  };

  const handleDeleteBoard = async (id: string) => {
    await deleteBoard(id);

    removeBoard(id);
  };

  const handleCreateTask = async (boardId: string) => {
    const data: Task | undefined = await createTask(boardId, createTaskForm);
    if (data) {
      appendTask(data);
    }

    clearCreateTaskForm();
  };

  const handleStatusChange = async (id: string, status: TaskStatus) => {
    const data: Task | undefined = await updateTask(id, { status: status });
    if (data) {
      replaceTask(data);
    }

    clearUpdateTaskForm();
  };

  const handleDeleteTask = async (id: string) => {
    await deleteTask(id);

    removeTask(id);
  };

  return (
    <>
      <div className="flex h-screen bg-white">
        {/* Sidebar: Boards */}
        <div className="p-5 w-80 flex flex-col gap-5 bg-white border-r border-solid border-[#dee2e6]">
          <h2 className="font-sans font-semibold text-blue-800 text-xl">
            Task Manager
          </h2>

          <div className="flex flex-col justify-start items-center gap-3">
            <TextField
              placeholder="New board name..."
              value={createBoardForm.name}
              onChange={(e) =>
                setCreateBoardForm({ ...createBoardForm, name: e })
              }
            />
            <Button text="Add New Board" onClick={handleCreateBoard} />
          </div>

          {loadingBoards ? (
            <div className="h-full w-full flex justify-center items-center">
              <p className="font-sans font-normal text-gray-800 text-base">
                Loading boards...
              </p>
            </div>
          ) : boards.length === 0 ? (
            <div className="h-full w-full flex justify-center items-center">
              <p className="font-sans font-normal text-gray-400 text-base italic">
                No boards yet on this task manager.
              </p>
            </div>
          ) : (
            <ul className="flex-1 list-none overflow-y-auto">
              {boards.map((board) => (
                <ListItem
                  key={board.id}
                  name={board.name}
                  onClick={() => setSelectedBoard(board)}
                  onDelete={() => handleDeleteBoard(board.id)}
                  isSelected={selectedBoard?.id === board.id}
                />
              ))}
            </ul>
          )}
        </div>

        {/* Main Content: Tasks */}
        <div className="px-10 py-5 flex-1 bg-[#f8f9fa] overflow-y-auto">
          {selectedBoard ? (
            <div className="flex flex-col justify-start gap-5">
              <div className="flex justify-between items-center gap-2">
                <h1 className="font-sans font-semibold text-gray-800 text-xl truncate">
                  {selectedBoard.name.toUpperCase()}
                </h1>

                <div className="flex justify-end items-center gap-2">
                  <label className="font-sans font-normal text-gray-800 text-base whitespace-nowrap">
                    Filter Status:
                  </label>

                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <option value="">(None)</option>
                    <option value="TODO">To Do</option>
                    <option value="IN_PROGRESS">In Progress</option>
                    <option value="DONE">Done</option>
                  </select>
                </div>
              </div>

              <div className="flex flex-col justify-start gap-3">
                <h3 className="font-sans font-normal text-gray-800 text-base">
                  Create Task
                </h3>

                <TextField
                  placeholder="New task title..."
                  value={createTaskForm.title}
                  onChange={(e) =>
                    setCreateTaskForm({ ...createTaskForm, title: e })
                  }
                />
                <div className="flex justify-between items-center gap-3">
                  <div className="flex-5">
                    <TextField
                      placeholder="Description (optional)"
                      value={createTaskForm.description ?? ""}
                      onChange={(e) =>
                        setCreateTaskForm({
                          ...createTaskForm,
                          description: e === "" ? undefined : e,
                        })
                      }
                    />
                  </div>
                  <div className="flex-1">
                    <Button
                      text="Add Task"
                      onClick={() => handleCreateTask(selectedBoard.id)}
                    />
                  </div>
                </div>
              </div>

              {loadingTasks ? (
                <div className="h-full w-full flex justify-center items-center">
                  <p className="font-sans font-normal text-gray-800 text-base">
                    Loading tasks...
                  </p>
                </div>
              ) : tasks.length === 0 ? (
                <div className="h-full w-full flex justify-center items-center">
                  <p className="font-sans font-normal text-gray-400 text-base italic">
                    No tasks yet on this board.
                  </p>
                </div>
              ) : (
                <div className="flex flex-col gap-2">
                  {tasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      title={task.title}
                      description={task.description}
                      status={task.status}
                      createdAt={task.created_at}
                      updatedAt={task.updated_at}
                      onStatusChange={(e) => handleStatusChange(task.id, e)}
                      onDelete={() => handleDeleteTask(task.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="h-full w-full flex justify-center items-center">
              <p className="font-sans font-normal text-gray-800 text-base">
                Select a board to view tasks.
              </p>
            </div>
          )}
        </div>
      </div>

      <Toaster position="bottom-right" />
    </>
  );
};

export default App;
