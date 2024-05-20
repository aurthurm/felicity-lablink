import { REACT_APP_API_BASE_URL, REACT_APP_WS_URL } from "./constant"


export const useUrl = (path: string) => {
    return `${REACT_APP_API_BASE_URL}${path}`;
}

export const useWs = (path: string) => {
    return `${REACT_APP_WS_URL}${path}`;
}