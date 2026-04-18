import React, { useEffect, useState } from 'react';
import { getPipelineStatus } from '../api/apiClient';

const TASK_LABELS = {
  data_ingestion: 'Data Ingestion',
  data_validation: 'Data Validation',
  data_cleaning: 'Data Cleaning',
  feature_engineering: 'Feature Engineering',
  encode_and_scale: 'Encode & Scale',
  train_test_split: 'Train / Test Split',
  trigger_training: 'Trigger Training',
};

export default function PipelineView() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPipelineStatus()
      .then(setStatus)
      .catch(() => setError('Could not connect to pipeline. Is the backend running?'));
  }, []);

  if (error) return <div className="error-msg">{error}</div>;
  if (!status) return <div className="loader-text">Loading pipeline status...</div>;

  return (
    <div className="pipeline-view">
      <div className="pipeline-header">
        <span>Status:</span>
        <span className="status-badge">{status.status.toUpperCase()}</span>
        <span className="pipeline-last-run">Last run: {status.last_run}</span>
      </div>

      <div className="pipeline-flow">
        {Object.entries(status.tasks).map(([key, taskStatus], idx) => (
          <React.Fragment key={key}>
            <div className={`task-node ${taskStatus}`}>
              <div className="task-icon">{taskStatus === 'success' ? '✅' : '❌'}</div>
              <div className="task-label">{TASK_LABELS[key] || key}</div>
              <div className="task-status-text">{taskStatus}</div>
            </div>
            {idx < Object.keys(status.tasks).length - 1 && (
              <div className="pipeline-arrow">→</div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
