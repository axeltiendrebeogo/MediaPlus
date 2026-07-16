import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const features = [
  {
    title: 'Tableaux de bord',
    desc: 'KPIs en temps réel, graphiques interactifs, filtres par période.',
  },
  {
    title: 'Analyse par page',
    desc: 'Scroll, durée, provenance — métriques détaillées par contenu.',
  },
  {
    title: 'Audio / Vidéo',
    desc: 'Taux de complétion, durée d\'écoute, popularité par épisode.',
  },
  {
    title: 'Rapports PDF',
    desc: 'Générés à la demande selon vos filtres, exportables en PDF.',
  },
  {
    title: 'Filtrage avancé',
    desc: 'Par période, appareil, source de trafic, type de contenu.',
  },
  {
    title: 'Accès sécurisé',
    desc: 'Espace privé par média, authentification JWT, rôles distincts.',
  },
];

const steps = [
  { n: '1', title: 'Compte créé', desc: "L'admin crée votre accès et envoie vos identifiants." },
  { n: '2', title: 'Vous connectez', desc: "Accès sécurisé depuis n'importe quel navigateur." },
  { n: '3', title: 'Consultez vos données', desc: 'Performances de vos pages en temps réel.' },
  { n: '4', title: 'Générez vos rapports', desc: 'Rapports PDF à la demande avec vos filtres.' },
];

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home">
      {/* ── Navbar ── */}
      <nav className="home-nav">
        <div className="home-nav-brand">
          <span className="home-brand-name">Mediaplus</span>
          <span className="home-brand-tagline">Analyse d'audience</span>
        </div>
        <button className="btn btn-secondary" onClick={() => navigate('/connexion')}>
          Se connecter
        </button>
      </nav>

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-inner">
            <span className="hero-badge">Plateforme professionnelle</span>
            <h1 className="hero-headline">
              Comprenez votre audience.<br />
              <span className="text-primary">Développez votre impact.</span>
            </h1>
            <p className="hero-desc">
              Mediaplus centralise l'analyse d'audience de vos médias en ligne. Visiteurs,
              comportements, contenus — toutes vos données en un seul endroit.
            </p>
            <div className="hero-actions">
              <button className="btn btn-primary btn-lg" onClick={() => navigate('/connexion')}>
                Accéder à la plateforme
              </button>
              <button
                className="btn btn-secondary btn-lg"
                onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
              >
                Découvrir les services
              </button>
            </div>

            {/* Stats */}
            <div className="hero-stats">
              <div className="hero-stat">
                <span className="hero-stat-value text-primary">+18%</span>
                <span className="hero-stat-label">Croissance audience</span>
              </div>
              <div className="hero-stat-divider" />
              <div className="hero-stat">
                <span className="hero-stat-value text-primary">4</span>
                <span className="hero-stat-label">Types de médias</span>
              </div>
              <div className="hero-stat-divider" />
              <div className="hero-stat">
                <span className="hero-stat-value text-primary">100%</span>
                <span className="hero-stat-label">Données sécurisées</span>
              </div>
            </div>
          </div>

          {/* Aperçu produit */}
          <div className="hero-visual" aria-hidden="true">
            <div className="hero-preview-card">
              <div className="hero-preview-header">
                <span className="hero-preview-dot" />
                <span className="hero-preview-dot" />
                <span className="hero-preview-dot" />
                <span className="hero-preview-title">Tableau de bord</span>
              </div>
              <div className="hero-preview-body">
                <div className="hero-preview-chart">
                  <div className="hero-bar" style={{ height: '40%' }} />
                  <div className="hero-bar" style={{ height: '65%' }} />
                  <div className="hero-bar" style={{ height: '50%' }} />
                  <div className="hero-bar" style={{ height: '80%' }} />
                  <div className="hero-bar" style={{ height: '60%' }} />
                  <div className="hero-bar hero-bar-active" style={{ height: '95%' }} />
                  <div className="hero-bar" style={{ height: '70%' }} />
                </div>
                <div className="hero-preview-rows">
                  <div className="hero-preview-row">
                    <span className="hero-preview-row-label">Radio Faso FM</span>
                    <span className="hero-preview-row-value text-primary">2 340 écoutes</span>
                  </div>
                  <div className="hero-preview-row">
                    <span className="hero-preview-row-label">Le Quotidien BF</span>
                    <span className="hero-preview-row-value text-primary">14 820 vues</span>
                  </div>
                  <div className="hero-preview-row">
                    <span className="hero-preview-row-label">SportInfo TV</span>
                    <span className="hero-preview-row-value text-primary">6 105 vues</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="section" id="features">
        <div className="section-header">
          <h2 className="section-title">Ce que la plateforme vous offre</h2>
          <p className="section-subtitle">Des outils pensés pour les médias, simples à utiliser et efficaces.</p>
        </div>
        <div className="features-grid">
          {features.map(f => (
            <div className="feature-card card" key={f.title}>
              <div className="feature-title">{f.title}</div>
              <div className="feature-desc">{f.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Steps ── */}
      <section className="section section-alt">
        <div className="steps-grid">
          {steps.map(s => (
            <div className="step" key={s.n}>
              <div className="step-num">{s.n}</div>
              <div className="step-title">{s.title}</div>
              <div className="step-desc">{s.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="cta-section">
        <h2 className="cta-title text-primary">Prêt à analyser votre audience ?</h2>
        <p className="cta-sub text-primary">Connectez-vous à votre espace pour accéder à vos données.</p>
        <button className="btn btn-primary btn-lg" onClick={() => navigate('/connexion')}>
          Se connecter à la plateforme
        </button>
        <p className="cta-note text-primary">
          L'inscription n'est pas ouverte au public. L'accès est attribué par l'administrateur.
        </p>
      </section>

      {/* ── Footer ── */}
      <footer className="home-footer">
        <span className="font-semibold">Mediaplus</span>
        <span className="text-muted">© 2026 — Mediaplus</span>
      </footer>
    </div>
  );
}
