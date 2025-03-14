import { useState, useEffect } from 'react';
import './App.css';
import { LOGIN_REQUEST, PUBLIC_CLIENT_APPLICATION, TOKEN_REQUEST } from './msalConfig';
import Layout from './components/Layout';
import LeftContainer from './components/LeftContainer';
import RightContainer from './components/RightContainer';

function App() {
  const [token, setToken] = useState(null);
  const [interactionInProgress, setInteractionInProgress] = useState(false);

  useEffect(() => {
    const initializeMsal = async () => {
      await PUBLIC_CLIENT_APPLICATION.initialize();
      
    const handleRedirectResponse = async () => {
      const loginResponse = await PUBLIC_CLIENT_APPLICATION.handleRedirectPromise();
      
      if (loginResponse) {
        if (loginResponse.account) {
          //console.log("Account:",loginResponse.account);
          const accounts = PUBLIC_CLIENT_APPLICATION.getAllAccounts();
          //console.log("Accounts:",accounts);

          PUBLIC_CLIENT_APPLICATION.setActiveAccount(loginResponse.account);
          const tokenResponse = await PUBLIC_CLIENT_APPLICATION.acquireTokenSilent({
            ...TOKEN_REQUEST,
            account: loginResponse.account[0],
          });
          //console.log("Token Response:",tokenResponse.accessToken)
          setToken(tokenResponse.accessToken);
        }
      }
    };

    handleRedirectResponse();
  };
  initializeMsal();
  }, []);

  const handleSignIn = () => {

    PUBLIC_CLIENT_APPLICATION.loginRedirect(LOGIN_REQUEST);
  }

  const handleSignOut = async () => {
    if (!interactionInProgress) {
      setInteractionInProgress(true);
      PUBLIC_CLIENT_APPLICATION.logout();
      setToken(null);
      setInteractionInProgress(false);
    }
  }

  const handleRefreshToken = async () => {
    const tokenResponse = await PUBLIC_CLIENT_APPLICATION.acquireTokenSilent(TOKEN_REQUEST);
    setToken(tokenResponse.accessToken);
  }

  return (
    <div className="App">
      <h1>
        dnatics ReactJS apps 
      </h1>
      {
        token ? (
          <Layout>
          <div style={{ display: 'flex' }}>
            <LeftContainer />
            <RightContainer />
          </div>
                </Layout>
        )
          : (
            <div>
              <p
                style={{
                  color: 'red',
                  fontSize: '20px',
                  fontWeight: 'bold'
                }}
              >
                You are not authenticated!
              </p>
              <p>
                Please click the button below to login.
              </p>

              <button
                onClick={handleSignIn}
              >
                Login
              </button>
            </div>
          )
      }
    </div>
  );
}

export default App;