import React from "react";

import Button from "./Button";
import type { TaskStatus } from "../types";

interface TaskCardProps {
  title: string;
  description: string | null | undefined;
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
  onStatusChange: (value: TaskStatus) => void;
  onDelete: () => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  title,
  description,
  status,
  createdAt,
  updatedAt,
  onStatusChange,
  onDelete,
}: TaskCardProps) => {
  return (
    <div className="p-4 flex justify-between items-center bg-white border border-solid border-[#dee2e6] rounded-sm">
      <div className="flex flex-col justify-center items-start gap-2">
        <h4 className="font-sans font-medium text-gray-800 text-base truncate">
          {title}
        </h4>
        {description && (
          <p className="font-sans font-normal text-gray-500 text-base truncate">
            {description}
          </p>
        )}
        <div className="flex justify-start items-center gap-10">
          <small className="font-sans font-normal text-gray-400">
            Created: {new Date(createdAt).toLocaleString()}
          </small>
          <small className="font-sans font-normal text-gray-400">
            Updated: {new Date(updatedAt).toLocaleString()}
          </small>
        </div>
      </div>

      <div className="flex justify-end items-center gap-2">
        <select
          value={status}
          onChange={(e) => onStatusChange(e.target.value as TaskStatus)}
          className="p-1 rounded-sm"
        >
          <option value="TODO">To Do</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="DONE">Done</option>
        </select>

        <Button
          text="Delete"
          onClick={onDelete}
          style="bg-red-500 outline-red-500"
        />
      </div>
    </div>
  );
};

export default TaskCard;
