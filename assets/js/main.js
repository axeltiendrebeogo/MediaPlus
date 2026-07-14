/**
 * FasoHorizon - Client Interactivity & Mock Backend Simulation
 * This script provides high-fidelity UI responses for forms, comments, and navigation.
 * All functions use stable IDs for easy targeting by external E2E testing systems (Playwright) and trackers.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initNewsletterForm();
  initContactForm();
  initCommentForms();
  initLoadMoreButton();
  updateHeaderTime();
});

/**
 * Responsive Mobile Menu Toggle
 */
function initMobileNav() {
  const toggleBtn = document.getElementById('nav-toggle-btn');
  const mainNav = document.getElementById('main-nav-menu');

  if (toggleBtn && mainNav) {
    toggleBtn.addEventListener('click', () => {
      const isOpen = mainNav.classList.contains('open');
      if (isOpen) {
        mainNav.classList.remove('open');
        toggleBtn.innerHTML = '&#9776;'; // Hamburger icon
      } else {
        mainNav.classList.add('open');
        toggleBtn.innerHTML = '&times;'; // Cross icon
      }
    });
  }
}

/**
 * Mock Newsletter Subscription Form
 */
function initNewsletterForm() {
  const form = document.getElementById('newsletter-form');
  const feedback = document.getElementById('newsletter-feedback');

  if (form && feedback) {
    form.addEventListener('submit', (e) => {
      e.preventDefault(); // Prevent full reload to allow tracking events to process
      
      const emailInput = document.getElementById('newsletter-email');
      const emailVal = emailInput ? emailInput.value.trim() : '';

      if (!emailVal) return;

      // Simulate network latency for a highly realistic interaction
      const submitBtn = document.getElementById('newsletter-submit');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Inscription...';
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = "S'abonner";
        }
        
        feedback.innerText = `Merci! L'adresse ${emailVal} a bien été enregistrée pour la newsletter.`;
        feedback.className = 'form-feedback success';
        
        if (emailInput) emailInput.value = '';
      }, 800);
    });
  }
}

/**
 * Mock Contact Form Submission
 */
function initContactForm() {
  const form = document.getElementById('contact-form');
  const feedback = document.getElementById('contact-feedback');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const name = document.getElementById('contact-name').value;
      const email = document.getElementById('contact-email').value;
      const submitBtn = document.getElementById('contact-submit');

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Envoi en cours...';
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = 'Envoyer le message';
        }

        if (feedback) {
          feedback.innerText = `Merci ${name}, votre message a été envoyé avec succès! Nous vous répondrons à l'adresse ${email}.`;
          feedback.style.display = 'block';
          feedback.style.color = '#0f6236';
          feedback.style.marginTop = '15px';
          feedback.style.fontWeight = 'bold';
        }

        form.reset();
      }, 1000);
    });
  }
}

/**
 * Mock Comments Appending & Submissions
 */
function initCommentForms() {
  // Select all comment forms (they match comment-form-{slug})
  const forms = document.querySelectorAll('[id^="comment-form-"]');
  
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const articleSlug = form.id.replace('comment-form-', '');
      const authorInput = form.querySelector('#comment-author');
      const textInput = form.querySelector('#comment-text');
      const submitBtn = form.querySelector('#comment-submit');
      const commentsList = document.getElementById(`comments-list-${articleSlug}`);
      const commentsCountText = document.getElementById(`comments-count-${articleSlug}`);

      if (!authorInput || !textInput) return;

      const author = authorInput.value.trim();
      const text = textInput.value.trim();

      if (!author || !text) return;

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Publication...';
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = 'Publier le commentaire';
        }

        // Add to comments list
        if (commentsList) {
          const newComment = document.createElement('div');
          newComment.className = 'comment-item';
          
          // Get initials
          const initials = author.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
          const dateStr = 'À l\'instant';

          newComment.innerHTML = `
            <div class="comment-avatar">${initials || 'A'}</div>
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author">${author}</span>
                <span class="comment-date">${dateStr}</span>
              </div>
              <p class="comment-text">${text}</p>
            </div>
          `;
          commentsList.appendChild(newComment);
        }

        // Increment count
        if (commentsCountText) {
          const currentCount = parseInt(commentsCountText.innerText) || 0;
          commentsCountText.innerText = `${currentCount + 1} Commentaire(s)`;
        }

        // Reset form
        form.reset();
      }, 600);
    });
  });
}

/**
 * Simulates loading more articles on the homepage grid
 */
function initLoadMoreButton() {
  const btn = document.getElementById('load-more-btn');
  const container = document.getElementById('recent-articles-grid');

  if (btn && container) {
    let clickCount = 0;

    btn.addEventListener('click', () => {
      clickCount++;
      btn.classList.add('loading');
      btn.innerText = 'Chargement...';

      // Mock list of generated extra articles
      const extraArticles = [
        {
          slug: 'modernisation-coton-burkina',
          category: 'economie',
          badgeClass: 'badge-economie',
          categoryLabel: 'Économie',
          title: 'Filière coton : La SOFITEX lance son programme de modernisation technologique',
          desc: 'La Société Burkinabè des Fibres Textiles a dévoilé un plan massif visant à équiper les coopératives de capteurs connectés et d\'équipements d\'égrenage de dernière génération.',
          author: 'Moussa Barro',
          date: '13 Juillet 2026',
          img: 'https://picsum.photos/id/102/400/250'
        },
        {
          slug: 'fespaco-preparation-ouaga',
          category: 'culture',
          badgeClass: 'badge-culture',
          categoryLabel: 'Culture',
          title: 'FESPACO 2027 : Les travaux de rénovation des salles de projection débutent à Ouaga',
          desc: 'Pour accueillir la biennale du cinéma africain dans des conditions optimales, la municipalité a débloqué des fonds exceptionnels pour équiper les salles historiques de projecteurs laser 4K.',
          author: 'Amina Sanou',
          date: '12 Juillet 2026',
          img: 'https://picsum.photos/id/366/400/250'
        },
        {
          slug: 'etudiants-innovation-energie',
          category: 'societe',
          badgeClass: 'badge-societe',
          categoryLabel: 'Société',
          title: 'Innovation verte : Des étudiants de l\'Université Joseph Ki-Zerbo primés pour leur kit solaire d\'irrigation',
          desc: 'Une équipe multidisciplinaire a conçu un système de pompage solaire intelligent à bas coût facilitant l\'irrigation agricole des petites exploitations maraîchères.',
          author: 'Fidèle Kaboré',
          date: '11 Juillet 2026',
          img: 'https://picsum.photos/id/201/400/250'
        }
      ];

      setTimeout(() => {
        btn.classList.remove('loading');
        btn.innerText = 'Charger plus d\'articles';

        extraArticles.forEach(art => {
          const card = document.createElement('article');
          card.className = 'news-card';
          card.setAttribute('data-category', art.category);
          
          card.innerHTML = `
            <div class="card-img-wrapper">
              <img src="${art.img}" alt="${art.title}">
            </div>
            <div class="card-content">
              <div class="card-meta">
                <span class="badge ${art.badgeClass}">${art.categoryLabel}</span>
                <span>Par ${art.author}</span>
                <span>${art.date}</span>
              </div>
              <h4><a href="articles/${art.slug}.html">${art.title}</a></h4>
              <p>${art.desc}</p>
              <a href="articles/${art.slug}.html" class="btn-read-more">Lire la suite</a>
            </div>
          `;
          container.appendChild(card);
        });

        // Hide load more button after 2 clicks to simulate end of articles list
        if (clickCount >= 2) {
          btn.style.display = 'none';
        }
      }, 1000);
    });
  }
}

/**
 * Updates the localized date/time stamp in the header
 */
function updateHeaderTime() {
  const dateEl = document.getElementById('header-date-text');
  if (dateEl) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Africa/Ouagadougou' };
    const today = new Date();
    // Force French locale for Burkinabè media look
    try {
      dateEl.innerText = today.toLocaleDateString('fr-BF', options);
    } catch(e) {
      dateEl.innerText = today.toLocaleDateString('fr-FR', options);
    }
  }
}
