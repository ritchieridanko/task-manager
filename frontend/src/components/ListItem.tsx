import React from "react";

interface ListItemProps {
  name: string;
  onClick: () => void;
  onDelete: () => void;
  isSelected: boolean;
}

const ListItem: React.FC<ListItemProps> = ({
  name,
  onClick,
  onDelete,
  isSelected,
}: ListItemProps) => {
  return (
    <li
      className={`
        mb-2 px-2.5 py-1.5 flex justify-between items-center rounded-sm
        cursor-pointer ${isSelected ? "bg-blue-800" : "bg-blue-100"}
      `}
      onClick={onClick}
    >
      <span
        className={`
          font-sans text-base
          ${isSelected ? "font-semibold text-white" : "font-normal text-blue-800"}
        `}
      >
        {name}
      </span>

      <button
        onClick={(e) => {
          e.stopPropagation();
          onDelete();
        }}
        className="px-1.5 bg-red-500 border-none rounded-sm font-extrabold text-xs text-white cursor-pointer"
      >
        ✕
      </button>
    </li>
  );
};

export default ListItem;
