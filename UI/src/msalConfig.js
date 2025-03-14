import { PublicClientApplication } from "@azure/msal-browser";

const MSAL_CONFIG = {
    auth: {
        clientId: "7ad70369-dbce-4e8e-9e31-eef6f405345c",
        authority: `https://login.microsoftonline.com/88bc54ee-b6f0-40a6-bf35-d729f9f74d23`,
        redirectUri: "http://localhost:3000",
    },
    cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false,
    },
};

const TOKEN_REQUEST = {
    scopes: ["https://analysis.windows.net/powerbi/api/.default"]
};

const LOGIN_REQUEST = {
    scopes: ["User.ReadWrite.All"]
};

const GRAPH_CONFIG = {
    graphUsersEndpoint: "https://graph.microsoft.com/v1.0/users"
};

const PUBLIC_CLIENT_APPLICATION = new PublicClientApplication(MSAL_CONFIG);
async function initializeMsal() {
    await PUBLIC_CLIENT_APPLICATION.initialize();
}
initializeMsal();

export {
    MSAL_CONFIG,
    LOGIN_REQUEST,
    TOKEN_REQUEST,
    GRAPH_CONFIG,
    PUBLIC_CLIENT_APPLICATION
};