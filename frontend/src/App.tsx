import { createBrowserRouter, RouterProvider, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import LoginPage from "./features/login/LoginPage";
import WorkoutPage from "./features/workout/WorkoutPage";
import CalendarPage from "./features/calendar/CalendarPage";
import ProgramPage from "./features/program/ProgramPage";

const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  { path: "/", element: <Navigate to="/login" replace /> },
  {
    element: <Layout />,
    children: [
      { path: "/treino", element: <WorkoutPage /> },
      { path: "/calendario", element: <CalendarPage /> },
      { path: "/programa", element: <ProgramPage /> },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
