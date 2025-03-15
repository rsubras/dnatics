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

  useEffect(() => {
    if (token) {
      document.body.classList.remove('body-unauthenticated');
    } else {
      document.body.classList.add('body-unauthenticated');
    }
  }, [token]);

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
      <div className="header-container">
        <img src="https://img1.wsimg.com/isteam/ip/4388fafb-e7a9-46cb-bc19-fce8e18b2928/dnatics-dark-blue.png/:/rs=w:304,h:76,cg=true,m/cr=w:304,h:76/qt=q:100/ll" className="img-left"/>
        <h1>ReactJS - AI app demo</h1>
      </div>
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