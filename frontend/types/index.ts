export interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  context: Record<string, any>;
}

export interface PerformanceMetric {
  timestamp: string;
  component: string;
  metric: string;
  value: number;
  message: string;
}

export interface AuditEntry {
  timestamp: string;
  user: string;
  action: string;
  resource: string;
  status: string;
  message: string;
}
