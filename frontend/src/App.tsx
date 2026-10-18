import React, { useState } from "react";
import { Toaster } from "react-hot-toast";

import { Button, ListItem, TextField } from "./components";
import { useCreateBoard, useDeleteBoard, useFetchAllBoards } from "./hooks";
import type { Board } from "./types";

const App: React.FC = () => {
  const [selectedBoard, setSelectedBoard] = useState<Board | null>(null);

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
              onChange={(e) => setCreateBoardForm({ name: e })}
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
      </div>

      <Toaster position="bottom-right" />
    </>
  );
};

export default App;
