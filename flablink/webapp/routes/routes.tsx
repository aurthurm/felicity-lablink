import {
  // createBrowserRouter,
  createHashRouter,
} from "react-router-dom";

import DashBoardPage from "@/pages/dashboard";
import InstrumentsPage from "@/pages/instruments";
import LoginPage from "@/pages/login";
import OrdersPage from "@/pages/orders";
import GeneralSettings from "@/pages/settings/general";
import LimsSettings from "@/pages/settings/lims";
import KeywordMapping from "@/pages/settings/mapping";
import ResultTranslation from "@/pages/settings/translation";
import ResultExclusion from "@/pages/settings/exclusion";

const router = createHashRouter([
    { path: '/', element: <DashBoardPage /> },
    { path: '/login', element: <LoginPage /> },
    { path: '/instruments', element: <InstrumentsPage /> },
    { path: '/orders', element: <OrdersPage /> },
    { 
      path: '/settings', 
      children: [
        { path: '', element: <GeneralSettings /> },
        { path: '/settings/lims', element: <LimsSettings /> },
        { path: '/settings/mappings', element: <KeywordMapping /> },
        { path: '/settings/translations', element: <ResultTranslation /> },
        { path: '/settings/exclusions', element: <ResultExclusion /> },
      ]
    },
]);

export default router;