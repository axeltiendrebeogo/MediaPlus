import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './AdminLayout.css';

const NAV_ITEMS = [
  { label: 'Vue globale', path: '/admin', group: 'TABLEAUX DE BORD', end: true },
  { label: 'Médias', path: '/admin/medias', group: 'GESTION' },
  { label: 'Comptes', path: '/admin/comptes', group: null },
];

export default function AdminLayout({ children, pageTitle }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/connexion');
  };

  const initials = user?.nom
    ? user.nom.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : 'AD';

  let lastGroup = null;

  return (
    <div className="admin-layout">
      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-name">MediaPulse</span>
          <span className="brand-sub">Analyse d'audience</span>
        </div>

        <div className="sidebar-user">
          <div className="sidebar-user-label">CONNECTÉ EN TANT QUE</div>
          <div className="sidebar-user-name">{user?.nom}</div>
          <span className="sidebar-user-role">Administrateur</span>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map(item => {
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

        <button className="sidebar-logout" onClick={handleLogout}>
          Se déconnecter
        </button>
      </aside>

      {/* ── Main ── */}
      <div className="admin-main">
        {/* Topbar */}
        <header className="topbar">
          <span className="topbar-title">{pageTitle}</span>
          <div className="topbar-right">
            <div className="topbar-avatar">{initials}</div>
            <span className="topbar-user-name">{user?.nom}</span>
          </div>
        </header>

        {/* Content */}
        <main className="admin-content">
          {children}
        </main>
      </div>
    </div>
  );
}
