import { REACT_APP_API_BASE_URL } from "./constant"


export const useUrl = (path: string) => {
    return `${REACT_APP_API_BASE_URL}${path}`;
}