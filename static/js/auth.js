// Authentication related functions
const auth = {
  async register(username, email, password) {
    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      
      return data;
    } catch (error) {
      throw error;
    }
  },

  async login(email, password) {
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      
      return data;
    } catch (error) {
      throw error;
    }
  },

  async logout() {
    try {
      await fetch('/logout', { method: 'POST' });
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }
};

export default auth;