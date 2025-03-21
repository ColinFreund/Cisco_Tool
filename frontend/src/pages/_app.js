import '../styles/globals.css';
import React from 'react';

// This component is used to initialize pages
function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;