import React from "react";

interface ButtonProps {
  text: string;
  onClick: () => void;
  style?: string;
}

const Button: React.FC<ButtonProps> = ({
  text,
  onClick,
  style,
}: ButtonProps) => {
  return (
    <button
      className={`
        px-2.5 py-1.5 w-full flex justify-center items-center
        bg-blue-800 rounded-sm outline-2 outline-blue-800
        cursor-pointer

        ${style}
      `}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
    >
      <p className="font-sans font-medium text-white text-base">{text}</p>
    </button>
  );
};

export default Button;
