import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './ControleurLayout.css';

const NAV = [
  { label: 'Dashboard',       path: '/controleur',            group: 'VUE GLOBALE', end: true },
  { label: 'Tous les médias', path: '/controleur/medias',     group: null },
  { label: 'Comparaison',     path: '/controleur/comparaison',group: null },
  { label: 'Tous les rapports', path: '/controleur/rapports', group: 'RAPPORTS' },
  { label: 'Générer rapport', path: '/controleur/rapports/generer', group: null },
  { label: 'Affectations',    path: '/controleur/affectations',group: 'GESTION' },
];

export default function ControleurLayout({ children, pageTitle }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => { await logout(); navigate('/connexion'); };

  const initials = user?.nom
    ? user.nom.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : 'CT';

  let lastGroup = null;

  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-name">FasoMedia Insights</span>
          <span className="brand-sub">Analyse d'audience</span>
        </div>

        <div className="sidebar-user">
          <div className="sidebar-user-label">CONNECTÉ EN TANT QUE</div>
          <div className="sidebar-user-name">{user?.nom}</div>
          <span className="sidebar-user-role ctrl-role">Contrôleur</span>
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

      <div className="admin-main">
        <header className="topbar">
          <span className="topbar-title">{pageTitle}</span>
          <div className="topbar-right">
            <div className="topbar-avatar ctrl-avatar">{initials}</div>
            <span className="topbar-user-name">{user?.nom}</span>
          </div>
        </header>
        <main className="admin-content">{children}</main>
      </div>
    </div>
  );
}
