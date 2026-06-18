import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const MOCK_USERS = {
  admin:        { id: 1, nom: 'Sami Traoré',   email: 'admin@mediapulse.bf',  role: 'admin',        media_id: null },
  gestionnaire: { id: 2, nom: 'Fatou Diallo',   email: 'fatou@rtb.bf',         role: 'gestionnaire', media_id: 1    },
  controleur:   { id: 5, nom: 'Moussa Kaboré',  email: 'moussa@mediapulse.bf', role: 'controleur',   media_id: null },
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Restore session on mount
  useEffect(() => {
    if (USE_MOCK) {
      // Restore mock session from localStorage
      const saved = localStorage.getItem('mp_mock_user');
      if (saved) {
        try { setUser(JSON.parse(saved)); } catch {}
      }
      setLoading(false);
      return;
    }

    const token = localStorage.getItem('mp_access');
    if (token) {
      api.get('/auth/me/')
        .then(res => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('mp_access');
          localStorage.removeItem('mp_refresh');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password, roleHint) => {
    if (USE_MOCK) {
      const userData = { ...(MOCK_USERS[roleHint] || MOCK_USERS.admin), email };
      localStorage.setItem('mp_mock_user', JSON.stringify(userData));
      setUser(userData);
      return userData;
    }
    const res = await api.post('/token/', { email, password });
    const { access, refresh, user: userData } = res.data;
    localStorage.setItem('mp_access', access);
    localStorage.setItem('mp_refresh', refresh);
    setUser(userData);
    return userData;
  }, []);

  const logout = useCallback(async () => {
    if (USE_MOCK) {
      localStorage.removeItem('mp_mock_user');
      setUser(null);
      return;
    }
    const refresh = localStorage.getItem('mp_refresh');
    try { await api.post('/auth/logout/', { refresh }); } catch {}
    localStorage.removeItem('mp_access');
    localStorage.removeItem('mp_refresh');
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
