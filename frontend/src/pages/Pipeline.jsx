import React from 'react';
import PipelineView from '../components/PipelineView';

export default function Pipeline() {
  return (
    <div className="pipeline-page">
      <div className="page-header">
        <h1>ML Pipeline Monitor</h1>
        <p>Real-time view of the Airflow data ingestion and training pipeline.</p>
      </div>
      <PipelineView />

      <div className="pipeline-links">
        <h3>External Tools</h3>
        <div className="tool-links">
          <a href="http://localhost:8080" target="_blank" rel="noreferrer" className="tool-link">
            Airflow DAG UI
          </a>
          <a href="http://localhost:5000" target="_blank" rel="noreferrer" className="tool-link">
            MLflow Experiments
          </a>
          <a href="http://localhost:3001" target="_blank" rel="noreferrer" className="tool-link">
            Grafana Dashboard
          </a>
          <a href="http://localhost:9090" target="_blank" rel="noreferrer" className="tool-link">
            Prometheus Metrics
          </a>
        </div>
      </div>
    </div>
  );
}
