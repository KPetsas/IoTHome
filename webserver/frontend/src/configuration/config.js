var config = module.exports = {};

config.productionEnv = false;

config.backend = {
  ip: '127.0.0.1',  // DEV
  port: 9191,  // DEV
  urlPrefix: '/api',
  devicesEndpoint: '/devices',
  wifiSwitchesEndpoint: '/wifi-switches',
  doorOpenerEndpoint: '/door-opener',
  tokenRefreshEndpoint: '/token/refresh',
  loginEndpoint: '/login',
  headers: {
    'Content-Type': 'application/json'
  }
};

config.frontend = {
  loadingPageDuration: 500,
  alertAutoHideDuration: 4500,
  doorBtnLoadingDuration: 2500  // Same as device firmware 2.5 seconds.
};
