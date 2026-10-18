import React from "react";

interface TextFieldProps {
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
}

const TextField: React.FC<TextFieldProps> = ({
  placeholder,
  value,
  onChange,
}: TextFieldProps) => {
  return (
    <input
      type="text"
      inputMode="text"
      placeholder={placeholder}
      value={value}
      className="
        px-2.5 py-1.5 w-full flex flex-row justify-between items-center rounded-sm
        font-sans font-normal text-gray-800 text-base truncate
        outline-2 outline-blue-800
        placeholder:font-sans placeholder:font-normal placeholder:text-gray-400 placeholder:text-base placeholder:truncate
      "
      onChange={(e) => onChange(e.target.value)}
    />
  );
};

export default TextField;
