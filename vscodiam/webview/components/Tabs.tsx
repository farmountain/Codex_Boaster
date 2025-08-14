import React, { useEffect, useRef, useState } from 'react';
import { MCPClient } from '../lib/mcpClient';

const tabNames = ['Plan', 'Runs', 'Diff', 'Eval', 'Settings'];

export const Tabs: React.FC = () => {
  const [active, setActive] = useState('Plan');
  const vscodeRef = useRef<any>();
  const clientRef = useRef(new MCPClient('http://localhost:3000'));

  useEffect(() => {
    vscodeRef.current = (window as any).acquireVsCodeApi?.();
    const listener = (event: MessageEvent) => {
      // handle messages from extension
      console.log('message', event.data);
    };
    window.addEventListener('message', listener);
    return () => window.removeEventListener('message', listener);
  }, []);

  const postMessage = (type: string, payload: any) => {
    vscodeRef.current?.postMessage({ type, payload });
  };

  const handleLogin = async () => {
    try {
      const result = await clientRef.current.login('user', 'pass');
      postMessage('login', { token: result.token });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div className="flex space-x-2 border-b">
        {tabNames.map((t) => (
          <button
            key={t}
            className={`px-3 py-2 ${active === t ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => setActive(t)}
          >
            {t}
          </button>
        ))}
      </div>
      <div className="p-4">
        {active === 'Settings' && (
          <button
            className="bg-blue-500 text-white px-4 py-2"
            onClick={handleLogin}
          >
            Login
          </button>
        )}
        <div className="mt-4">{active} content</div>
      </div>
    </div>
  );
};
