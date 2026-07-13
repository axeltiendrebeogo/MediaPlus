import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './GestionnaireLayout.css';

// Navigation de la sidebar (cf. maquette "Sidebars des 3 rôles")
const NAV = [
  { label: 'Dashboard',   path: '/gestionnaire',        group: 'MON MÉDIA', end: true },
  { label: 'Pages web',   path: '/gestionnaire/pages',  group: null },
  { label: 'Audio / Vidéo', path: '/gestionnaire/audio', group: 'CONTENU' },
  { label: 'Mes rapports', path: '/gestionnaire/rapports', group: 'RAPPORTS' },
];

export default function GestionnaireLayout({ children, pageTitle }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => { await logout(); navigate('/connexion'); };

  const initials = user?.nom
    ? user.nom.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : 'GE';

  let lastGroup = null;

  return (
    <div className="admin-layout">
      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-name">FasoMedia Insights</span>
          <span className="brand-sub">Analyse d'audience</span>
        </div>

        <div className="sidebar-user">
          <div className="sidebar-user-label">CONNECTÉ EN TANT QUE</div>
          <div className="sidebar-user-name">{user?.nom}</div>
          <span className="sidebar-user-role gest-role">Gestionnaire</span>
        </div>

        <nav className="sidebar-nav">
          {NAV.map(item => {
            const showGroup = item.group && item.group !== lastGroup;
            if (item.group) lastGroup = item.group;
            return (
              <React.Fragment key={item.path}>
                {showGroup && <div className="nav-group-label">{item.group}</div>}
                <NavLink
                  to={item.path}
                  end={item.end}
                  className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
                >
                  {item.label}
                </NavLink>
              </React.Fragment>
            );
          })}
        </nav>

        <button className="sidebar-logout" onClick={handleLogout}>Se déconnecter</button>
      </aside>

      {/* ── Contenu principal ── */}
      <div className="admin-main">
        <header className="topbar">
          <span className="topbar-title">{pageTitle}</span>
          <div className="topbar-right">
            <div className="topbar-avatar gest-avatar">{initials}</div>
            <span className="topbar-user-name">{user?.nom}</span>
          </div>
        </header>
        <main className="admin-content">{children}</main>
      </div>
    </div>
  );
}
