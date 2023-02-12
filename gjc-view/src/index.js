import React from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import App from './App';
import './styles/index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <MantineProvider withNormalizeCSS withGlobalStyles>
    <NotificationsProvider>
    <React.StrictMode>
      <App />
    </React.StrictMode>
    </NotificationsProvider>
  </MantineProvider>
);