// SOS functionality
const sos = {
  socket: null,

  init() {
    this.socket = io();
    this.setupSocketListeners();
  },

  setupSocketListeners() {
    this.socket.on('sos_alert', (data) => {
      this.showAlert(data);
    });
  },

  async sendSOS() {
    try {
      const position = await this.getCurrentPosition();
      const alertData = {
        location: position,
        timestamp: new Date().toISOString()
      };

      await fetch('/sos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      });
    } catch (error) {
      console.error('Failed to send SOS:', error);
    }
  },

  getCurrentPosition() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          reject(error);
        }
      );
    });
  },

  showAlert(data) {
    const alertsContainer = document.getElementById('alerts');
    const alert = document.createElement('div');
    alert.className = 'alert';
    alert.innerHTML = `
      <strong>SOS Alert!</strong>
      <p>Location: ${data.location.latitude}, ${data.location.longitude}</p>
      <p>Time: ${new Date(data.timestamp).toLocaleString()}</p>
    `;
    alertsContainer.prepend(alert);
  }
};

export default sos;