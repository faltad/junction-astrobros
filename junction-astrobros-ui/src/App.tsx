import "./App.css";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import placeholderImage from './assets/fig2.jpg';
import { Layout } from "./components/Layout/Layout";

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <div>Something went very wrong in the parent element</div>,
    children: [
      {
        path: '/image',
        element: <div><img src={placeholderImage} /></div>,
        errorElement: <div>Something went wrong in the Child element</div>
      }
    ]
  }
]);

function App() {
  return (
    <Layout />
  );
}

export default App;
