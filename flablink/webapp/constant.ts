const NODE_ENV = process.env.NODE_ENV ?? "development";
export const IS_DEV = NODE_ENV === "development";

export const WS_CLIENT_ID = Math.random().toString(36).replace(/^0\./, '').substring(2, length);

export const REACT_APP_API_BASE_URL = IS_DEV ? "http://localhost:8000" : "" + "/api/v1";

export let REACT_APP_WS_URL: string;
if (REACT_APP_API_BASE_URL?.includes("http")) {
    REACT_APP_WS_URL = `ws://${REACT_APP_API_BASE_URL.replace("http://", "")}`;
} else {
    REACT_APP_WS_URL = `ws://${window.location.host}`;
}