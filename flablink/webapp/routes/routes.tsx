import {
  // createBrowserRouter,
  createHashRouter,
} from "react-router-dom";

import DashBoardPage from "@/pages/dashboard";
import InstrumentsPage from "@/pages/instruments";
import LoginPage from "@/pages/login";

const router = createHashRouter([
    { path: '/', element: <DashBoardPage /> },
    { path: '/login', element: <LoginPage /> },
    { path: '/instruments', element: <InstrumentsPage /> },
]);

export default router;