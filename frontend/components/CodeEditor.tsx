import Editor from '@monaco-editor/react';

interface Props {
  code: string;
  onChange(value: string): void;
}

export default function CodeEditor({ code, onChange }: Props) {
  return (
    <Editor
      height="400px"
      language="python"
      value={code}
      onChange={(value) => onChange(value || '')}
    />
  );
}
