export const environment = {
  production: false,
  keycloakConfig: {
    url: 'http://localhost/auth/',
    realm: 'datahub',
    clientId: 'angular'
  },

  secureUrlPattern: /^(.*)\/backend-fastapi\/(.*)$/
};
