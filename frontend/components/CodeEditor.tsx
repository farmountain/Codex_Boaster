import MonacoEditor from "@monaco-editor/react";

export default function CodeEditor({ code, onChange }) {
  return (
    <div className="h-96 border rounded shadow">
      <MonacoEditor
        height="100%"
        defaultLanguage="python"
        value={code}
        onChange={onChange}
        theme="vs-dark"
      />
    </div>
  );
}
