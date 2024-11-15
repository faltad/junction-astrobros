import "./App.css";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { Layout } from "./components/Layout/Layout";
import { Map } from "./components/Map/Map";
import { DetailPage, loader } from "./components/DetailPage/DetailsPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <div>Something went very wrong in the parent element</div>,
    children: [
      {
        path: "/",
        element: <Map />,
        errorElement: <div>Something went wrong in the Child element</div>,
      },
      {
        path: "/map/details",
        element: <DetailPage />,
        loader: loader,
        errorElement: <div>Something went wrong in the Details element</div>,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
