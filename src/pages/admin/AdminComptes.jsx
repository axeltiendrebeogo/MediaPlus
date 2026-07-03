import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import api from '../../services/api';
import { mockUsers } from '../../services/mockData';
import ModalCreerCompte from './modals/ModalCreerCompte';
import './AdminComptes.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const ROLE_LABELS = { admin: 'Admin', gestionnaire: 'Gestionnaire', controleur: 'Contrôleur' };

export default function AdminComptes() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreer, setShowCreer] = useState(false);
  const [filterRole, setFilterRole] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        setUsers(mockUsers.results);
      } else {
        const params = filterRole ? { role: filterRole } : {};
        const res = await api.get('/users/', { params });
        setUsers(res.data.results);
      }
    } finally {
      setLoading(false);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [filterRole]);

  const handleToggleActive = async (user) => {
    if (USE_MOCK) {
      setUsers(prev => prev.map(u => u.id === user.id ? { ...u, is_active: !u.is_active } : u));
      return;
    }
    try {
      await api.patch(`/users/${user.id}/`, { is_active: !user.is_active });
      setUsers(prev => prev.map(u => u.id === user.id ? { ...u, is_active: !u.is_active } : u));
    } catch {}
  };

  const handleDelete = async (user) => {
    if (!window.confirm(`Supprimer le compte de ${user.nom} ? Cette action est irréversible.`)) return;
    if (USE_MOCK) {
      setUsers(prev => prev.filter(u => u.id !== user.id));
      return;
    }
    try {
      await api.delete(`/users/${user.id}/`);
      setUsers(prev => prev.filter(u => u.id !== user.id));
    } catch {}
  };

  const handleCreated = (u) => {
    setUsers(prev => [u, ...prev]);
    setShowCreer(false);
  };

  const filtered = filterRole ? users.filter(u => u.role === filterRole) : users;

  const formatDate = d => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });

  return (
    <AdminLayout pageTitle="Comptes">
      <div className="page-header-row">
        <div>
          <div className="page-eyebrow">ADMINISTRATION</div>
          <h1 className="page-title">Comptes utilisateurs</h1>
          <p className="page-subtitle">{users.length} compte{users.length > 1 ? 's' : ''} enregistré{users.length > 1 ? 's' : ''}</p>
        </div>
        <button className="btn btn-secondary" onClick={() => setShowCreer(true)}>
          + Créer un compte
        </button>
      </div>

      {/* Filters */}
      <div className="comptes-filters">
        {['', 'gestionnaire', 'controleur', 'admin'].map(r => (
          <button
            key={r}
            className={`filter-tab${filterRole === r ? ' active' : ''}`}
            onClick={() => setFilterRole(r)}
          >
            {r === '' ? 'Tous' : ROLE_LABELS[r]}
          </button>
        ))}
      </div>

      {/* Table */}
      {loading ? (
        <div className="loading-state">Chargement…</div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table className="table">
            <thead>
              <tr>
                <th>NOM</th>
                <th>RÔLE</th>
                <th>MÉDIA AFFECTÉ</th>
                <th>CRÉÉ LE</th>
                <th>STATUT</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(u => (
                <tr key={u.id}>
                  <td>
                    <div className="user-name">{u.nom}</div>
                    <div className="user-email">{u.email}</div>
                  </td>
                  <td>
                    <span className={`badge role-badge-${u.role}`}>
                      {ROLE_LABELS[u.role]}
                    </span>
                  </td>
                  <td className={u.media_nom ? '' : 'text-muted'}>
                    {u.media_nom || '—'}
                  </td>
                  <td className="text-muted">{formatDate(u.date_creation)}</td>
                  <td>
                    <span className={`badge ${u.is_active ? 'badge-actif' : 'badge-inactif'}`}>
                      • {u.is_active ? 'Actif' : 'Inactif'}
                    </span>
                  </td>
                  <td>
                    <div className="action-btns">
                      <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => handleToggleActive(u)}
                      >
                        {u.is_active ? 'Désactiver' : 'Activer'}
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(u)}
                      >
                        Supprimer
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filtered.length === 0 && (
            <div className="empty-state">Aucun compte trouvé.</div>
          )}
        </div>
      )}

      {showCreer && (
        <ModalCreerCompte
          onClose={() => setShowCreer(false)}
          onCreated={handleCreated}
        />
      )}
    </AdminLayout>
  );
}
