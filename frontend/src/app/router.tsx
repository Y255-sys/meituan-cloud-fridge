import { createBrowserRouter } from "react-router-dom";

import { ProtectedLayout } from "./layouts/AppShell";
import { HomePage } from "pages/HomePage";
import { InventoryPage } from "pages/InventoryPage";
import { LoginPage } from "pages/LoginPage";
import { NotFoundPage } from "pages/NotFoundPage";
import { PurchasePage } from "pages/PurchasePage";
import { RecognizePage } from "pages/RecognizePage";
import { RecipesPage } from "pages/RecipesPage";
import { SeniorModePage } from "pages/SeniorModePage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: <ProtectedLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "recognize", element: <RecognizePage /> },
      { path: "inventory", element: <InventoryPage /> },
      { path: "recipes", element: <RecipesPage /> },
      { path: "purchase", element: <PurchasePage /> },
      { path: "senior", element: <SeniorModePage /> },
    ],
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);
