import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdminLayout from '../../components/AdminLayout';
import api from '../../services/api';
import { mockDashboardAdmin } from '../../services/mockData';
import './AdminDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

function KPICard({ label, value, sub }) {
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {sub && <div className="kpi-sub">{sub}</div>}
    </div>
  );
}

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [medias, setMedias] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setData(mockDashboardAdmin);
      setMedias(mockDashboardAdmin.performances_medias || []);
    } else {
      api.get('/admin/dashboard/').then(r => setData(r.data));
      api.get('/medias/').then(r => setMedias(r.data.results));
    }
  }, []);

  if (!data || !medias) return (
    <AdminLayout pageTitle="Vue globale">
      <div className="loading-state">Chargement…</div>
    </AdminLayout>
  );

  return (
    <AdminLayout pageTitle="Vue globale">
      <div className="page-eyebrow">ADMINISTRATION</div>
      <h1 className="page-title">Vue d'ensemble globale</h1>

      <div className="kpi-grid" style={{ marginTop: 24 }}>
        <KPICard label="MÉDIAS ACTIFS" value={data.medias_actifs} sub={`sur ${data.medias_total} au total`} />
        <KPICard label="UTILISATEURS ACTIFS" value={data.utilisateurs_total} />
        <KPICard label="GESTIONNAIRES" value={data.gestionnaires_total} />
        <KPICard label="RAPPORTS GÉNÉRÉS" value={data.rapports_generes_total} />
      </div>

      {data.medias_sans_gestionnaire > 0 && (
        <div className="card" style={{ marginTop: 16, padding: 14, borderLeft: '4px solid var(--color-danger)' }}>
          ⚠ {data.medias_sans_gestionnaire} média(s) sans gestionnaire affecté — à signaler au Contrôleur.
        </div>
      )}

      <div className="card" style={{ marginTop: 20 }}>
        <div className="perf-header">
          <div className="chart-title" style={{ margin: 0 }}>Médias enregistrés</div>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/admin/medias')}>
            Gérer les médias →
          </button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>MÉDIA</th>
              <th>TYPE</th>
              <th>GESTIONNAIRE</th>
              <th>STATUT</th>
            </tr>
          </thead>
          <tbody>
            {medias.map(m => (
              <tr key={m.id}>
                <td className="font-medium">{m.nom}</td>
                <td>
                  <span className={`badge badge-${m.type_media}`}>
                    {m.type_media.charAt(0).toUpperCase() + m.type_media.slice(1)}
                  </span>
                </td>
                <td className={m.gestionnaire_nom ? '' : 'text-muted'}>
                  {m.gestionnaire_nom || '—'}
                </td>
                <td>
                  <span className={`badge badge-${m.statut}`}>
                    • {m.statut.charAt(0).toUpperCase() + m.statut.slice(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  );
}